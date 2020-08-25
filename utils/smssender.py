import requests,json

def send_sms(telephone,message):
    url = "http://10.250.70.82:5000/sendsms/"
    telephone = '852'+telephone
    message = '您的验证码是:{code}。如非本人操作，请忽略此短信'.format(code=message)
    payload = {
        "telephone":telephone,
        "message":message
    }
    headers = {
      'Content-Type': 'application/json'
    }
    data = json.dumps(payload)
    try:
        response = requests.request("POST", url, headers=headers, data = data,timeout=5)
    except:
        return False
    if json.loads(response.text)['code'] == 200:
        return True
    else:
        return False