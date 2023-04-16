sudo apt update
sudo apt install libtool dh-autoreconf libpcap-dev libghc-bzlib-dev flex autoconf pkgconf bison-y
git clone https://github.com/phaag/nfdump

cd nfdump
./autogen.sh

./configure --enable-sflow --enable-readpcap --enable-nfpcapd
make
sudo make install
sudo ldconfig