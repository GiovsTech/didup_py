import asyncio
from Constants import ClientId, redirectUri
from getCode import getCode
from randomstring import random_string
import hashlib
import base64
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta, UTC
import secrets

async def getToken(credentials):

    code, code_challenge, code_verifier = await getCode(credentials)
    token_res_body = urlencode({

        "client_id": ClientId,

        "code" : code,

        "redirect_uri" : redirectUri,

        "code_verifier" : code_verifier,

        "grant_type": "authorization_code"

        })

    response = requests.post("https://auth.portaleargo.it/oauth2/token",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data=token_res_body)

    token_data = response.json()


    response.raise_for_status()


    expires_in = token_data.pop("expires_in")
    token_data["expires_at"] = (datetime.now(UTC) + timedelta(seconds=expires_in)).isoformat() + "Z"

    return token_data

if __name__ == '__main__':

    pass
