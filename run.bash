mkdir RduanAnki
cd ./RduanAnki
python3 -m venv V1
source V1/bin/activate
git clone git@github.com:Rduanchen/RduanAnkiMaker.git
cd RduanAnkiMaker
pip install -r requirements.txt
pip install pyinstaller
mkdir dist
pyinstaller --distpath dist --noconfirm --onedir --console --add-data "./templates;templates/"  "./App.py"
