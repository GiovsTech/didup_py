import sys
sys.path.append('../utility')
from Argo import Argo
from Client import ArgoClient
import asyncio
from datetime import datetime, timedelta

client = ArgoClient("schoolcode", "username", "password", "path/to/config") ## HERE THE CREDENTIALS THE SCHOOL ADMINISTRATION HAS GIVEN TO YOU
argo = Argo(client)


### JUST AN EXAMPLE OF HOW THE LIBRARY WORKS:
### THIS CODE JUST PRINTS THE HOMEWORK THE STUDENT HAS TO DO FOR THE NEXT DAY

async def main():

    await argo.client.login()
    my_profilo = await argo.select_user("NAME", "SURNAME") ## HERE the student's name

    dashboard = await argo.get_dashboard()

    all_compiti = {}
    for x in dashboard["dati"]:
        if x["registro"]:

            for t in x["registro"]:
                all_compiti[t["materia"]] = t["compiti"]
    current_date = datetime.now()
    next_date = current_date + timedelta(days=1)
    next_day_date = next_date.date()

    for m in all_compiti.values():
        for n in m:
            if str(next_day_date) == n["dataConsegna"]:
                print(f"{list(all_compiti.keys())[list(all_compiti.values()).index(m)]}: " + f"{n["compito"]}")

asyncio.run(main())





