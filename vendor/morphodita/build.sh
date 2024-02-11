#!/bin/bash

mkdir build && cd build || exit
git clone https://github.com/ufal/morphodita.git
cd morphodita/src || exit
make server
mv rest_server/morphodita_server ../../..
cd ../../..
rm -rf build

mkdir data && cd data || exit
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4794{/czech-morfflex2.0-pdtc1.0-220710.zip}
unzip czech-morfflex2.0-pdtc1.0-220710.zip
mv czech-morfflex2.0-pdtc1.0-220710 morphodita_model
rm -rf czech-morfflex2.0-pdtc1.0-220710
rm czech-morfflex2.0-pdtc1.0-220710.zip
cd .. || exit
