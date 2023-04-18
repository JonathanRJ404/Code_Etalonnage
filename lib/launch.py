import json
from datetime import date

def launch():
    lastname = input("lastname:")
    firstname = input("firstname:")
    organisation = input("organisation:")
    latitude = float(input("latitude (default: -20.9): ") or "-20.9")
    longitude = float(input("longitude (default: 55.48): ") or "55.48")
    altitude = float(input("altitude (default:90) ") or "90")
    TZ = int(input("TimeZone (default: 4): ") or "4")

    model = input("model:")
    serial_num = input("serial_num:")
    sensi_ghi_old = float(input("sensi_ghi_old (default: 1):") or "1")
    sensi_dhi_old = float(input("sensi_dhi_old (default: 1):") or "1")
    mode = input("mode:")   
    reference = input("reference:")
    date.today()
    filename = './param/param_'+str(date.today().year)+str(date.today().month)+str(date.today().day)+'_'+model+'_'+serial_num+'.json'

    link = input("Influxdb link: ") or "http://localhost:8086"
    bucket = input("bucket: ")
    org = input("org: ")
    token = input("token: ")

    data = {
        "Location":{
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "TZ": TZ
        },
        "operator":{
            "lastname":lastname,
            "firstname":firstname,
            "org":organisation
        },
        "InfluxDB":{
            "link":link,
            "bucket":bucket,
            "org":org,
            "token":token
        },
        "Device":{
            "model":model,
            "serial_num":serial_num,
            "sensi_ghi_old": sensi_ghi_old,
            "sensi_dhi_old": sensi_dhi_old,
            "mode":mode,
            "reference":reference
        }
    }



    with open(filename, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)

    return filename