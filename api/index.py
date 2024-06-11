from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)

def get_headers(bearer_token):
    headers = {
        'User-Agent': "Mozilla/6.0 (Linux; Android 8.1.2; Nexus 6 Build/N2G47H; wv) AppleWebKit/637.36 (KHTML, like Gecko) Version/5.0 Chrome/82.0.4044.117 Mobile Safari/637.36",
        'Accept': "application/json",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/json",
        'authorization': f"Bearer {bearer_token}",
        'Origin': "https://hamsterkombat.io",
        'X-Requested-With': "org.telegram.messenger",
        'Sec-Fetch-Site': "same-site",
        'Sec-Fetch-Mode': "cors",
        'Sec-Fetch-Dest': "empty",
        'Referer': "https://hamsterkombat.io/clicker",
        'Accept-Language': "en,en-GB;q=0.9,en-US;q=0.8"
    }
    return headers

def call_first_api(bearer_token):
    url = "https://api.hamsterkombat.io/clicker/sync"
    headers = get_headers(bearer_token)
    response = requests.post(url, headers=headers, verify=False)
    print("প্রথম এপিআই কল করা হচ্ছে...")
    print(response.text)

    if response.status_code == 200:
        call_second_api(bearer_token)
    else:
        print("প্রথম এপিআই কল ব্যর্থ হয়েছে, প্রোগ্রাম শেষ করা হচ্ছে।")

def call_second_api(bearer_token):
    url = "https://api.hamsterkombat.io/clicker/tap"
    headers = get_headers(bearer_token)
    current_timestamp = int(time.time())
    payload = json.dumps({
        "count": 7000,
        "availableTaps": 0,
        "timestamp": current_timestamp
    })

    response = requests.post(url, data=payload, headers=headers)
    print("দ্বিতীয় এপিআই কল করা হচ্ছে...")
    print(response.text)

    if response.status_code == 200:
        call_third_api(bearer_token)
    else:
        print("দ্বিতীয় এপিআই কল ব্যর্থ হয়েছে, প্রোগ্রাম শেষ করা হচ্ছে।")

def call_third_api(bearer_token):
    url = "https://api.hamsterkombat.io/clicker/buy-boost"
    headers = get_headers(bearer_token)
    current_timestamp = int(time.time())
    payload = json.dumps({
      "boostId": "BoostFullAvailableTaps",
      "timestamp": current_timestamp
    })

    response = requests.post(url, data=payload, headers=headers, verify=False)
    print("তৃতীয় এপিআই কল করা হচ্ছে...")
    print(response.text)

    if response.status_code == 200:
        print("দ্বিতীয় এপিআই আবার কল করা হচ্ছে...")
        call_second_api(bearer_token)
    else:
        print("তৃতীয় এপিআই কল ব্যর্থ হয়েছে, প্রোগ্রাম শেষ করা হচ্ছে।")

@app.route('/', methods=['POST'])
def handle_request():
    bearer_token = request.json['bearer_token']
    call_first_api(bearer_token)
    return jsonify({'message': 'Request handled successfully'})

if __name__ == '__main__':
    app.run(debug=True)  # অথবা debug=False করুন যদি প্রোডাকশনে ব্যবহার করা হয়।
