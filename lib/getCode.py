import getlink
import asyncio
import requests
from Constants import ClientId
from urllib.parse import urlparse, parse_qs
from http.cookiejar import CookieJar



async def getCode(credentials):
    link, code_challenge, code_verifier = await getlink.generateLoginLink()
    session = requests.Session()
    session.cookies = CookieJar()
    resp = session.get(link, allow_redirects=False)
    url = resp.headers.get('Location')
    if not isinstance(url, str):
        raise Exception("Invalid login url")

    parsed_url = urlparse(url)

    challenge = parse_qs(parsed_url.query).get("login_challenge", [None])[0]

    if not challenge:
        raise Exception("Invalid login challenge")

    form_data = {
    'challenge': challenge,
    'client_id': ClientId,
    'famiglia_customer_code': credentials['schoolCode'],
    'login': "true",
    'password': credentials['password'],
    'username': credentials['username']
    }
    resp2 = session.post(
        "https://www.portaleargo.it/auth/sso/login",
        data=form_data,
        allow_redirects=False,
        headers={"content-type": "application/x-www-form-urlencoded"}
    )
    location = resp2.headers.get('Location')

    if not isinstance(location, str):
        raise Exception("Invalid login redirect")

    resp3 = session.get(location, allow_redirects=False)
    location= resp3.headers.get('Location')
    resp4 = session.get(location, allow_redirects=False)
    location = resp3.headers.get('Location')
    resp5 = session.get(location, allow_redirects=False)
    location = resp5.headers.get('Location')
    final_resp = session.get(location, allow_redirects=False)
    location = final_resp.headers.get('Location')
    parsed_loc = urlparse(location)
    code = parse_qs(parsed_loc.query).get("code", [None])[0]
    if not code:
        raise Exception("Invalid login code")

    return code, code_challenge, code_verifier


if __name__ == '__main__':
    pass





















