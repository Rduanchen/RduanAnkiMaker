from flask import Flask, render_template, request, jsonify, send_file
import os
import zipfile
import io
import subprocess
from threading import Timer
from CambridgeParser import Cambridge as Cambridge
from YahooDic import YahooDic as YahooDic
from AnkiHtmlMaker import AnkiHtml as AH

current_path = os.path.dirname(__file__)
os.chdir(current_path)

zip_buffer_download = io.BytesIO()

MediaSetting = None
MediaType = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Main.html')

@app.route('/api', methods=['POST'])
def api():
    global MediaSetting, MediaType, zip_buffer_download
    zip_buffer_download = io.BytesIO()
    data = request.json
    Reply = []
    MediaSetting = data["Settings"]["Media"]
    MediaType = data["Settings"]["MediaType"]
    for Vol in data["Vols"]:
        if Vol == "": continue
        try:
            ReplyData = {"Vol": Vol}
            Ya = YahooDic(Vol)
            Cam = Cambridge(Vol)
            Limit = data["Settings"]["DefinationLimit"]
            if data["Settings"]["Defination"] == "Cambridge":
                temp = Cam.Defination(data["Settings"]["DefinationLimit"])
                out = ""
                cnt = 1
                for i in temp:
                    out += str(cnt) + ". " + i + "\n"
                    cnt += 1
                ReplyData["Defination"] = out
            Limit = data["Settings"]["TranslateLimit"]
            if data["Settings"]["Translate"] == "Cambridge":
                temp = Cam.Vol_Type_Pair(data["Settings"]["TranslateLimit"])
                out = ""
                for i in temp:
                    out += str(i) + "\n"
                    for j in temp[i]:
                        out += j
                    out += "\n"
                ReplyData["Translate"] = out
            elif data["Settings"]["Translate"] == "Yahoo":
                temp = Ya.Type_Vol_Pair()
                out = ""
                for i in temp:
                    out += str(i) + "\n"
                    for j in temp[i]:
                        out += j
                    out += "\n"
                ReplyData["Translate"] = out
            Limit = data["Settings"]["SentenceLimit"]
            if data["Settings"]["Sentence"] == "Cambridge":
                temp = Cam.Sentence(data["Settings"]["SentenceLimit"])
                temp = str(temp).replace("[", "").replace("]", "").replace("'", "").replace(",", "").replace("\\n", "\n").replace("  ", "").replace('"', '')
                ReplyData["Sentence"] = temp
            elif data["Settings"]["Sentence"] == "Yahoo":
                temp = Ya.Sentence(data["Settings"]["SentenceLimit"])
                temp = str(temp).replace("[", "").replace("]", "").replace("'", "").replace(",", "\n").replace("\\n", "\n").replace("  ", "").replace('"', '')
                ReplyData["Sentence"] = temp
            ReplyData["Media"] = Ya.PronunceUrl()

            if MediaSetting:
                with zipfile.ZipFile(zip_buffer_download, 'a', zipfile.ZIP_DEFLATED, False) as z:
                    mp3_content = Ya.PronunceContent()
                    if mp3_content:
                        z.writestr("RduanAnki{}.mp3".format(Vol), mp3_content)
            
            if data["Settings"]["KK"] == "Cambridge":
                ReplyData["KK"] = Cam.KK()
            elif data["Settings"]["KK"] == "Yahoo":
                ReplyData["KK"] = Ya.KK()
            Reply.append(ReplyData)
        except Exception as e:
            Reply.append({"Vol": Vol, "Defination": "No Data", "Translate": "No Data", "Sentence": "No Data", "Media": "No Data"})
    return jsonify(Reply)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    Text = AH()
    for i in data:
        Text.H2_tag(i["Vol"])
        if MediaSetting:
            if MediaType:
                Text.AnkiSoundTag(i["Vol"])
            else:
                Text.AudioTag(i["Media"])
        Text.gap()
        Text.div_start()
        Text.H3_tag("英文定義")
        Text.p_tag(i["Defination"].replace("\n", "<br>"))
        Text.H3_tag("中文翻譯")
        Text.p_tag(i["Translate"].replace("\n", "<br>"))
        Text.H3_tag("造句")
        Text.p_tag(i["Sentence"].replace("\n", "<br>"))
        Text.div_end()
        Text.next_word()
    output = io.BytesIO()
    output.write(Text.get_result().encode('utf-8'))
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="AnkiCardOutput.txt")

@app.route('/api/media', methods=['GET'])
def download_media():
    zip_buffer_download.seek(0)
    return send_file(
        zip_buffer_download,
        as_attachment=True,
        download_name='Media.zip',
        mimetype='application/zip'
    )
def oppen_browser():
    subprocess.Popen(['start', '', 'http://127.0.0.1:5990'], shell=True)
if __name__ == '__main__':
    Timer(1, oppen_browser).start()
    app.run(port=5990)
