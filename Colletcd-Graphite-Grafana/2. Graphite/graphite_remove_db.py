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
whisper_path = '/var/lib/carbon/whisper/collectd/compute2/'
ip_con = '192.168.40.11'
ssl = 'http'

auth_url = "{0}://{1}:5000/v3".format(ssl, ip_con)
username = "admin"
password = "Welcome123"
project_name = "admin"
user_domain_id = "default"
project_domain_id = "default"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
loger = logging.getLogger(__name__)

# List uuid VMs
auth = loader.load_from_options(auth_url=auth_url, username=username, password=password, project_name=project_name, user_domain_id=user_domain_id, project_domain_id=project_domain_id)
sess = session.Session(auth=auth)
nova = client.Client(2, session=sess)

vms = nova.servers.list(search_opts={'all_tenants': 1})

list_uuid = []

for vm in vms:
	list_uuid.append(vm._info['id'])


# List database whisper
list_dir = os.listdir(whisper_path)
list_dir.remove("compute2")


diff = set(list_dir) - set(list_uuid)

print ("Removing...")
for i in diff:
    print ("  ", i)
    shutil.rmtree(os.path.join(whisper_path, i))

print("Finished.")