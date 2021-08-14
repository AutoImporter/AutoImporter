import sys
import requests

# Logs in to seiso using the user_agent, seiso_username, seiso_password and debug
# Returns the seiso session_id
# TODO: Probably move to seiso.py
def login_seiso(settings):

    headers = {
        'user-agent': settings['user_agent'],
    }

    data = {
      'username': settings['seiso_username'],
      'password': settings['seiso_password']
    }

    response = requests.post('https://seiso.party/account/login', headers=headers, data=data)


    print("Getting Seiso Session Key..")

    if settings['debug']:
        print(response)
        print(response.headers)

    try:
        session_id = response.headers['Set-Cookie'].split('session=')[1].split(';')[0]
    except Exception as e:
        if settings['debug']:
            print(e)
        session_id = None

    if settings['debug']:
        print(session_id)
    if not session_id:
        print("Invalid Seiso Credentials.")
        print("Update Seiso Session Key/ID in the config manually or re-check your credentials!")
        # TODO: Handle invalid details gracefully
        sys.exit()


    return session_id
