from setuptools import setup

APP = ['App.py']  # 將 your_flask_app.py 替換為你的 Flask 應用程式的檔案名稱
DATA_FILES = [('templates', ['templates'])]  # 指定要包含的資料夾
OPTIONS = {
    'argv_emulation': True,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)