import requests
from monitoring import system
import json


def collectData():

    pc = system
    data = {}
    ## CPU, Memory, Disk
    data['CPU'] = {}
    data['CPU']['percent'] = pc.get_cpu_usage()

    data['Memory'] = {}
    data['Memory']['all'] = pc.get_mem_usage("all")
    data['Memory']['total'] = pc.get_mem_usage("total")
    data['Memory']['available'] = pc.get_mem_usage("available")
    data['Memory']['percent'] = pc.get_mem_usage("percent")
    data['Memory']['used'] = pc.get_mem_usage("used")
    data['Memory']['free'] = pc.get_mem_usage("free")

    data['Disk'] = {}
    data['Disk']['all'] = pc.get_disk_usage("all")
    data['Disk']['total'] = pc.get_disk_usage("total")
    data['Disk']['percent'] = pc.get_disk_usage("percent")
    data['Disk']['used'] = pc.get_disk_usage("used")
    data['Disk']['free'] = pc.get_disk_usage("free")

    return json.dumps(data)

def sendRequest(url, data):

    url = 'https://api.github.com/some/endpoint'
    payload = {'some': 'data'}
    headers = {'content-type': 'application/json'}

    r = requests.post(url, data=json.dumps(payload), headers=headers)