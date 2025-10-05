import sys
sys.path.append('../lib')
from getToken import getToken
from utilities import Utility
import os
import json
from datetime import datetime
from argo_requests import sendArgoRequest

class ArgoClient():

    def __init__(self, schoolCode, username, password, configPath, save_login=True):

        self.account_credentials = {
            "schoolCode": schoolCode,
            "username": username,
            "password": password
            }

        self.configPath = configPath

        self.saveLogin = save_login


        self.data_aggiorna_data = ""

        self.token =  { "access_token": "", "expires_at": "undefined", "id_token": "", "refresh_token": "", "scope": "openid offline profile user.roles argo", "token_type": "bearer" }

        self.utilities = Utility(self)


    async def login(self):

        self.token = await getToken(self.account_credentials)

        if not self.saveLogin:
            return

        if not os.path.exists(self.configPath):
            os.makedirs(self.configPath)
            self._write_token_file()
        else:
            token_file = self._get_token_file_path()
            if os.path.exists(token_file):
                with open(token_file, 'r', encoding='utf8') as f:
                    self.token = json.load(f)

                if self.token.get("expires_at") and self._is_token_expired(self.token["expires_at"]):
                    new_token = await self.utilities.refresh_token()
                    if not new_token:
                        self.token = await getToken(self.account_credentials)
                        self._write_token_file()
                        if not await self.attempt_access_token():
                            self.token = await getToken(self.account_credentials)
                            self._write_token_file
                        else:
                            self.token = await getToken(self.account_credentials)
                            self._write_token_file




    async def send_argo_request(self,path, method, parse_body= True, body=None, headers=None):

        req = await sendArgoRequest(self, path, method, body, headers, parse_body)

        return  req



    async def get_profile(self):
        req = await self.send_argo_request("/profilo", "GET", True)
        return req.get('response')

    async def attempt_access_token(self):
        req = await self.send_argo_request(
            "/login", "POST", False,
            json.dumps({
                "lista-opzioni-notifiche": "{}",
                "lista-x-auth-token": "[]",
                "clientID": "d8MtQX5fR3yS9I7k-5OXUs:APA91bErrU-H7wGQ8yLastE_xS2JHDrVrfReRY2mnWQ9aVd-ohWYDTSLVRrKUsO2-25mBN1aduh5sPnZjFstg0Ixqiuoh5wCC38BB6NEveqWI_d6ZpM5DN3nvyVS8vDtwLS9caWeCmEK"
            })
        )
        if req.get('status') == 401:
            return False
        return True


    def _get_token_file_path(self):
        return os.path.join(
            self.configPath,
            f"{self.account_credentials['schoolCode']}{self.account_credentials['username']}.json"
        )

    def _write_token_file(self):
        token_file = self._get_token_file_path()
        with open(token_file, 'w', encoding='utf8') as f:
            json.dump(self.token, f)

    def _is_token_expired(self, expires_at):
        try:
            expiry = datetime.fromisoformat(expires_at)
            return expiry.timestamp() < datetime.now().timestamp()
        except Exception:
            return True







