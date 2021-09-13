#TODO: insert warnings before using rm where they are prompted with a (y/n) question
cd ~/Documents/GitHub/bgmc/python/lib
cp lib_care ~/Documents/GitHub/care/notebooks
rm -r lib
mv ~/Documents/GitHub/care/notebooks/lib_care ~/Documents/GitHub/care/notebooks/lib

#update care/lib as lib_care
cd ~/Documents/GitHub/bgmc/python/lib
cp lib_care ~/Documents/GitHub/care/notebooks
rm -r lib
mv ~/Documents/GitHub/care/notebooks/lib_care ~/Documents/GitHub/care/notebooks/lib

#update neurophysics with lib_care, yielding lib.lib_care
cp -r lib_care ~/Documents/GitHub/neurophysics/notebooks/lib
