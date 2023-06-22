
import json
import os
import hashlib

from twilio.rest import Client
from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect

app = Flask(__name__)

#index registere yönlendirecek
@app.route("/")
def index():
    #render template kullanmamalısın
    return redirect(url_for("register"))

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

def usercreate(jsondata):
    with open("users.json", "r") as f:
        data = json.load(f)
    data.update(jsondata)

    # Write the updated JSON file to disk
    with open("users.json", "w") as f:
        json.dump(data, f)

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

if __name__ == '__main__':

    app.run(debug=True)
