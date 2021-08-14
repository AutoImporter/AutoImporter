import os

CONFIG_NAME = 'settings.conf'
CONFIG_PATH = os.path.join(os.path.curdir, CONFIG_NAME)

# Changes/adds a key value pair to the config file and rewrites to disk
def update_config(key, value):

    with open(CONFIG_PATH, 'r') as file:
        data = file.readlines()

    for index, line in enumerate(data):
        if line.split(':')[0] == key:
            data[index] = '{}:{}\n'.format(key,value)
            break
    else: # No break
        # The key was not found so add a new key
        data.append('{}:{}\n'.format(key,value))

    with open(CONFIG_PATH, 'w') as file:
        file.writelines(data)

# Called when a config file is not detected, creates a new config file interactively
def create_config():

    # TODO: Validate the existing config, and ensure required values are present
    # TODO: Clean up questions, default values and wording, it's a mess currently
    # TODO: Have command line arguments as an alternative to make docker support far easier (Could be used to configure, or perhaps for a single execution)
    if not os.path.isfile(CONFIG_PATH):

        print("No config exists.")

        print("Creating Config..")

        print("If a prompt mentions a default value, you can simply press enter.")

        print("This program can either use the provided session key or login credentials to get one.")

        default_useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'

        if (input("Do you want to provide a session key? (Default is No) ").lower() or 'n')[0] == "n":
            email = input("Patreon Email: ")
            password = input("Patreon Password: ")
            session_key = '<enter session key>'
            user_agent = input("User Agent (default is a chrome 87 user agent): ") or default_useragent
        else:
            email = '<enter email>'
            password = '<enter password>'
            session_key = input("Session Key: ")
            user_agent = default_useragent

        if (input("Do you want to login to seiso for importer credit? (Default is No) ").lower() or 'n')[0] != "n":
            if (input("Do you want to login to seiso using a session_key? (Default is No) ").lower() or 'n')[0] != "n":
                seiso_username = '<enter username>'
                seiso_password = '<enter password>'
                seiso_session_key = input("Seiso Session Key: ")
            else:
                seiso_username = input("Seiso Username: ")
                seiso_password = input("Seiso Password: ")
                seiso_session_key = '<enter session key>'
            seiso_account = 'True'
        else:
            seiso_username = '<enter email>'
            seiso_password = '<enter password>'
            seiso_session_key = '<enter session key>'
            seiso_account = 'False'

        kemono = input("Import to Kemono (default is True): ") or 'True'
        seiso = input("Import to Seiso (default is True): ") or 'True'
        time_between_imports = input("Time between imports in hours (default is 24): ") or '24'
        time_between_attempts = input("Time between import re-attempts in seconds (default is 600): ") or '600'
        time_wait_to_check = input("Time to wait to check if an import was successful in seconds (default is 15): ") or '15'
        retry_attempts_before_relogin = input("Attempts between patreon re-login (default is 3): ") or '3'
        debug = input("Debug mode (default is False): ") or 'False'
        allow_dev_session_debug = input("Allow kemono/seiso debug session id for developers (default is False): ") or 'False'

        print("Saving new config..")

        with open(CONFIG_PATH, 'w') as file:
            file.write('email:{}\n'.format(email))
            file.write('password:{}\n'.format(password))
            file.write('session_key:{}\n'.format(session_key))
            file.write('user_agent:{}\n'.format(user_agent))
            file.write('kemono:{}\n'.format(kemono))
            file.write('seiso:{}\n'.format(seiso))
            file.write('seiso_account:{}\n'.format(seiso_account))
            file.write('seiso_username:{}\n'.format(seiso_username))
            file.write('seiso_password:{}\n'.format(seiso_password))
            file.write('seiso_session_key:{}\n'.format(seiso_session_key))
            file.write('time_between_imports:{}\n'.format(time_between_imports))
            file.write('time_between_attempts:{}\n'.format(time_between_attempts))
            file.write('time_wait_to_check:{}\n'.format(time_wait_to_check))
            file.write('retry_attempts_before_relogin:{}\n'.format(retry_attempts_before_relogin))
            file.write('debug:{}\n'.format(debug))
            file.write('allow_dev_session_debug:{}\n'.format(allow_dev_session_debug))

# Loads the config from disk and returns the settings in a dictionary
# Handles booleans and strings only
# TODO: Switch over to a library instead, or maybe extend to more common variable types
# TODO: Rewrite it so it isn't one line
def load_config():

    with open(CONFIG_PATH) as file:
        settings = {line.split(":")[0].strip():(":".join(line.split(":")[1:]).strip() if ":".join(line.split(":")[1:]).strip() not in ["True", "False"] else (True if (":".join(line.split(":")[1:]).strip() == "True") else False)) for line in file.readlines()}

    return settings
