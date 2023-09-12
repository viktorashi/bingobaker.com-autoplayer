import requests, re
from threading import Thread


def generate():
    response = requests.post("https://bingobaker.com/play/64c998520e68afc5")
    pattern = r'<meta property="og:url" content="([^"]+)"'

    matches = re.findall(pattern, response.text)

    if matches:
        session = matches[0]
        print(session)
    else:
        print("Error getting Session key")
        return session


for i in range(20):
    x = Thread(target=generate)
    x.start()
