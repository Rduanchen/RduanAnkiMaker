from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import requests
from bs4 import BeautifulSoup
import os
import zipfile
import subprocess
from threading import Timer
import io

current_path = os.path.dirname(__file__)
os.chdir(current_path)

zip_buffer_download = io.BytesIO()

# 進入專案資料
app = Flask(__name__)

def H2_tag(text):
    return f"<h2>{text}</h2>"
def H3_tag(text):
    return f"<h3>{text}</h3>"
def p_tag(text):
    return f"<p>{text}</p>"
def br():
    return "<br>"
def hr():
    return "<hr>"
def AnkiSoundTag(src):
    src="RduanCard_"+src
    return f"[sound:RduanAnki{src}.mp3]"

def data2AnkiTxt(data,withmedia=False):
    # 原文會成為卡片正面，翻譯會成為卡片背面
    # 一個卡片一行，原文和翻譯用tab分隔
    AnkiText = '''
#separator:tab
#html:true
'''
    for i in data:
        try:
            AnkiText += H2_tag(i["Vol"])
            if withmedia:
                AnkiText += AnkiSoundTag(i["Vol"])
            AnkiText += '\t'
            AnkiText += '<div class="RduanCard">'
            AnkiText += p_tag(i["def"])
            for j in i["Translate"]:
                AnkiText += p_tag(j)
            AnkiText += H3_tag("造句")
            for k in i["Sentence"]:
                AnkiText += p_tag(k)
            AnkiText += '</div>'
            AnkiText += "\n"
        except:
            AnkiText += "查無資料\n"
            AnkiText += "\n"
    print(AnkiText)
    with open("AnkiCardOutput.txt", "w", encoding="utf-8") as f:
        f.write(AnkiText)
    return AnkiText

def EmptyFolder():
    # 清空media資料夾
    for root, dirs, files in os.walk('./media'):
        for file in files:
            os.remove(os.path.join(root, file))
    print("清空完成")

def MakeMP3File(word, zip_buffer):
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zipf:
        for i in word:
            url = "https://s.yimg.com/bg/dict/dreye/live/m/{}.mp3".format(i)
            try:
                # 發送 GET 請求獲取 MP3 文件
                response = requests.get(url)
                if response.status_code == 200:
                    # 將文件寫入 zip buffer 中
                    zipf.writestr("RduanAnki{}.mp3".format(i), response.content)
                    print("MP3 文件下載成功")
                else:
                    print("無法下載文件，錯誤碼:", response.status_code)
            except Exception as e:
                print("下載時出錯", str(e))
@app.route("/")
def MainPage():
    return render_template('./Main.html')

@app.route('/api/ankitxt', methods=['GET'])
def ankitxt():
    return send_from_directory(current_path, "AnkiCardOutput.txt", as_attachment=True)

def start_flask():
    # 启动 Flask 应用
    app.run()

@app.route('/api', methods=['POST'])
# 不含音訊檔案
def api():
    data = request.json
    res = {
        "Translate": [],
    }
    # 傳回英文翻譯
    appen_data = {
        "Vol": "",
        "Translate": [],
        "def": "",
        "Sentence": [],
    }
    for i in data["Vol"]:
        try:
            # Yahoo 翻譯: 詞性 + 翻譯
            url = url = 'https://tw.dictionary.search.yahoo.com/search?p={}'.format(i)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            Vol_Type = soup.find_all('div', class_='pos_button fz-14 fl-l mr-12')
            Translate_Text = soup.find_all('div', class_='dictionaryExplanation')
            for m in range(len(Translate_Text)):
                temp = "["+Vol_Type[m].text+"] "+Translate_Text[m].text
                appen_data["Translate"].append(temp)
            # ------分隔線------
                
            # Cambridge 翻譯: 英文解釋 + 例句
            url ='''https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'''.format(i)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            def_part = soup.find('div', class_='ddef_h') # 英文解釋區段
            def_text = def_part.find_all('div', class_='def ddef_d db') # 英文解釋
            for z in range(len(def_text)):
                x = def_text[z].find_all('a') # 取得所有的文字
                for e in range(len(x)):
                    appen_data["def"] += x[e].text + " "
                    
            Example_Text = soup.find('div', class_='def-body ddef_b') # 造句區段
            Sentences = Example_Text.find_all('span', class_='eg deg') # 所有造句
            sentence_limit=3 #造句最大值
            for y in range(len(Sentences)):
                if y<sentence_limit:
                    appen_data["Sentence"].append(Sentences[y].text)
                else:
                    break
            appen_data["Vol"] = i
            res["Translate"].append(appen_data)
            appen_data = {
                "Vol": "",
                "Translate": [],
                "def": "",
                "Sentence": [],
            }
        except:
            res["Translate"].append({
                "Vol": i,
                "Translate": "error",
            })
    a=data2AnkiTxt(res["Translate"])
    return jsonify(res) # 回傳翻譯結果

@app.route('/api/media', methods=['POST'])
# 下載media(含有音訊檔)
def media():
    data = request.json
    res = {
        "Translate": [],
    }
    # 傳回英文翻譯
    appen_data = {
        "Vol": "",
        "Translate": [],
        "def": "",
        "Sentence": [],
    }
    validate_word=[]
    for i in data["Vol"]:
        try:
            # Yahoo 翻譯: 詞性 + 翻譯
            url = url = 'https://tw.dictionary.search.yahoo.com/search?p={}'.format(i)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            Vol_Type = soup.find_all('div', class_='pos_button fz-14 fl-l mr-12')
            Translate_Text = soup.find_all('div', class_='dictionaryExplanation')
            for m in range(len(Translate_Text)):
                temp = "["+Vol_Type[m].text+"] "+Translate_Text[m].text
                appen_data["Translate"].append(temp)
            # ------分隔線------
                
            # Cambridge 翻譯: 英文解釋 + 例句
            url ='''https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'''.format(i)
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            def_part = soup.find('div', class_='ddef_h') # 英文解釋區段
            def_text = def_part.find_all('div', class_='def ddef_d db') # 英文解釋
            for z in range(len(def_text)):
                x = def_text[z].find_all('a') # 取得所有的文字
                for e in range(len(x)):
                    appen_data["def"] += x[e].text + " "
                    
            Example_Text = soup.find('div', class_='def-body ddef_b') # 造句區段
            Sentences = Example_Text.find_all('span', class_='eg deg') # 所有造句
            sentence_limit=3 #造句最大值
            for y in range(len(Sentences)):
                if y<sentence_limit:
                    appen_data["Sentence"].append(Sentences[y].text)
                else:
                    break
            appen_data["Vol"] = i
            validate_word.append(i) # 下載音訊使用
            res["Translate"].append(appen_data)
            appen_data = {
                "Vol": "",
                "Translate": [],
                "def": "",
                "Sentence": [],
            }
        except:
            res["Translate"].append({
                "Vol": i,
                "Translate": "error",
            })
    MakeMP3File(validate_word,zip_buffer_download)
    a=data2AnkiTxt(res["Translate"],withmedia=True)
    return jsonify(res) # 回傳翻譯結果


@app.route('/api/download',methods=['GET'])
def download():
    # 創建一個 BytesIO 對象來存儲壓縮後的音訊檔案
    # MakeMP3File(words, zip_buffer)
    zip_buffer_download.seek(0)  # 將游標移動到文件的開頭
    return send_file(
        zip_buffer_download,
        as_attachment=True,
        download_name='media.zip',
        mimetype='application/zip'
    )


# def oppen_browser():
#     # 打开浏览器
#     subprocess.Popen(['start', '', 'http:127.0.0.1:5990'], shell=True)
# if __name__ == '__main__':
#     Timer(1,oppen_browser).start()
#     app.run(port=5990)