cd lib
git clone git@github.com:ufal/korektor.git
cd korektor/src
make exe
mv korektor_server ../..
cd ../../..
rm -rf lib/korektor

cd data
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1460{/korektor-czech-130202.zip}
unzip korektor-czech-130202.zip
mv korektor-czech-130202 korektor_model
rm korektor-czech-130202.zip
cd ..

cd lib
git clone git@github.com:ufal/morphodita.git
cd morphodita/src
make server
mv rest_server/morphodita_server ../..
cd ../../..
rm -rf lib/morphodita

cd data
curl --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-4794{/czech-morfflex2.0-pdtc1.0-220710.zip}
unzip czech-morfflex2.0-pdtc1.0-220710.zip
mv czech-morfflex2.0-pdtc1.0-220710/czech-morfflex2.0-220710.dict morphodita_model.dict
rm -rf czech-morfflex2.0-pdtc1.0-220710
rm czech-morfflex2.0-pdtc1.0-220710.zip
cd ..
