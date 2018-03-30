import requests
from monitoring import system
import json

## TODO: 3. Juhul, kui matchib siis saadab selle edasi netdata serverile.
## TODO: 4. netdata server võtab selle vastu statsd plugini abiga

def collectData():

    pc = system
    data = {}
    ## CPU, Memory, Disk
    data['CPU'] = {}
    data['CPU']['percent'] = pc.get_cpu_usage()

    data['Memory'] = {}
    #data['Memory']['all'] = pc.get_mem_usage("all")
    data['Memory']['total'] = pc.get_mem_usage("total")
    data['Memory']['available'] = pc.get_mem_usage("available")
    data['Memory']['percent'] = pc.get_mem_usage("percent")
    data['Memory']['used'] = pc.get_mem_usage("used")
    data['Memory']['free'] = pc.get_mem_usage("free")

    data['Disk'] = {}
    #data['Disk']['all'] = pc.get_disk_usage("all")
    data['Disk']['total'] = pc.get_disk_usage("total")
    data['Disk']['percent'] = pc.get_disk_usage("percent")
    data['Disk']['used'] = pc.get_disk_usage("used")
    data['Disk']['free'] = pc.get_disk_usage("free")
    print(type(data))
    return data

def sendRequest(url):

    data = collectData()
    headers = {'api-key': '123123'}
    r = requests.post(url, json=data, headers=headers)
    print(r.status_code)


if __name__ == '__main__':
    url = "http://127.0.0.1:5000/api"
    sendRequest(url=url)
