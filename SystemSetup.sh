sudo apt-get update & sudo apt-get upgrade
sudo apt-get install -y python3 python3-pip git autoconf automake libtool curl make g++ unzip
sudo pip3 install flask
sudo pip3 install flask_login
hostname -f > hostname.txt
sudo apt-get install -y mysql-server
sudo mysql_secure_installation
sudo ldconfig
cd ~
git clone http://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j8
make check
sudo make install
sudo ldconfig
cd python
cd python ./setup.py install
sudo ldconfig
sudo pip3 install --upgrade pip
sudo pip3 install mysql-connector


