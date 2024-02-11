#!/bin/bash
mkdir build && cd build
git clone https://github.com/ufal/korektor.git
cd korektor/src
make exe
mv korektor_server ../../..
cd ../../..
rm -rf build

mkdir data
cd data
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1460{/korektor-czech-130202.zip}
unzip korektor-czech-130202.zip
mv korektor-czech-130202 korektor_model
rm korektor-czech-130202.zip
cd ..
