class AnkiHtml:
    def __init__(self):
        self.AnkiText = ""
        self.init_Text()
    def init_Text(self):
        self.AnkiText = '''#separator:tab
#html:true
'''
    def H2_tag(self,text):
        self.AnkiText += f"<h2>{text}</h2>"
    def H3_tag(self,text):
        self.AnkiText += f"<h3>{text}</h3>"
    def p_tag(self,text):
        self.AnkiText += f"<p>{text}</p>"
    def br(self):
        self.AnkiText += "<br>"
    def hr(self):
        self.AnkiText += "<hr>"
    def gap(self):
        self.AnkiText += "\t"
    def AnkiSoundTag(self,src):
        self.AnkiText += "[sound:RduanAnki{}.mp3]".format(src)
    def AddDirectly(self,text):
        self.AnkiText += text
    def div_start(self):
        self.AnkiText += '<div class="RduanCard">'
    def div_end(self):
        self.AnkiText += '</div>'
    def next_word(self):
        self.AnkiText += "\n"
    def get_result(self):
        return self.AnkiText
    def AudioTag(self,src):
        self.AnkiText += f'<audio controls><source src="{src}" type="audio/mpeg"></audio>'
    