from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect
from cryptography.fernet import Fernet
import jso
import test2
from twilio.rest import Client
app = Flask(__name__)

account_sid = "AC81a1b3293edc7ca46d8af73468033abf"
auth_token = "4ab8120c60ae06ba036127cd288fa764"
verify_sid = "VA4973fb8c0cedc410d7ce9693ba050421"
key = "kG42LRGl1Tk57NRRaCV2WJ4TcDyzyz_S4TUy59mMHmE="
salt = "cs2OAjbibK3gxKd8U-V5wUUe4JTCe2TIhci33J0jANk="

def usercreate(jsondata):
    with open("users.json", "r") as f:
        data = json.load(f)

    data.update(jsondata)

    # Write the updated JSON file to disk
    with open("users.json", "w") as f:
        json.dump(data, f)

def decryptdata(data):
    fernetextra = Fernet(salt)
    datadecrypt = fernetextra.decrypt(data)
    fernetmaster = Fernet(key)
    datadecrypt = fernetmaster.decrypt(datadecrypt)
    print(datadecrypt.decode("UTF-8"))
    return datadecrypt.decode("UTF-8")


def createencryption(data):
    fernetmaster = Fernet(key)
    encrypted_data = fernetmaster.encrypt(data.encode("UTF-8"))
    print("Şifrelenmiş veri:", encrypted_data)
    fernetextra = Fernet(salt)
    encrypted_data = fernetextra.encrypt(encrypted_data)
    print(encrypted_data)
    return encrypted_data


data = createencryption("Ömer Abey")
decryptdata(data)

def get_usernames(json_data):
    usernames = []
    for key, value in json_data.items():
        usernames.append(key)
    return usernames

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Register")
    if request.method == 'POST':
        username = request.form['username']
        phone = request.form['phone']
        tc = request.form['tc']
        tc_valid = tckontrol(tc)

        print(username)
        print(phone)
        print(tc)
        print(tc_valid)

        if tc_valid:
            print("TC doğrulandı")
        else:
            print("TC doğrulanmadı")
            return render_template('kayitt.html')

        phonechecker = phonecheck(phone)
        phone = "+90" + phonechecker[1]

        if phonechecker:
            new_account = {
                username: {
                    "phone": phone,
                    "chats": [],
                    "tc": tc
                }
            }
            #client = Client(account_sid, auth_token)

            #verification = client.verify.v2.services(verify_sid) \
            #   .verifications \
            #    .create(to=phone, channel="sms")
            #print(verification.status)
            with open("users.json", "r") as f:
                data = json.load(f)
            available = True
            isim = next(iter(new_account.keys()))
            for i in data:
                if i == isim:
                    available = False
                    pass
            print("Deneme: ", isim)
            if available:
                # Write the updated JSON file to disk
                with open("users.json", "w") as f:
                    json.dump(data, f)
                res = make_response("<h1>Cookie is set</h1>")
                res.set_cookie("name", createencryption(isim))
                return res


            else:
                print("Kullanıcı adı zaten var")
                return render_template('kayitt.html')
            #return redirect(url_for('verify', phone=phone, userdata=new_account))
        else:
            print("Telefon doğrulanmadı")
            return render_template('kayitt.html')

    return render_template('kayit.html')

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        otp_code = request.form['otp_code']
        phone = request.args.get('phone')

        client = Client(account_sid, auth_token)
        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=phone, code=otp_code)
        print(verification_check.status)
    else:
        return render_template("kontrol.html")

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    cookie = request.cookies.get("name")
    if cookie:
        cookie = decryptdata(cookie)
        print(cookie)
        resp = make_response(render_template("chat.html", username=cookie))
        resp.set_cookie("name", createencryption(cookie))
        return resp
    else:
        return render_template("kayit.html")





if __name__ == '__main__':
    app.run(debug=True)
