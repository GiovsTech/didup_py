import requests
from datetime import datetime, timedelta
import sys
sys.path.append('../lib')
from Constants import scopes, ClientId, redirectUri




class Utility():
    def __init__(self, client):
        self.client = client


    def formatta_data_ultimo_aggiornamento(self, data) -> str:
        return data.strftime("%Y-%m-%d %H:%M:%S")


    def refresh_token(self):

        url = "https://auth.portaleargo.it/oauth2/token"

        payload = {
            "refresh_token": self.client.token.get("refresh_token"),
            "grant_type": "refresh_token",
            "scope": scopes,
            "client_id": ClientId,
            "redirect_uri": redirect_uri
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }


        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 401:
            return None
        data = response.json()
        expires_in = data.pop("expires_in", None)
        if expires_in is not None:
                data["expires_at"] = datetime.now() + timedelta(seconds=expires_in)

        return data
