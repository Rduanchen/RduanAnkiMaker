import requests
from bs4 import BeautifulSoup
import io
class YahooDic:
    def __init__(self,word):
        self.url = "https://tw.dictionary.search.yahoo.com/search?p="
        self.word = word
        self.reply = {
            "Vol": word,
            "KK": "",
            "Translate": [],
            "Type": [],
            "Sentence": [],
            "Pair": {},
            "Media": io.BytesIO()
        }
        self.soup = None
        self.get_data()
    def get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        url = self.url + self.word
        response = requests.get(url, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')
    def Vol_Type(self):
        Vol_Type = self.soup.find_all('div', class_='pos_button fz-14 fl-l mr-12')
        re = []
        for i in Vol_Type:
            re.append(i.text)
        self.reply["Type"] = re
        return re
    def Translation(self):
        Translate_Text = self.soup.find_all('div', class_='dictionaryExplanation')
        re = []
        for i in Translate_Text:
            re.append(i.text)
        self.reply["Translate"] = re
        return re
    def Sentence(self,limit=5,WithChinese=True):
        Sentence = self.soup.find_all('span', class_='d-b fz-14 fc-2nd lh-20')
        re = []
        limit = -1 if limit == "end" else limit
        cnt = 0
        for i in Sentence:
            if limit == cnt:
                break
            re.append(i.text)
            cnt += 1
        if WithChinese == False:
            for i in range(len(re)):
                S = ""
                for j in range(len(re[i])):
                    if ord(re[i][j]) < 127:
                        S += re[i][j]
                re[i] = S
        self.reply["Sentence"] = re
        return re
    def Type_Vol_Pair(self):
        type = self.Vol_Type()
        trans= self.Translation()
        re = {}
        for i in range(len(type)):
            re[type[i]] = trans[i]
        self.reply["Pair"] = re
        return re
    def KK(self):
        KK = self.soup.find('div', class_='dictionaryWordCard')
        KK = KK.find_all('div', class_='compList')
        self.reply["KK"] = KK[0].text
        return KK[0].text
    def PronunceUrl(self):
        return "https://s.yimg.com/bg/dict/dreye/live/m/{}.mp3".format(self.word)
    def Pronunce(self,download=False):
        url = "https://s.yimg.com/bg/dict/dreye/live/m/{}.mp3".format(self.word)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.reply["Media"] = io.BytesIO(response.content)
                if download == True:
                    with open("{}.mp3".format(self.word), "wb") as f:
                        f.write(response.content)
                print("下載成功")
            else:
                print("無法下載文件，錯誤碼:", response.status_code)
        except Exception as e:
            print("下載時出錯", str(e))
            self.reply["Media"] = None
    def PronunceContent(self):
        url = "https://s.yimg.com/bg/dict/dreye/live/m/{}.mp3".format(self.word)
        try:
            response = requests.get(url)
            if response.status_code == 200:            
                return response.content
            else:             
                print("無法下載文件，錯誤碼:", response.status_code)
                return None
        except Exception as e:
            print("下載時出錯", str(e))
            return None
    def get_All(self,limit=5,SentenceWithChinese=True):
        self.Vol_Type()
        self.Translation()
        self.Sentence(limit=limit,WithChinese=SentenceWithChinese)
        self.Type_Vol_Pair()
        self.KK()
        return self.reply
if __name__ == "__main__":
    y = YahooDic("hate")
    print(y.Type_Vol_Pair())        