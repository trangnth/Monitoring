#!/usr/bin/python36

# Delete VMs deleted in whisper database 

import logging
import os
import shutil

from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

loader = loading.get_plugin_loader('password')

# Khai bao path luu tru cua compute2 tren whisper va ip controller
list_compute = ['compute1', 'compute2']
whisper_path = '/var/lib/carbon/whisper/collectd/'

# IP controller
ip_con = '192.168.40.11' 
ssl = 'http'

auth_url = "{0}://{1}:5000/v3".format(ssl, ip_con)
# Thong tin xac thuc project admin
username = "admin"
password = "Welcome123"
project_name = "admin"
user_domain_id = "default"
project_domain_id = "default"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# List uuid VMs
try:
    auth = loader.load_from_options(auth_url=auth_url, username=username, password=password, project_name=project_name, user_domain_id=user_domain_id, project_domain_id=project_domain_id)
    sess = session.Session(auth=auth)
    nova = client.Client(2, session=sess)

    vms = nova.servers.list(search_opts={'all_tenants': 1})

    list_uuid = []

    for vm in vms:
        list_uuid.append(vm._info['id'])
except Exception as e:
    logger.critical(e)


# List database whisper
logger.info("Start check VMs deleted.")
for com in list_compute:
    list_vm = []
    path = whisper_path + com
    
    list_vm = os.listdir(path)
#    list_compute.remove(com)
    
    diff = set(list_vm) - set(list_uuid)
    for i in diff:
        logger.info("Delete " + i + " from " + com)
        shutil.rmtree(os.path.join(path, i))
