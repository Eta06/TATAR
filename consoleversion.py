import json
import hashlib
import os
import requests
import fuzzywuzzy
import torch

from fuzzywuzzy import fuzz
from Bard import Chatbot
from twilio.rest import Client
from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect
from gtts import gTTS
from diffusers import StableDiffusionPipeline
from flask import Flask, request, jsonify
#from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)
image = "./static/images/tester.jpeg"

#index registere yönlendirecek
@app.route("/")

def index():
    #render template kullanmamalısın
    return redirect(url_for("register"))

def nsfwbulucu(image):
    url = 'https://api.deepai.org/api/nsfw-detector'
    headers = {
        'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'
    }
    response = requests.post(
        url,
        files={
            'image': open(image, 'rb')
        },
        headers=headers
    )
    return print(response.text)


def speak(text):
    audio = gTTS(text=text, lang="en", slow=False)
    audio.save("audio.mp3")
    os.system("start audio.mp3")

def yarenai():
    chatbot = Chatbot("GOOGLEID")

    instructions = """
    Instructions: From now your name is Yaren. And you are speaking with Emir. Say hi! 
    """

    while True:
        request = input("Enter a message: ")
        if request == "exit":
            exit()
        # Get the response from the chatbot
        response = chatbot.ask(instructions + request)
        if not response["choices"]:
            continue
        message = response["choices"][0]["content"][0]
        try:
            print(message)
        except:
            print("Error: No response found")

def tckontrol(s):
    try:
        n = 11
        d = {}
        for i in range(1, n + 1):
            d[i] = int(s[i - 1])
        teklertoplam = 0
        ciftlertoplam = 0
        for i in range(1, n - 1):
            if i % 2 != 0:
                teklertoplam += d[i]
            else:
                ciftlertoplam += d[i]
        toplam1 = 3 * teklertoplam + ciftlertoplam
        q1 = (10 - toplam1 % 10) % 10
        toplam2 = 3 * (ciftlertoplam + q1) + teklertoplam
        q2 = (10 - toplam2 % 10) % 10
        if q1 == d[10] and q2 == d[11]:
            return True
        else:
            return False
    except:
        return False

def phonecheck(phone_number):
    try:
        if len(phone_number) >= 10 and len(phone_number) <= 13:
            if not any(c.isalpha() for c in phone_number):
                if phone_number[0] == '0':
                    phone_number = phone_number[1:]
                    return True, phone_number
                elif phone_number[0] == '+':
                    phone_number = phone_number[3:]
                    return True, phone_number
                elif phone_number[0] == '9':
                    phone_number = phone_number[2:]
                    return True, phone_number
                elif phone_number[0] == '5':
                    return True, phone_number
                else:
                    return False
            else:
                return False
        else:
            return False
    except:
        return False

def get_words(sentence):
  words = sentence.split(" ")
  return words

def badwords():
  sentence = input("Enter a sentence: ")
  words = get_words(sentence)
  wordlist = ["abaza","abazan","ag","a\u011fz\u0131na s\u0131\u00e7ay\u0131m","ahmak","allahs\u0131z","am","amar\u0131m","ambiti","am biti","amc\u0131\u011f\u0131","amc\u0131\u011f\u0131n","amc\u0131\u011f\u0131n\u0131","amc\u0131\u011f\u0131n\u0131z\u0131","amc\u0131k","amc\u0131k ho\u015faf\u0131","amc\u0131klama","amc\u0131kland\u0131","amcik","amck","amckl","amcklama","amcklaryla","amckta","amcktan","amcuk","am\u0131k","am\u0131na","am\u0131nako","am\u0131na koy","am\u0131na koyar\u0131m","am\u0131na koyay\u0131m","am\u0131nakoyim","am\u0131na koyyim","am\u0131na s","am\u0131na sikem","am\u0131na sokam","am\u0131n feryad\u0131","am\u0131n\u0131","am\u0131n\u0131 s","am\u0131n oglu","am\u0131no\u011flu","am\u0131n o\u011flu","am\u0131s\u0131na","am\u0131s\u0131n\u0131","amina","amina g","amina k","aminako","aminakoyarim","amina koyarim","amina koyay\u0131m","amina koyayim","aminakoyim","aminda","amindan","amindayken","amini","aminiyarraaniskiim","aminoglu","amin oglu","amiyum","amk","amkafa","amk \u00e7ocu\u011fu","amlarnzn","aml\u0131","amm","ammak","ammna","amn","amna","amnda","amndaki","amngtn","amnn","amona","amq","ams\u0131z","amsiz","amsz","amteri","amugaa","amu\u011fa","amuna","ana","anaaann","anal","analarn","anam","anamla","anan","anana","anandan","anan\u0131","anan\u0131","anan\u0131n","anan\u0131n am","anan\u0131n am\u0131","anan\u0131n d\u00f6l\u00fc","anan\u0131nki","anan\u0131sikerim","anan\u0131 sikerim","anan\u0131sikeyim","anan\u0131 sikeyim","anan\u0131z\u0131n","anan\u0131z\u0131n am","anani","ananin","ananisikerim","anani sikerim","ananisikeyim","anani sikeyim","anann","ananz","anas","anas\u0131n\u0131","anas\u0131n\u0131n am","anas\u0131 orospu","anasi","anasinin","anay","anayin","angut","anneni","annenin","annesiz","anuna","aptal","aq","a.q","a.q.","aq.","ass","atkafas\u0131","atm\u0131k","att\u0131rd\u0131\u011f\u0131m","attrrm","auzlu","avrat","ayklarmalrmsikerim","azd\u0131m","azd\u0131r","azd\u0131r\u0131c\u0131","babaannesi ka\u015far","baban\u0131","baban\u0131n","babani","babas\u0131 pezevenk","baca\u011f\u0131na s\u0131\u00e7ay\u0131m","bac\u0131na","bac\u0131n\u0131","bac\u0131n\u0131n","bacini","bacn","bacndan","bacy","bastard","basur","beyinsiz","b\u0131z\u0131r","bitch","biting","bok","boka","bokbok","bok\u00e7a","bokhu","bokkkumu","boklar","boktan","boku","bokubokuna","bokum","bombok","boner","bosalmak","bo\u015falmak","cenabet","cibiliyetsiz","cibilliyetini","cibilliyetsiz","cif","cikar","cim","\u00e7\u00fck","dalaks\u0131z","dallama","daltassak","dalyarak","dalyarrak","dangalak","dassagi","diktim","dildo","dingil","dingilini","dinsiz","dkerim","domal","domalan","domald\u0131","domald\u0131n","domal\u0131k","domal\u0131yor","domalmak","domalm\u0131\u015f","domals\u0131n","domalt","domaltarak","domalt\u0131p","domalt\u0131r","domalt\u0131r\u0131m","domaltip","domaltmak","d\u00f6l\u00fc","d\u00f6nek","d\u00fcd\u00fck","eben","ebeni","ebenin","ebeninki","ebleh","ecdad\u0131n\u0131","ecdadini","embesil","emi","fahise","fahi\u015fe","feri\u015ftah","ferre","fuck","fucker","fuckin","fucking","gavad","gavat","geber","geberik","gebermek","gebermi\u015f","gebertir","ger\u0131zekal\u0131","gerizekal\u0131","gerizekali","gerzek","giberim","giberler","gibis","gibi\u015f","gibmek","gibtiler","goddamn","godo\u015f","godumun","gotelek","gotlalesi","gotlu","gotten","gotundeki","gotunden","gotune","gotunu","gotveren","goyiim","goyum","goyuyim","goyyim","g\u00f6t","g\u00f6t deli\u011fi","g\u00f6telek","g\u00f6t herif","g\u00f6tlalesi","g\u00f6tlek","g\u00f6to\u011flan\u0131","g\u00f6t o\u011flan\u0131","g\u00f6to\u015f","g\u00f6tten","g\u00f6t\u00fc","g\u00f6t\u00fcn","g\u00f6t\u00fcne","g\u00f6t\u00fcnekoyim","g\u00f6t\u00fcne koyim","g\u00f6t\u00fcn\u00fc","g\u00f6tveren","g\u00f6t veren","g\u00f6t verir","gtelek","gtn","gtnde","gtnden","gtne","gtten","gtveren","hasiktir","hassikome","hassiktir","has siktir","hassittir","haysiyetsiz","hayvan herif","ho\u015faf\u0131","h\u00f6d\u00fck","hsktr","huur","\u0131bnel\u0131k","ibina","ibine","ibinenin","ibne","ibnedir","ibneleri","ibnelik","ibnelri","ibneni","ibnenin","ibnerator","ibnesi","idiot","idiyot","imansz","ipne","iserim","i\u015ferim","ito\u011flu it","kafam girsin","kafas\u0131z","kafasiz","kahpe","kahpenin","kahpenin feryad\u0131","kaka","kaltak","kanc\u0131k","kancik","kappe","karhane","ka\u015far","kavat","kavatn","kaypak","kayyum","kerane","kerhane","kerhanelerde","kevase","keva\u015fe","kevvase","koca g\u00f6t","kodu\u011fmun","kodu\u011fmunun","kodumun","kodumunun","koduumun","koyarm","koyay\u0131m","koyiim","koyiiym","koyim","koyum","koyyim","krar","kukudaym","laciye boyad\u0131m","lavuk","libo\u015f","madafaka","mal","malafat","malak","manyak","mcik","meme","memelerini","mezveleli","minaamc\u0131k","mincikliyim","mna","monakkoluyum","motherfucker","mudik","oc","ocuu","ocuun","O\u00c7","o\u00e7","o. \u00e7ocu\u011fu","o\u011flan","o\u011flanc\u0131","o\u011flu it","orosbucocuu","orospu","orospucocugu","orospu cocugu","orospu \u00e7oc","orospu\u00e7ocu\u011fu","orospu \u00e7ocu\u011fu","orospu \u00e7ocu\u011fudur","orospu \u00e7ocuklar\u0131","orospudur","orospular","orospunun","orospunun evlad\u0131","orospuydu","orospuyuz","orostoban","orostopol","orrospu","oruspu","oruspu\u00e7ocu\u011fu","oruspu \u00e7ocu\u011fu","osbir","ossurduum","ossurmak","ossuruk","osur","osurduu","osuruk","osururum","otuzbir","\u00f6k\u00fcz","\u00f6\u015fex","patlak zar","penis","pezevek","pezeven","pezeveng","pezevengi","pezevengin evlad\u0131","pezevenk","pezo","pic","pici","picler","pi\u00e7","pi\u00e7in o\u011flu","pi\u00e7 kurusu","pi\u00e7ler","pipi","pipi\u015f","pisliktir","porno","pussy","pu\u015ft","pu\u015fttur","rahminde","revizyonist","s1kerim","s1kerm","s1krm","sakso","saksofon","salaak","salak","saxo","sekis","serefsiz","sevgi koyar\u0131m","sevi\u015felim","sexs","s\u0131\u00e7ar\u0131m","s\u0131\u00e7t\u0131\u011f\u0131m","s\u0131ecem","sicarsin","sie","sik","sikdi","sikdi\u011fim","sike","sikecem","sikem","siken","sikenin","siker","sikerim","sikerler","sikersin","sikertir","sikertmek","sikesen","sikesicenin","sikey","sikeydim","sikeyim","sikeym","siki","sikicem","sikici","sikien","sikienler","sikiiim","sikiiimmm","sikiim","sikiir","sikiirken","sikik","sikil","sikildiini","sikilesice","sikilmi","sikilmie","sikilmis","sikilmi\u015f","sikilsin","sikim","sikimde","sikimden","sikime","sikimi","sikimiin","sikimin","sikimle","sikimsonik","sikimtrak","sikin","sikinde","sikinden","sikine","sikini","sikip","sikis","sikisek","sikisen","sikish","sikismis","siki\u015f","siki\u015fen","siki\u015fme","sikitiin","sikiyim","sikiym","sikiyorum","sikkim","sikko","sikleri","sikleriii","sikli","sikm","sikmek","sikmem","sikmiler","sikmisligim","siksem","sikseydin","sikseyidin","siksin","siksinbaya","siksinler","siksiz","siksok","siksz","sikt","sikti","siktigimin","siktigiminin","sikti\u011fim","sikti\u011fimin","sikti\u011fiminin","siktii","siktiim","siktiimin","siktiiminin","siktiler","siktim","siktim","siktimin","siktiminin","siktir","siktir et","siktirgit","siktir git","siktirir","siktiririm","siktiriyor","siktir lan","siktirolgit","siktir ol git","sittimin","sittir","skcem","skecem","skem","sker","skerim","skerm","skeyim","skiim","skik","skim","skime","skmek","sksin","sksn","sksz","sktiimin","sktrr","skyim","slaleni","sokam","sokar\u0131m","sokarim","sokarm","sokarmkoduumun","sokay\u0131m","sokaym","sokiim","soktu\u011fumunun","sokuk","sokum","soku\u015f","sokuyum","soxum","sulaleni","s\u00fclaleni","s\u00fclalenizi","s\u00fcrt\u00fck","\u015ferefsiz","\u015f\u0131ll\u0131k","taaklarn","taaklarna","tarrakimin","tasak","tassak","ta\u015fak","ta\u015f\u015fak","tipini s.k","tipinizi s.keyim","tiyniyat","toplarm","topsun","toto\u015f","vajina","vajinan\u0131","veled","veledizina","veled i zina","verdiimin","weled","weledizina","whore","xikeyim","yaaraaa","yalama","yalar\u0131m","yalarun","yaraaam","yarak","yaraks\u0131z","yaraktr","yaram","yaraminbasi","yaramn","yararmorospunun","yarra","yarraaaa","yarraak","yarraam","yarraam\u0131","yarragi","yarragimi","yarragina","yarragindan","yarragm","yarra\u011f","yarra\u011f\u0131m","yarra\u011f\u0131m\u0131","yarraimin","yarrak","yarram","yarramin","yarraminba\u015f\u0131","yarramn","yarran","yarrana","yarrrak","yavak","yav\u015f","yav\u015fak","yav\u015fakt\u0131r","yavu\u015fak","y\u0131l\u0131\u015f\u0131k","yilisik","yogurtlayam","yo\u011furtlayam","yrrak","z\u0131kk\u0131m\u0131m","zibidi","zigsin","zikeyim","zikiiim","zikiim","zikik","zikim","ziksiiin","ziksiin","zulliyetini","zviyetini"]

  for word in words:
    for i, w in enumerate(wordlist):
      ratio = fuzz.ratio(word, w)
      if ratio > 80:
        print(f"Found {word} in wordlist at index {i} with ratio {ratio}")

def usercreate(jsondata):
    with open("users.json", "r") as f:
        data = json.load(f)
    data.update(jsondata)

    # Write the updated JSON file to disk
    with open("users.json", "w") as f:
        json.dump(data, f)

@app.route("/myai", methods=["GET", "POST"])
def myai():
    if request.method == "GET":
        return render_template("myai.html")
    else:
        return render_template("myai.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("kayit.html")
    else:
        username = request.form['username']
        phone = request.form['phone']
        tc = request.form['tc']
        tc_valid = tckontrol(tc)
        if tc_valid:
            print("TC doğrulandı")
        else:
            print("TC doğrulanamadı")
            return render_template('kayit.html')
        phonechecker = phonecheck(phone)
        phone = "+90" + phonechecker[1]
        if phonechecker:
            print("Telefon doğrulandı")
            new_account = {
                username: {
                    "phone": phone,
                    "chats": [],
                    "tc": tc
                }
            }
            usercreate(new_account)
        else:
            print("Telefon doğrulanamadı")
            return render_template('kayit.html')

        # Kayıt işlemi tamamlandığında veya doğrulama işlemi tamamlandığında yanıt döndürün
        return render_template('chat.html')

"""
def generate_keypair():
    # RSA ile anahtar çifti oluşturdum
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
"""
"""
def encrypt_text(text, public_key):
    # Metni RSA ile şifreledim
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_text = cipher.encrypt(text.encode())
    return encrypted_text
"""
"""
@app.route('/encrypt', methods=['POST'])
def encrypt():
    # POST isteği ile gönderilen veriyi aldım
    text = request.form['text']

    # Anahtar çiftini oluşturdum
    private_key, public_key = generate_keypair()

    # Metni şifreledim
    encrypted_text = encrypt_text(text, public_key)

    # Anahtar çiftini yanıt olarak gönderin
    return jsonify({
        'private_key': private_key.decode(),
        'encrypted_text': encrypted_text.hex()
    })
"""
#nsfwbulucu(image)
yarenai()
