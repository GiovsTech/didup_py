from Client import ArgoClient
from datetime import datetime
import asyncio
import json

class Argo:
    def __init__(self, client):
        self.client = client
        self.profilo_selezionato = None

    async def get_dashboard(self):
        if not self.client.data_aggiorna_data:
            self.client.data_aggiorna_data = self.client.utilities.formatta_data_ultimo_aggiornamento(datetime(datetime.now().year, 9, 1))

        if not self.profilo_selezionato:
            raise Exception("Profilo non selezionato. Si prega di selezionare un profilo con il metodo client.argo.select_user()")

        body = {
            "dataultimoaggiornamento": self.client.data_aggiorna_data,
            "opzioni": '{"ORARIO_SCOLASTICO":true,"PAGELLINO_ONLINE":true,"VALUTAZIONI_PERIODICHE":true,"VALUTAZIONI_GIORNALIERE":true,"COMPITI_ASSEGNATI":true,"IGNORA_OPZIONE_VOTI_DOCENTE":true}'
        }

        headers = {
            "x-auth-token": self.profilo_selezionato['token']
        }

        resp = await self.client.send_argo_request("/dashboard/dashboard", "POST", True, body=json.dumps(body), headers=headers)
        return resp.get("response", {}).get("data")

    async def select_user(self, nome, cognome):
        profilo = None
        profili = await self.get_profili()
        to_find = f"{cognome.lower()} {nome.lower()}"
        for p in profili:
            if p["profilo"]["alunno"]["nominativo"].lower() in to_find:
                profilo = p
            if not profilo:
                raise Exception("Profilo non trovato")
        self.profilo_selezionato = profilo
        return profilo

    async def get_profili(self):
         body = {
            "lista-opzioni-notifiche": "{}",
            "lista-x-auth-token": "[]",
            "clientID": "d8MtQX5fR3yS9I7k-5OXUs:APA91bErrU-H7wGQ8yLastE_xS2JHDrVrfReRY2mnWQ9aVd-ohWYDTSLVRrKUsO2-25mBN1aduh5sPnZjFstg0Ixqiuoh5wCC38BB6NEveqWI_d6ZpM5DN3nvyVS8vDtwLS9caWeCmEK"
        }
         res = await self.client.send_argo_request("/login", "POST", True, body=json.dumps(body))
         profili = []
         for profile in  res['response'].get("data", []):
            profile_req = await self.client.send_argo_request("/profilo", "GET", True, headers={"x-auth-token": profile['token']})
            profile_data = profile_req.get("response", {}).get("data")
            profili.append({
                    "profilo": profile_data,
                    "token": profile['token']
                })
         return profili



    def aggiorna_data(self, data):
        formatted_date = self.client.utilities.formatta_data_ultimo_aggiornamento(data)
        body = { "dataultimoaggiornamento": formatted_date}
        req = self.client.send_argo_request("/dashboard/aggiorna_data", "POST", False, body=str(body))
        if req.get("status") == 200:
            self.client.data_aggiorna_data = formatted_date
            return True
        return False

