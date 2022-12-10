apt-get update -y
hostnamectl set-hostname slave

echo "slaveIP slave" >> /etc/hosts
echo "masterIP master" >> /etc/hosts

swapoff -a

wget -qO- https://get.docker.com/ | sh

modprobe br_netfilter
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

sysctl --system
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

apt-get update
apt-get install -y kubelet kubeadm kubectl

sleep 30 
cp /home/ubuntu/10-kubeadm.conf /etc/systemd/system/kubelet.service.d/ 
sleep 10
systemctl daemon-reload
sleep 30


rm /etc/containerd/config.toml
systemctl restart containerd
