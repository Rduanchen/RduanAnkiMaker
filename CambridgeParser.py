import requests
from bs4 import BeautifulSoup
class Cambridge:
    def __init__(self, w, limit=5):
        self.word = w
        self.reply = {
            "words": [],
            "sentences": [],
            "defination": []
        }
        self.soup = None
        self.limit = limit
        self.get_data()
    def get_data(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        url ='''https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'''.format(self.word)
        response = requests.get(url, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        return self.soup
    def KK(self): #FIXME
        KKs = self.soup.find_all('span', class_='pron dpron')
        re = []
        for i in range(2):
            s = ""
            for x in KKs[i]:
                s += x.text
            re.append(s)
        self.reply["KK"] = re = ["UK: "+re[0]] + [" US: "+re[1]]
        return re
    def Defination(self,limit=5): # English defination 英文解釋
        limit = -1 if limit == "end" else limit
        def_part = self.soup.find_all('div', class_='ddef_h')
        cnt = 0
        re = []
        for i in def_part:
            Defination = i.find_all('div', class_='def ddef_d db')
            s = ""
            if cnt == limit: break
            for x in Defination:
                s += x.text
            re.append(s)
            cnt += 1
        self.reply["defination"] = re
        return re

    def Translation(self,limit=5):
        limit = -1 if limit == "end" else limit
        def_part = self.soup.find_all('div', class_='def-body ddef_b')
        cnt = 0
        re = []
        for i in def_part:
            s = ""
            if cnt == limit:
                break
            Sentence = i.find('span')
            for x in Sentence:
                s += x.text
            re.append(s)
            cnt += 1
        self.reply["words"] = re
        return re
    def Sentence(self,limit=5):
        Example_Text = self.soup.find_all('div', class_='def-body ddef_b')
        limit = -1 if limit == "end" else limit
        re = []
        for Sec in Example_Text:
            Sentences = Sec.find_all('div', class_='examp dexamp')
            cnt = 0
            temp = []
            for i in Sentences:
                s = ""
                if cnt == limit:
                    break
                for x in i:
                    s += x.text
                temp.append(s)
                cnt += 1
            re.append(temp)
        self.reply["sentences"] = re
        return re
    def get_all_seperately(self,limit = 5):
        self.Defination(limit)
        self.Translation(limit)
        self.Sentence(limit)
        r = {
            "Vol": "",
            "KK": "",
            "Content": []
        }
        for i in range(limit):
            re = {
                "Translation": "",
                "Defination": "",
                "Example": ""
            }
            re["Translation"] = self.reply["words"][i]
            re["Defination"] = self.reply["defination"][i]
            re["Example"] = self.reply["sentences"][i]
            r["Content"].append(re)
        return r
    def Vol_Type_Pair(self,limit=5):
        limit = -1 if limit == "end" else limit
        re = {}
        Datas = self.Card()
        for i in Datas["Content"]:
            S = ""
            cnt = 0
            for x in i["Data"]:
                if cnt == limit:
                    break
                S += x["Translation"]
                cnt += 1
            re[i["Type"]] = S
        return re
    def Card(self,limit=5):
        re = {
            "Vol": self.word,
            "KK": "",            
            "Content": []
        }
        re["KK"] = self.KK()
        Field = self.soup.find_all('div', class_="pr entry-body__el")
        for sec in Field:
            Type = sec.find('span', class_='pos dpos').text
            Datas = []
            paragraph = sec.find_all('div', class_='pr dsense')
            for section in paragraph:
                reply = {
                    "Translation": "",
                    "Defination": "",
                    "Example": []
                }
                defination = ''
                for d in section.find_all('div', class_='def ddef_d db'):
                    defination += d.text
                reply["Defination"] = defination
                translate = ''
                for t in section.find('span',class_="trans"):
                    translate += t.text
                reply["Translation"] = translate
                example = []
                for e in section.find_all('div', class_='examp dexamp'):
                    temp = ""
                    for i in e:
                        temp += i.text
                    example.append(temp)
                reply["Example"] = example
                Datas.append(reply)
            re["Content"].append({
                "Type": Type,
                "Data": Datas
            })
        return re
if __name__ == "__main__":
    obj = Cambridge("fix")
    # print(obj.Card())
    # print(obj.KK())
    a = obj.Vol_Type_Pair(limit='end')
    print(a)
    # print(obj.Sentence())