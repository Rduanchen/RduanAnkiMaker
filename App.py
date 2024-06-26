from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import subprocess
import threading
from threading import Timer, Thread
import io
from queue import Queue

# Warning:
# This code is generated by claude ai.

app = Flask(__name__)
current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)


zip_buffer_download = io.BytesIO()
zip_buffer_lock = threading.Lock()  # 創建一個鎖對象
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
sentence_limit = 3


def start_flask():
    app.run()

def get_tags(tag, text, className=""):
    return f'''<{tag} class="{ className }">{text}</{tag}>'''

def AnkiSoundTag(src):
    return f"[sound:RduanAnki{src}.mp3]"

def data2AnkiTxt(data, withmedia=False):
    AnkiText = "#separator:tab\n#html:true\n"
    for item in data:
        try:
            AnkiText += get_tags("h2", item["Vol"], "Vol")
            if withmedia:
                AnkiText += AnkiSoundTag(item["Vol"])
            AnkiText += "\t"
            AnkiText += '<div class="RduanCard">'
            AnkiText += get_tags("p", item["def"], "EngDefination")
            AnkiText += "".join([get_tags("div", translate, "ChineseDefination") for translate in item["Translate"]])
            AnkiText += '''<div class="SampleSentence">'''
            AnkiText += get_tags("h3", "造句", "SentenceTitle")
            AnkiText += "".join([get_tags("p", sentence, "Sentence") for sentence in item["Sentence"]])
            AnkiText += "</div>"
            AnkiText += '</div>\n'
        except:
            AnkiText += "查無資料\n\n"
    with open("AnkiCardOutput.txt", "w", encoding="utf-8") as f:
        f.write(AnkiText)
    return AnkiText

def EmptyFolder():
    for root, dirs, files in os.walk('./media'):
        for file in files:
            os.remove(os.path.join(root, file))
    print("清空完成")

def MakeMP3File(words, zip_buffer):
    with zip_buffer_lock:  # 加鎖
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zipf:
            for word in words:
                url = f"https://s.yimg.com/bg/dict/dreye/live/m/{word}.mp3"
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        zipf.writestr(f"RduanAnki{word}.mp3", response.content)
                        print(f"MP3 文件 {word} 下載成功")
                    else:
                        print(f"無法下載文件 {word}，錯誤碼: {response.status_code}")
                except Exception as e:
                    print(f"下載 {word} 時出錯: {str(e)}")
def get_translation(word, result_queue):
    # Yahoo 翻譯
    yahoo_url = f'https://tw.dictionary.search.yahoo.com/search?p={word}'
    yahoo_response = requests.get(yahoo_url, headers=headers)
    yahoo_soup = BeautifulSoup(yahoo_response.text, 'html.parser')
    vol_types = [tag.text for tag in yahoo_soup.find_all('div', class_='pos_button fz-14 fl-l mr-12')]

    translations = [f"{get_tags('p',vol_type,'Type')}{tag.text}" for vol_type, tag in zip(vol_types, yahoo_soup.find_all('div', class_='dictionaryExplanation'))]

    # Cambridge 翻譯
    cambridge_url = f'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{word}'
    cambridge_response = requests.get(cambridge_url, headers=headers)
    cambridge_soup = BeautifulSoup(cambridge_response.text, 'html.parser')
    definition = ' '.join([a.text for div in cambridge_soup.find('div', class_='ddef_h').find_all('div', class_='def ddef_d db') for a in div.find_all('a')])
    sentences = [tag.text for tag in cambridge_soup.find('div', class_='def-body ddef_b').find_all('span', class_='eg deg')][:3]

    result_queue.put({
        "Vol": word,
        "Translate": translations,
        "def": definition,
        "Sentence": sentences
    })

@app.route("/")
def MainPage():
    return render_template('./Main.html')

@app.route('/api/ankitxt', methods=['GET'])
def ankitxt():
    return send_from_directory(current_path, "AnkiCardOutput.txt", as_attachment=True)

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    words = data["Vol"]
    result_queue = Queue()
    threads = []

    for word in words:
        thread = Thread(target=get_translation, args=(word, result_queue))
        thread.start()
        threads.append(thread)

    res = {"Translate": []}
    for _ in words:
        try:
            res["Translate"].append(result_queue.get())
        except:
            pass

    for thread in threads:
        thread.join()

    data2AnkiTxt(res["Translate"])
    return jsonify(res)

@app.route('/api/media', methods=['POST'])
def media():
    data = request.json
    words = data["Vol"]
    result_queue = Queue()
    threads = []
    validate_words = []

    for word in words:
        thread = Thread(target=get_translation, args=(word, result_queue))
        thread.start()
        threads.append(thread)
        validate_words.append(word)

    res = {"Translate": []}
    for _ in words:
        try:
            res["Translate"].append(result_queue.get())
        except:
            pass

    for thread in threads:
        thread.join()

    MakeMP3File(validate_words, zip_buffer_download)
    data2AnkiTxt(res["Translate"], withmedia=True)
    return jsonify(res)

@app.route('/api/download', methods=['GET'])
def download():
    with zip_buffer_lock:  # 加鎖
        zip_buffer_download.seek(0)
        return send_file(
            zip_buffer_download,
            as_attachment=True,
            download_name='media.zip',
            mimetype='application/zip'
        )

def oppen_browser():
    subprocess.Popen(['start', '', 'http://127.0.0.1:5990'], shell=True)

if __name__ == '__main__':
    Timer(1, oppen_browser).start()
    app.run(port=5990)