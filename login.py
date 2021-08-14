import sys
import cloudscraper # Bypass cloudflare verification (Doesn't seem very necessary ATM)

# Attempts to login to patreon, takes the settings from the config and returns the session_id if successful or exits the program
# Only uses user_agent, email and password (and debug)
def login(settings):

    scraper = cloudscraper.create_scraper()

    headers = {
        'user-agent': settings['user_agent'],
    }

    data = '{"data":{"type":"user","attributes":{"email":"'+settings['email']+'","password":"'+settings['password']+'"},"relationships":{}}}'

    response = scraper.post('https://www.patreon.com/api/login', headers=headers, data=data)

    print("Getting Session Key..")

    session_id = response.cookies.get('session_id')
    if settings['debug']:
        print(session_id)
    if not session_id: # TODO: Have reattempts for the patreon login
        print("Invalid Credentials.")
        print("Update Session Key/ID in the config manually or re-check your credentials!")
        sys.exit()

    return session_id
