#### Sử dụng script xóa db

Cài đặt python 3.6 trên CentOS 7

	sudo yum install python36 -y 
	sudo yum install python36-setuptools -y 
	sudo easy_install-3.6 pip 

<!-- Mặc định python 2,7 sẽ được cài đặt, và khi cài pip sẽ là pip của bản python 2.7, nên khi cài python 3.6 vào thì tôi sẽ đặt một cái alias ở `~/.bashrc` cho tiện sử dụng (có thể không cần tới bước này khi chưa cài pip nào khác):

```sh
$ vim ~/.bashrc
...
alias pip36='/usr/local/bin/pip3.6'
``` -->

Sử dụng python3.6

	pip3.6 install keystoneauth
	pip3.6 install python-openstackclient

Test script với lệnh:

	python36 graphite_remove_db.py

Hoặc dùng shebang thì thêm quyền thực thi cho file

	chmod +x graphite_remove_db.py
	./graphite_remove_db.py

#### Tạo crontab chạy script 1 tuần 1 lần

Thêm dòng sau vào file `/etc/contab` để chạy scrpit mỗi tuần một lần vào lúc 8h05 ngày chủ nhật

	5 8 * * 0 root python36 /root/graphite_remove_db.py >> /var/log/graphite-web/deletedbgraphite.log 2>&1


#### Command get module pip 

```sh
mkdir python
cd python
pip download keystoneauth
pip download python-openstackclient
```

Khi đó các gói sẽ được download nằm tại thư mục này:

```sh
[root@trang-68-110 python]# ls
appdirs-1.4.3-py2.py3-none-any.whl                keystoneauth-0.5.0-py2.py3-none-any.whl            python_cinderclient-4.2.1-py2.py3-none-any.whl
asn1crypto-0.24.0-py2.py3-none-any.whl            keystoneauth1-3.15.0-py2.py3-none-any.whl          python_glanceclient-2.16.0-py2.py3-none-any.whl
attrs-19.1.0-py2.py3-none-any.whl                 msgpack-0.6.1-cp36-cp36m-manylinux1_x86_64.whl     python_keystoneclient-3.20.0-py2.py3-none-any.whl
Babel-2.7.0-py2.py3-none-any.whl                  munch-2.3.2.tar.gz                                 python_novaclient-14.2.0-py2.py3-none-any.whl
certifi-2019.6.16-py2.py3-none-any.whl            netaddr-0.7.19-py2.py3-none-any.whl                python_openstackclient-3.19.0-py2.py3-none-any.whl
cffi-1.12.3-cp36-cp36m-manylinux1_x86_64.whl      netifaces-0.10.9-cp36-cp36m-manylinux1_x86_64.whl  pytz-2019.2-py2.py3-none-any.whl
chardet-3.0.4-py2.py3-none-any.whl                openstacksdk-0.32.0-py2.py3-none-any.whl           PyYAML-5.1.2.tar.gz
cliff-2.15.0-py2.py3-none-any.whl                 osc_lib-1.13.0-py2.py3-none-any.whl                requests-2.22.0-py2.py3-none-any.whl
cmd2-0.9.15-py3-none-any.whl                      oslo.config-6.11.0-py2.py3-none-any.whl            requestsexceptions-1.4.0-py2.py3-none-any.whl
colorama-0.4.1-py2.py3-none-any.whl               oslo.i18n-3.23.1-py2.py3-none-any.whl              rfc3986-1.3.2-py2.py3-none-any.whl
cryptography-2.7-cp34-abi3-manylinux1_x86_64.whl  oslo.serialization-2.29.1-py2.py3-none-any.whl     setuptools-41.0.1-py2.py3-none-any.whl
debtcollector-1.21.0-py2.py3-none-any.whl         oslo.utils-3.41.0-py2.py3-none-any.whl             simplejson-3.16.0.tar.gz
decorator-4.4.0-py2.py3-none-any.whl              os_service_types-1.7.0-py2.py3-none-any.whl        six-1.12.0-py2.py3-none-any.whl
dogpile.cache-0.7.1.tar.gz                        pbr-5.4.2-py2.py3-none-any.whl                     stevedore-1.30.1-py2.py3-none-any.whl
idna-2.8-py2.py3-none-any.whl                     prettytable-0.7.2.tar.bz2                          urllib3-1.25.3-py2.py3-none-any.whl
iso8601-0.1.12-py2.py3-none-any.whl               pycparser-2.19.tar.gz                              warlock-1.3.3.tar.gz
jmespath-0.9.4-py2.py3-none-any.whl               pyOpenSSL-19.0.0-py2.py3-none-any.whl              wcwidth-0.1.7-py2.py3-none-any.whl
jsonpatch-1.24-py2.py3-none-any.whl               pyparsing-2.4.2-py2.py3-none-any.whl               wrapt-1.11.2.tar.gz
jsonpointer-2.0-py2.py3-none-any.whl              pyperclip-1.7.0.tar.gz
jsonschema-3.0.2-py2.py3-none-any.whl             pyrsistent-0.15.4.tar.gz
```

Thực hiện cài đặt:

```sh
pip install --no-index --find-links /tmp/python python_openstackclient-3.19.0-py2.py3-none-any.whl
pip install --no-index --find-links /tmp/python keystoneauth-0.5.0-py2.py3-none-any.whl
```

Nén và giải nén
```
tar -zcvf python.tar.gz python/
tar xvzf python.tar.gz
```

Liệt kê các file có trong thư mục nén

```sh
tar -tf  python.tar.gz
```

 cliff!=2.9.0,>=2.8.0