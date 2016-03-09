# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION=2
MEMORY=2048
CPU_COUNT = 4
IOAPIC = "on"
PROJECT_NAME = "toolbox"
IP_ADDRESS = "192.168.33.100"
EMAIL="toolbox@localhost"

$provision = <<SCRIPT
echo "Europe/Amsterdam" > /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

export DEBIAN_FRONTEND="noninteractive"
echo "mysql-apt-config mysql-apt-config/select-server select mysql-5.6" | debconf-set-selections
echo "mysql-apt-config mysql-apt-config/repo-distro string debian" | debconf-set-selections
echo "mysql-apt-config mysql-apt-config/repo-codename string jessie" | debconf-set-selections

wget --quiet http://dev.mysql.com/get/mysql-apt-config_0.6.0-1_all.deb
dpkg -i mysql-apt-config_0.6.0-1_all.deb
#echo 'deb http://repo.mysql.com/apt/debian/ jessie mysql-5.6' >> /etc/apt/sources.list.d/mysql.list
rm -f mysql-apt-config_0.6.0-1_all.deb

apt-get update

apt-get install -y \
    mysql-community-server \
    libmysqlclient-dev \
    python \
    python-dev \
    python-pip \
    libjpeg-dev \
    libpng-dev \
    ufw

mysql -u root -e 'create database `toolbox-dev`'
mysqladmin password "root"

ufw allow 22
ufw allow 3306
ufw allow 80
ufw --force enable

pip install --quiet virtualenv
virtualenv /toolboxenv
source /toolboxenv/bin/activate
cd /toolbox/
pip install --quiet -r requirements.txt
logdir=/toolbox/toolbox/logs
if [ ! -d "$logdir" ]; then
    mkdir $logdir
fi
python manage.py syncdb --noinput
python manage.py migrate toolbox --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser --username toolbox --email $1

cat > /lib/systemd/system/toolbox.service <<EOF
[Unit]
Description=Toolbox DEV server
After=network.target
Requires=mysql.service

[Service]
Type=simple
KillMode=process
RemainAfterExit=no
Restart=always
RestartSec=20
ExecStart=/toolboxenv/bin/python2 /toolbox/manage.py runserver 0.0.0.0:80 --insecure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable toolbox.service
systemctl start toolbox.service
SCRIPT


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = "debian/jessie64"

    config.vm.provider :virtualbox do |vb|
        vb.customize ["modifyvm", :id, "--memory", MEMORY]
        vb.customize ["modifyvm", :id, "--cpus", CPU_COUNT]
        vb.customize ["modifyvm", :id, "--ioapic", IOAPIC]
    end

    config.vm.box_check_update = true

    config.hostmanager.enabled = true
    config.hostmanager.manage_host = true
    config.vm.define PROJECT_NAME do |node|
        node.vm.hostname = PROJECT_NAME + ".local"
        node.vm.network :private_network, ip:  IP_ADDRESS
    end
    config.vbguest.auto_update = true
    config.vbguest.no_remote = false
    config.vm.synced_folder ".", "/vagrant/", disabled: true
    config.vm.synced_folder ".", "/toolbox/", type: "virtualbox"
    config.vm.provision "shell" do |s|
        s.inline = $provision
        s.args   = [EMAIL]
    end
end
