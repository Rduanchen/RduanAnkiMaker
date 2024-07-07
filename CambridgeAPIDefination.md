# Cambridge Parser Library Defination

> The Cambridge Parser API is a RESTful API that allows you to parse English text and get back a structured JSON response. The API is based on the Cambridge English Profile, a framework for describing English language ability. The API can be used to analyze the grammatical structure of English sentences, identify parts of speech, and extract other linguistic features.


## 2. Import to Project
```python
import CambridgeParser as Cambridge
```

## 3. Init
```python
# Translate = Cambridge('PUT_THE_WORD_HERE')
Translate = Cambridge('Hello')
```
## 4. Features
* Get KK Pronunciation (US and UK)
* Get the Translation
* Get The Defination
* Get All Example Sentence
* Get All WordType
* Get All Datas
* Get Type_Translation Pair
* Get Soup Object


# Docs
## get_data()
> This Function will return the soup object of the word

Example:
```python
a = Translate.get_data()
print(a.text)
```

## KK()
> This Function will return the pronunciation of the word in KK (US and UK)

Example:
```python
a = Translate.KK():
print(a)
```
Return:
```python
['UK: /fɪks/', ' US: /fɪks/']
```

## Translation(limit)
> This Function will return the translation ( Chinese ) of the word `limit` is the max number of translation you want to get (default is 5), if you want to get all translation, you can set `limit` to 'end'

Example:
```python
a = Translate.Translation(limit = 2)
b = Translate.Translation(limit = 'end')
print(a)
print(b)
```
Return:
```python
# a = 
['修理', '安排，確定（時間、地點、價格等）']

# b = 
['修理', '安排，確定（時間、地點、價格等）', '使固定；安裝', '盯著看，凝視', '不斷想（某事）;仍然記得（某事）', '操縱;在（比賽或選舉）中作弊', '梳洗，整理（頭髮、容妝、衣服等）', '做（飯）;準備（食物或飲料）', '懲罰，收拾（尤指待人不公者）', '（對攝影感光材料）定（色），定（影）', '閹割（動物）', '注射
毒品', '操縱;在（比賽或選舉）中作弊', '窘境；困境', '（毒品或致癮物的）一次用量', '（車輛的）方位;方位確定']
```
## Defination(limit)
> This Function will return the English Defination of the word, `limit` is the max number of defination you want to get (default is 5), if you want to get all defination, you can set `limit` to 'end'.

Example:
```python
a = Translate.Defination(limit = 2)
b = Translate.Defination(limit = 'end')
print(a)
print(b)
```


## Sentence(limit)
> This Function will return the Example Sentence of the word, `limit` is the max number of sentence you want to get (default is 5), if you want to get all sentence, you can set `limit` to 'end'.


## Vol_Type_Pair()
> This Function will return the Type_Translation Pair of the word, `limit` is the max number of defination you want to get (default is 5), if you want to get all defination, you can set `limit` to 'end'.

## Card(limit):
> Due to the Cambridge Dictionary organize word's Explanation as 'Card', Each Card contains its own Type, Defination, Translation, and Example Sentence. This Function will return the Card of the word, `limit` is the max number of card you want to get (default is 5), if you want to get all card, you can set `limit` to 'end'.


Return Format
```python
{
    'Word': 'Hello',
    'Pronunciation': {'UK': 'həˈləʊ', 'US': 'həˈloʊ'},
    'Type': ['exclamation', 'noun']
    'Content': [
        {
            'Type': 'exclamation',
            'Datas' : [
                {
                    'Defination': 'used when meeting or greeting someone',
                    'Translation': '喂，你好（用於問候或打招呼）',
                    'Sentence': [
                        "Hello, Paul. I haven't seen you for ages.\n「你好，保羅。好久不見了。」",
                        "Hello, is anyone there?\n「喂，有人在嗎？」"
                    ]
                    
                }
            ]
        }
    ]
}
```
