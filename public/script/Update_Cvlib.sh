apt update && apt install git
rm -rf /home/data/cvpack2
git clone https://github.com/2742195759/cvpack2
cd cvpack2
python setup.py install

git clone https://github.com/2742195759/cvpack2_model
