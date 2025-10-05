import sys
sys.path.append('../lib')
from getToken import getToken
import asyncio
import requests
from datetime import datetime, timezone
from Constants import baseApiURL


async def sendArgoRequest(client, path, method, body, headers, parseBody= True):
        default_headers = {
            "Authorization": f"Bearer {client.token['access_token']}",
            "argo-client-version": "9.99.9",
            "content-type": "application/json; charset=utf-8",
            "x-auth-token": "",
            "x-cod-min": client.account_credentials['schoolCode'],
            "x-date-exp-auth": (
                datetime.fromisoformat(client.token['expires_at'][:-1]).isoformat()
                if client.token.get('expires_at') else
                datetime.now(timezone.utc).isoformat()
            ),
        }

        if headers:
            default_headers.update(headers)

        request_kwargs = {
            "headers": default_headers,
            }

        if body:
            request_kwargs["data"] = body

        url = baseApiURL + path

        response = requests.request(method, url, **request_kwargs)


        if response.status_code == 401 and "oauth" not in path:
            new_token = client.utilities.refresh_token()
            if not new_token:
                client.token = await getToken(client.account_credentials)
                default_headers["Authorization"] = f"Bearer {client.token['access_token']}"
                request_kwargs["headers"] = default_headers
                response = requests.request(method, url, **request_kwargs)


        return_data = {
            "response": response.json() if parseBody else None,
            "status": response.status_code,
            "fetchResponse": response
            }

        return return_data
