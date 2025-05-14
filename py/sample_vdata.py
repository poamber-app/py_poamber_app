# Create a Python script containing 20 critical, 20 medium, and 20 low vulnerabilities

full_vulnerable_script = """
import os
import sqlite3
import pickle
import jwt
import hashlib
import random
import secrets
import urllib.request
import requests
from flask import Flask, request, redirect, make_response

app = Flask(__name__)

# ----------------------------
# Critical Vulnerabilities
# ----------------------------

@app.route('/sql_injection')
def sql_injection():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)
    return str(cursor.fetchall())

@app.route('/command_injection')
def command_injection():
    cmd = request.args.get('cmd')
    return os.popen(cmd).read()

@app.route('/pickle_injection')
def pickle_injection():
    data = request.args.get('data')
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

@app.route('/rce')
def rce():
    code = request.args.get('code')
    exec(code)
    return "Executed"

@app.route('/ssrf')
def ssrf():
    url = request.args.get('url')
    response = urllib.request.urlopen(url)
    return response.read()

@app.route('/path_traversal')
def path_traversal():
    filename = request.args.get('filename')
    with open(filename, 'r') as f:
        return f.read()

@app.route('/weak_hashing')
def weak_hashing():
    password = request.args.get('password')
    return hashlib.md5(password.encode()).hexdigest()

@app.route('/xxe', methods=['POST'])
def xxe():
    data = request.data.decode()
    import xml.etree.ElementTree as ET
    tree = ET.fromstring(data)
    return tree.find('.//password').text

@app.route('/file_upload', methods=['POST'])
def file_upload():
    file = request.files['file']
    file.save("/tmp/" + file.filename)
    return "File saved"

@app.route('/open_redirect')
def open_redirect():
    url = request.args.get('url')
    return redirect(url)

@app.route('/csrf')
def csrf():
    return "<form method='post' action='/change_password'><input name='password' value='newpass'></form>"

@app.route('/insecure_jwt')
def insecure_jwt():
    payload = {"user": "admin"}
    token = jwt.encode(payload, '1234', algorithm='HS256')
    return token

@app.route('/insecure_tls_validation')
def insecure_tls_validation():
    url = request.args.get('url')
    return requests.get(url, verify=False).text

@app.route('/unsafe_reflection')
def unsafe_reflection():
    module = request.args.get('module')
    eval("import " + module)
    return "Imported"

@app.route('/hardcoded_secrets')
def hardcoded_secrets():
    return "Secret API Key: ABCD1234"

@app.route('/bypass_auth')
def bypass_auth():
    if request.args.get('admin') == 'true':
        return "Admin Access Granted"
    return "User Access"

@app.route('/insecure_random')
def insecure_random():
    return str(random.randint(0, 1000000))

@app.route('/sensitive_data_exposure')
def sensitive_data_exposure():
    return "Credit Card Number: 4111-1111-1111-1111"

@app.route('/cors_misconfig')
def cors_misconfig():
    resp = make_response("CORS Misconfigured")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# ----------------------------
# Medium Vulnerabilities
# ----------------------------

@app.route('/leaky_logging')
def leaky_logging():
    user = request.args.get('user')
    print(f"User login attempt: {user}")
    return "Logged"

@app.route('/info_disclosure')
def info_disclosure():
    return os.listdir('/')

@app.route('/clickjacking')
def clickjacking():
    resp = make_response("<h1>Welcome</h1>")
    return resp

@app.route('/log_injection')
def log_injection():
    user = request.args.get('user')
    print("User: " + user)
    return "OK"

@app.route('/debug_mode_exposure')
def debug_mode_exposure():
    if request.args.get('debug') == 'true':
        app.debug = True
        return "Debug Mode On"
    return "Debug Mode Off"

@app.route('/overly_permissive_cors')
def overly_permissive_cors():
    resp = make_response("Permissive CORS")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

@app.route('/insecure_form_action')
def insecure_form_action():
    return "<form method='POST' action='http://insecure.site/submit'></form>"

@app.route('/unvalidated_redirect')
def unvalidated_redirect():
    url = request.args.get('next')
    return redirect(url)

@app.route('/weak_encoding')
def weak_encoding():
    data = request.args.get('data')
    return data.encode('utf-7')

@app.route('/insecure_cache_control')
def insecure_cache_control():
    resp = make_response("Cached Content")
    resp.headers['Cache-Control'] = 'public, max-age=86400'
    return resp

@app.route('/html_injection')
def html_injection():
    user_input = request.args.get('input')
    return f"<div>{user_input}</div>"

@app.route('/verbose_error')
def verbose_error():
    raise Exception("Verbose error for debugging")

@app.route('/inefficient_algorithm')
def inefficient_algorithm():
    n = int(request.args.get('n', '10000'))
    result = [x for x in range(n) if all(x % i != 0 for i in range(2, x))]
    return str(result)

@app.route('/open_ports')
def open_ports():
    os.system("nmap -sS localhost")
    return "Port scan done"

@app.route('/unencrypted_connection')
def unencrypted_connection():
    import smtplib
    server = smtplib.SMTP('mail.example.com', 25)
    server.sendmail('from@example.com', 'to@example.com', 'Hello')
    return "Email sent"

@app.route('/insecure_token_generation')
def insecure_token_generation():
    return str(secrets.randbelow(100000))

@app.route('/misconfigured_logging')
def misconfigured_logging():
    try:
        1 / 0
    except Exception as e:
        return str(e)

@app.route('/weak_password_policy')
def weak_password_policy():
    password = request.args.get('password')
    if len(password) < 4:
        return "Password Accepted"
    return "Password Rejected"

@app.route('/hardcoded_api_key')
def hardcoded_api_key():
    return "API_KEY=1234567890ABCDEF"


# ----------------------------
# Low Vulnerabilities (dummy)
# ----------------------------

@app.route('/unused_code')
def unused_code():
    pass

@app.route('/debug_comments')
def debug_comments():
    # TODO: remove debug comments
    return "Debug comments present"

@app.route('/default_credentials')
def default_credentials():
    return "Username: admin, Password: admin"

@app.route('/insufficient_logging')
def insufficient_logging():
    return "Action completed"

@app.route('/missing_security_headers')
def missing_security_headers():
    return "No security headers added"

@app.route('/obsolete_protocol')
def obsolete_protocol():
    return "Using FTP instead of SFTP"

@app.route('/inefficient_loops')
def inefficient_loops():
    result = []
    for i in range(1000):
        for j in range(1000):
            result.append(i * j)
    return str(len(result))

@app.route('/lack_of_rate_limiting')
def lack_of_rate_limiting():
    return "No rate limit applied"

@app.route('/weak_ssl_config')
def weak_ssl_config():
    return "Using SSLv3"

@app.route('/improper_data_validation')
def improper_data_validation():
    data = request.args.get('data')
    return f"Data received: {data}"

@app.route('/no_input_sanitization')
def no_input_sanitization():
    user = request.args.get('user')
    return f"Welcome {user}"

@app.route('/no_csrf_token')
def no_csrf_token():
    return "<form method='POST'></form>"

@app.route('/hardcoded_debug_mode')
def hardcoded_debug_mode():
    if True:
        app.debug = True
    return "Debug mode hardcoded"

@app.route('/excessive_privileges')
def excessive_privileges():
    return "Running as root"

@app.route('/unencrypted_storage')
def unencrypted_storage():
    with open('/tmp/sensitive_data.txt', 'w') as f:
        f.write("Sensitive data unencrypted")
    return "Data saved"

@app.route('/missing_audit_logging')
def missing_audit_logging():
    return "No audit log"

@app.route('/unhandled_exception')
def unhandled_exception():
    return 1 / 0

@app.route('/deprecated_function')
def deprecated_function():
    os.popen('ls')
    return "Deprecated function used"

@app.route('/plaintext_password_storage')
def plaintext_password_storage():
    password = request.args.get('password')
    with open('/tmp/passwords.txt', 'a') as f:
        f.write(password + "\\n")
    return "Password stored"

@app.route('/redundant_code')
def redundant_code():
    x = 1 + 1
    x = 2 + 2
    return "Redundant code executed"

if __name__ == '__main__':
    app.run(debug=True)
"""

# Write the script to a file
output_path = "/mnt/data/full_vulnerable_script.py"
with open(output_path, 'w') as f:
    f.write(full_vulnerable_script)

output_path

