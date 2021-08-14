import requests
import time
import json
import sys

import config # Handles reading and writing to the config file
from login import login # Handles the patreon login if the session_id is invalid

from kemono import import_kemono # Handles most kemono related code
from seiso import import_seiso # Handles most seiso related code

# TODO: Stop using 'session_id' and 'session_key' interchangeably, maybe use 'token'?

# Checks if the session_id for patreon worked on seiso/kemono
# Returns true/false
# TODO: move into each importers own file and write only for that importer, eg. (kemono.validate_session_id() and seiso.validate_session_id())
def validate_session_id(url,settings):

    result = False
    try:
        headers = {
            'User-Agent': settings['user_agent'],
        }
        response = requests.get(url, headers=headers)
        parsed_response = response.json()
        if len(parsed_response) >= 2:
            if 'already being imported' in parsed_response[1]: # Seiso doesn't allow importing the same session key simultaneously but it serves our purposes
                result = True
            elif 'Importing campaign' in parsed_response[1] or 'Importing pledge' in parsed_response[1]: # Sometimes might be very slow and take a long time to actually start importing
                result = True
            elif 'No active subscriptions' in parsed_response[1]:
                print('No active subscriptions or invalid key.')
                # TODO: Handle accounts without active subscriptions gracefully
                sys.exit()
            else:
                if settings['debug']:
                    print("Unknown Importer Status")
                    print(parsed_response)
        print("{website} Import {status}!".format(website='Kemono' if 'kemono' in url.lower() else 'Seiso', status='Successful' if result else 'Unsuccessful'))
    except Exception as e:
        if settings['debug']:
            print(e)
    return result

attempts = 0

# Does an import, returns true if time_between_imports is 0, signaling that the program should terminate the main loop and exit
# TODO: Completely rewrite IMO, too many side effects and not easy to debug
def do_import():
    global attempts

    config.create_config()
    settings = config.load_config()

    # Log in and get a new session key, or use the old session key
    if settings['session_key'] == "<enter session key>":
        print("Logging in..")
        session_id = login(settings)
        # Update the config
        config.update_config('session_key', session_id)
        # Update the value in the settings that are already loaded
        settings['session_key'] = session_id
    else:
        if attempts > 0:
            print('Attempting same session key ({}/3)..'.format(attempts))
        else:
            print("Using pre-existing session key..")
        session_id = settings['session_key']

    # Import to Kemono and Seiso
    if settings['kemono']:
        print("Importing to Kemono..")
        log_id_kemono = import_kemono(session_id, settings)

    if settings['seiso']:
        print("Importing to Seiso..")
        log_id_seiso = import_seiso(session_id, settings)

    # Wait X seconds before checking if the session key was valid
    time.sleep(int(settings['time_wait_to_check']))

    old_attempts = attempts

    # Check if the imports were successful
    if settings['kemono']:
        result = validate_session_id('https://kemono.party/api/logs/{}'.format(log_id_kemono), settings)
        if not result:
            attempts += 1

    if settings['seiso']:
        result = validate_session_id('https://seiso.party/api/logs/{}'.format(log_id_seiso), settings)
        if not result and old_attempts == attempts:
            attempts += 1

    # There was no failure this time
    # TODO: Fix bug where one website might fail where the other succeeds, handle retries individually
    if attempts == old_attempts:
        attempts = 0

    if attempts == 0:
        # Wait to import again, or exit the program
        time_between_imports = int(settings['time_between_imports'])
        if time_between_imports > 0:
            print("Importing again in {time_between_imports} hour{plural}.".format(time_between_imports=time_between_imports, plural='s' if time_between_imports != 1 else ''))
            time.sleep(3600*time_between_imports)
        else: # Only one import was required, as the time_between_imports was 0
            print("Done.")
            return True
    elif attempts > int(settings['retry_attempts_before_relogin']):
        # TODO: Fix login loop due to one website being down or constantly failing
        if attempts > int(settings['retry_attempts_before_relogin']): # Temp fix to wait even longer between severe failure
            print('Potential Severe Website Failure - Waiting for an hour.')
            time.sleep(3600) # Wait an hour as relogging in to patreon didn't work

        # Update the config
        config.update_config('session_key', '<enter session key>')
        # Update the value in the settings that are already loaded
        settings['session_key'] = '<enter session key>'

    # Wait some time between the next attempt, it may just be a temporary issue
    if attempts > 0:
        time.sleep(int(settings['time_between_attempts']))

# Do imports until signaled to stop (Only if time_between_imports is 0, otherwise runs forever)
def main():
    result = False
    while not result:
        result = do_import()

# Only run if not imported into another python program
if __name__ == "__main__":
    main()
