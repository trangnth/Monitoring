# Check_mk check docker host

**Bước 1**: Tải plugin về agent

* Trên agent thực hiện tải plugin từ phía server về

```sh
cd /usr/lib/check_mk_agent/plugins
wget http://192.168.40.129/monitoring/check_mk/agents/plugins/mk_docker_node
chmod +x mk_docker_node
```
* Lưu ý thay địa chỉ IP và tên site cho của checkmk server cho phù hợp với cấu hình của mình

**Bước 2**:

* Khởi động lại xinetd

```sh
systemctl restart xinetd 
```

* Kiểm tra lại trên agent 

```sh
[root@trang-40-124 plugins]# check_mk_agent | grep docker
(root,594576,69360,00:00:00/27:59,9034) /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
(root,112712,968,00:00:00/00:00,13621) grep --color=auto docker
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
docker0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
[docker0]
<<<docker_node_info:sep(58)>>>
| Init Binary: docker-init
| Docker Root Dir: /var/lib/docker
| Registry: https://index.docker.io/v1/
<<<docker_node_disk_usage:sep(0)>>>
<<<docker_node_images>>>
                "MergedDir": "/var/lib/docker/overlay2/192de0ec36ce2a788cf36d2fe23de95a4f66fed543601afe8c3297ff42aeda58/merged",
                "UpperDir": "/var/lib/docker/overlay2/192de0ec36ce2a788cf36d2fe23de95a4f66fed543601afe8c3297ff42aeda58/diff",
                "WorkDir": "/var/lib/docker/overlay2/192de0ec36ce2a788cf36d2fe23de95a4f66fed543601afe8c3297ff42aeda58/work"
<<<docker_node_network:sep(0)>>>
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
```

**Bước 3**: Kiểm tra trên web của checkmk server 

<img src="../img/81.png">





