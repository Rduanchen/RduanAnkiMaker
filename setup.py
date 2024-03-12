from setuptools import setup

APP = ['App.py']  # 將 your_flask_app.py 替換為你的 Flask 應用程式的檔案名稱
DATA_FILES = ['templates']  # 將 templates 替換為你的應用程式的模板資料夾名稱
OPTIONS = {
    'argv_emulation': True,
    'packages': ['flask', 'requests', 'bs4', 'lxml'],  # 將 flask 替換為你的 Flask 應用程式所需的套件名稱

}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)