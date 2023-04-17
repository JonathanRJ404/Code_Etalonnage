import pandas as pd
import json
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS


def csvtoinflux(file_json, tab):

    with open(file_json) as json_data:
        data_dict = json.load(json_data)
    
    tab = tab.reset_index()
    # You can generate a Token from the "Tokens Tab" in the UI
    token = data_dict['InfluxDB']['token']
    org = data_dict['InfluxDB']['org']
    bucket = data_dict['InfluxDB']['bucket']
    link = data_dict['InfluxDB']['link']

    client = InfluxDBClient(url=link, token=token)

    write_api = client.write_api(write_options=ASYNCHRONOUS)

    data_ghi = []
    data_dhi = []
    erreur_ghi = []
    erreur_dhi = []
    for i in range(len(tab)):
        a = "SPN1,mesures=irradiance GHI=" + str(tab['GHI_test'][i])+" "+str(pd.to_datetime(tab['TIMESTAMP'][i]).value)
        data_ghi.append(a)
        b = "SPN1,mesures=irradiance DHI=" + str(tab['DHI_test'][i])+" "+str(pd.to_datetime(tab['TIMESTAMP'][i]).value)
        data_dhi.append(b)
        c = "SPN1,mesures=irradiance erreur_GHI=" + str(tab['erreur_ghi'][i])+" "+str(pd.to_datetime(tab['TIMESTAMP'][i]).value)
        erreur_ghi.append(c)
        d = "SPN1,mesures=irradiance erreur_DHI=" + str(tab['erreur_dhi'][i])+" "+str(pd.to_datetime(tab['TIMESTAMP'][i]).value)
        erreur_dhi.append(d)

    write_api.write(bucket, org, [data_ghi, data_dhi, erreur_ghi, erreur_dhi])
