# import requests
# from bs4 import BeautifulSoup

# """
# # Yahoo 翻譯: 詞性 + 翻譯
# Sentencelimite = 5
# reply = {
#     "words": [],
#     "sentences": []
# }
# word = "wash"
# url = url = 'https://tw.dictionary.search.yahoo.com/search?p={}'.format(word)
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# Vol_Type = soup.find_all('div', class_='pos_button fz-14 fl-l mr-12')
# Translate_Text = soup.find_all('div', class_='dictionaryExplanation')
# Sentence = soup.find_all('span', class_='d-b fz-14 fc-2nd lh-20')
# for m in range(len(Vol_Type)):
#     reply["words"].append({
#         "Vol_Type": Vol_Type[m].text,
#         "Translate_Text": Translate_Text[m].text,
#     })

# cnt = 0
# for i in Sentence:
#     s = ""
#     if cnt == Sentencelimite:
#         break
#     for x in i:
#         s += x.text
#     reply["sentences"].append(s)
#     cnt += 1
# print(reply)

# """

# # Cambridge 翻譯: 詞性 + 翻譯
# Sentencelimite = 5
# Defination_limit = 5
# Translate_Limit = 5
# reply = {
#     "words": [],
#     "sentences": []
# }
# word = "fix"
# url = url ='''https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{}'''.format(word)
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# }
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# def_part = soup.find_all('div', class_='def-body ddef_b') # 英文解釋區
# cnt = 0
# for i in def_part:
#     s = ""
#     if cnt == Defination_limit:
#         break
#     Sentence = i.find('span')
#     for x in Sentence:
#         s += x.text
#     reply["words"].append(s)
#     cnt += 1

# Example_Text = soup.find_all('div', class_='def-body ddef_b') # 造句區段
# for Sec in Example_Text:
#     Sentences = Sec.find_all('div', class_='examp dexamp') # 所有造句
#     cnt = 0
#     for i in Sentences:
#         s = ""
#         if cnt == Sentencelimite:
#             break
#         for x in i:
#             s += x.text
#         cnt += 1
# # print(reply)

import requests

def translate_text(text, source_language, target_language):
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': source_language,
        'tl': target_language,
        'dt': 't',
        'q': text
    }
    response = requests.get(url, params=params)
    print(response.text)
    if response.status_code == 200:
        # The response contains the translated text in a nested list
        translation = response.json()[0][0][0]

        return translation
    else:
        return None

# Example usage
text = "Hello"
source_language = "en"
target_language = "zh-TW"
translation = translate_text(text, source_language, target_language)
print(f"Translation: {translation}")
