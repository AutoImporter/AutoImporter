import requests

# Takes in the user_agent, session_id, allow_dev_session_debug and debug
# Returns the log_id of the import
def import_kemono(session_id,settings):

    headers = {
        'User-Agent': settings['user_agent'],
    }

    # Send service type and session key to kemono
    data = {
      'service': 'patreon',
      'session_key': session_id
    }

    if settings['allow_dev_session_debug']:
        data['save_session_key'] = '1'

    response = requests.post('https://kemono.party/api/import', headers=headers, data=data)

    if settings['debug']:
        print(response.url)
        print(response.headers)

     # Retrieve the log ID from the kemono import to check if the import was successful
    if "/importer/status/" in response.text:
        try:
            log_id = response.text.split("/importer/status/")[1].split("'")[0]
            if settings['debug']:
                print("https://kemono.party/importer/status/{}".format(log_id))
        except Exception as e:
            if settings['debug']:
                print(e)
    else:
        log_id = None

    return log_id
