import requests
from login_seiso import login_seiso # Handles the seiso login
import config # Handles reading and writing to the config file

# Takes in the user_agent, session_id, seiso_account, allow_dev_session_debug and debug
# Returns the log_id of the import
# If seiso_account is used, will use seiso_username, seiso_password and seiso_session_key
def import_seiso(session_id,settings):

    headers = {
        'User-Agent': settings['user_agent'],
    }

    # If seiso accounts are enabled in the config
    if settings['seiso_account']:
        # If there is no session key, login and get a new one
        if settings['seiso_session_key'] == '<enter session key>':
            seiso_session_id = login_seiso(settings)
            # if a session_id is found, write it to the config
            if seiso_session_id:
                # Update the config
                config.update_config('seiso_session_key', seiso_session_id)
                # Update the value in the settings that are already loaded
                settings['seiso_session_key'] = seiso_session_id

        # TODO: Clean up all this seiso login code
        # TODO: Implement a rate limit to 5 attempts per 5 minutes
        # If there is a seiso_session_key, add it to the cookies
        if settings['seiso_session_key'] != '<enter session key>':
            headers['cookie'] = 'session={}'.format(settings['seiso_session_key'])

    # Send service type and session key to seiso
    data = {
      'service': 'patreon',
      'session_key': session_id
    }

    if settings['allow_dev_session_debug']:
        data['save_session_key'] = '1'

    response = requests.post('https://seiso.party/api/import', headers=headers, data=data)

    if settings['debug']:
        print(response.url)
        print(response.headers)

    # Retrieve the log ID from the seiso import to check if the import was successful
    if "/importer/status/" in response.url:
        log_id = response.url.split("/importer/status/")[1]
    else:
        log_id = None

    return log_id
