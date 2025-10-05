from Constants import ClientId, redirectUri
from encryptCodeVerifiers import encryptcodeVerifier as ec
from randomstring import random_string as random
import urllib.parse
import asyncio

async def generateLoginLink():
    scopes = ["openid", "offline", "profile", "user.roles", "argo"]
    codeVerifier = random(43)
    state = random(22)
    nonce = random(22)
    challenge = await ec(codeVerifier)
    query_params = {
        "redirect_uri": redirectUri,
        "client_id": ClientId,
        "response_type": "code",
        "prompt": "login",
        "state": state,
        "nonce": nonce,
        "scope": " ".join(scopes),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }

    url = f"https://auth.portaleargo.it/oauth2/auth?{urllib.parse.urlencode(query_params)}"

    return url, challenge, codeVerifier


if __name__ == '__main__':
    pass




