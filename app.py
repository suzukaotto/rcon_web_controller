from flask import Flask, request, render_template, redirect, url_for, session
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import os
import mcrcon
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')

MC_RCON_IP = os.getenv('RCON_IP', '127.0.0.1')
MC_RCON_PORT = int(os.getenv('RCON_PORT', 25575))
MC_RCON_PASSWORD = os.getenv('RCON_PASSWORD', 'default_rcon_password')

DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = '12431243'

ADMIN_USERNAME_HASH = generate_password_hash(os.getenv('ADMIN_USERNAME', DEFAULT_ADMIN_USERNAME))
ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv('ADMIN_PASSWORD_HASH', DEFAULT_ADMIN_PASSWORD))

# Minecraft formatting codes to HTML styles
color_codes = {
    '§0': 'color-black',
    '§1': 'color-dark_blue',
    '§2': 'color-dark_green',
    '§3': 'color-dark_aqua',
    '§4': 'color-dark_red',
    '§5': 'color-dark_purple',
    '§6': 'color-gold',
    '§7': 'color-gray',
    '§8': 'color-dark_gray',
    '§9': 'color-blue',
    '§a': 'color-green',
    '§b': 'color-aqua',
    '§c': 'color-red',
    '§d': 'color-light_purple',
    '§e': 'color-yellow',
    '§f': '',
    '§l': 'bold',
    '§m': 'strikethrough',
    '§n': 'underline',
    '§o': 'italic',
    '§r': 'reset'
}

def minecraft_to_html(text):
    html_text = ""
    codes = re.split(r'(§.)', text)
    active_styles = []

    for code in codes:
        if code in color_codes:
            if code == '§r':
                active_styles.clear()
            else:
                active_styles.append(color_codes[code])
        else:
            if active_styles:
                html_text += f'<span class="{" ".join(active_styles)}">{code}</span>'
            else:
                html_text += code

    return html_text

def send_rcon_command(command):
    try:
        with mcrcon.MCRcon(MC_RCON_IP, MC_RCON_PASSWORD, port=MC_RCON_PORT) as mcr:
            response = mcr.command(command)
        return response
    except Exception as e:
        return f"Error: {e}"

def login_required(f):
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', error='로그인 후 작업하세요.'))
    wrap.__name__ = f.__name__
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = request.args.get('error')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_password_hash(ADMIN_USERNAME_HASH, username) and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for('index', error=error))
        else:
            error = '로그인 정보를 확인하세요.'
            return redirect(url_for('login', error=error))
        
    if error == None:
        error = '로그인 하세요.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login', error='로그아웃되었습니다.'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    response = ""
    if request.method == 'POST':
        command = request.form['command']
        response = send_rcon_command(command)
        response = minecraft_to_html(response)  # Convert Minecraft formatting to HTML
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=SERVER_PORT)
