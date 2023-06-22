import json

username = "Emir"
phone = "5555555555"
tc = "12345678901"

data = {
                username: {
                    "phone": phone,
                    "chats": [],
                    "tc": tc
                }
            }

isimler = data.keys()

# İsimleri liste olarak elde etmek için list() fonksiyonunu kullanabilirsiniz
isimler_listesi = list(data.keys())

# İsimleri döngü kullanarak yazdırmak için aşağıdaki gibi yapabilirsiniz
for isim in data.keys():
    print(isim)
