import json
import datetime
import requests
from Bard import Chatbot

#def nudepic(picture):
#    url = 'https://api.deepai.org/api/nsfw-detector'
#   headers = {
#        'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'
#    }
#    response = requests.post(
#        url,
#        files=picture 'image': open('static/images/logo.png', 'rb')
#        },
#        headers=headers
#    )
#    print(response.text)

def add_message(username, message):
    # Get the current time

    now = datetime.datetime.now()
    print(now)
    # Load the messages from the JSON file
    data = loadmessages("chat0001.json")
    try:
        current_max_id = max(data.keys())
    except:
        current_max_id = 0
    print(current_max_id)
    # Add the new message to the data structure
    data.update({str(int(current_max_id) + 1): {"username": username, "message": message, "time": str(now)}})
    with open("chat0001.json", "w") as f:
        json.dump(data, f)


def printchat(chatfile):
    data = loadmessages(chatfile)
    for key in data:
        name = key
        if "username" in data[key]:
            name = data[key]["username"]
        print(f"{name}: {data[key]}")



def urlsafetycheck(url):
  """Checks if a URL is safe.

  Args:
    url: The URL to check.

  Returns:
    "Safe" if the URL is safe, "Malicious" otherwise.
  """

  with open("unsafelist.txt", "r") as f:
    for line in f:
      if line.strip() in url:
        return "Malicious"

  return "Safe"


print(urlsafetycheck("http://182.113.15.133:34548/bin.sh"))






def userload():
    with open('users.json', 'r') as f:
        return json.load(f)

def sendmessage(message, sender):
    messages = loadmessages()
    messages.update({sender: message})
    with open("messages.json", "w") as f:
        json.dump(messages, f)

def userloginheck(username):
    users = userload()
    if username in users:
        print("Kullanıcı adı doğru")

def usercreate(jsondata):
    with open("users.json", "r") as f:
        data = json.load(f)

    data.update(jsondata)

    # Write the updated JSON file to disk
    with open("users.json", "w") as f:
        json.dump(data, f)


def loadmessages(chatfile):
    with open(chatfile, 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    new_account = {
        "rıdvan polat": {
            "phone": "458903840584",
            "chats": [3849834],
            "tc": "432482340"
        }
    }
    #add_message("Lucifer polat", "Selamlar Reisler")
    #printchat("chat0001.json")
    #usercreate(new_account)
    #print(userloginheck("Mehmet Emre"))

