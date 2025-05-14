
import os
import sqlite3
import pickle
import jwt
import requests
import urllib.request
from flask import Flask, request, redirect, make_response

app = Flask(__name__)

# 1. SQL Injection
@app.route('/sql_injection')
def sql_injection():
    username = request.args.get('username')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '%s'" % username)
    return str(cursor.fetchall())

# 2. Command Injection
@app.route('/command_injection')
def command_injection():
    cmd = request.args.get('cmd')
    return os.popen(cmd).read()

# 3. Unsafe Deserialization
@app.route('/unsafe_deserialization')
def unsafe_deserialization():
    data = request.args.get('data')
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

# 4. Remote Code Execution (RCE)
@app.route('/rce')
def rce():
    code = request.args.get('code')
    exec(code)
    return "Executed"

# 5. SSRF (Server Side Request Forgery)
@app.route('/ssrf')
def ssrf():
    url = request.args.get('url')
    response = urllib.request.urlopen(url)
    return response.read()

# 6. Path Traversal
@app.route('/path_traversal')
def path_traversal():
    filename = request.args.get('filename')
    with open(filename, 'r') as f:
        return f.read()

# 7. Insecure JWT
@app.route('/insecure_jwt')
def insecure_jwt():
    payload = {"user": "admin"}
    token = jwt.encode(payload, '1234', algorithm='HS256')
    return token

# 8. Sensitive Data Exposure
@app.route('/sensitive_data_exposure')
def sensitive_data_exposure():
    return "Credit Card Number: 4111-1111-1111-1111"

# 9. Open Redirect
@app.route('/open_redirect')
def open_redirect():
    url = request.args.get('url')
    return redirect(url)

# 10. Hardcoded Secret
@app.route('/hardcoded_secret')
def hardcoded_secret():
    return "SECRET_KEY=supersecretkey123"

if __name__ == '__main__':
    app.run(debug=True)
