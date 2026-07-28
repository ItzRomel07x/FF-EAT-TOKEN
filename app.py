from flask import Flask, request, jsonify, render_template_string
import requests
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

# Premium UI Template
UI_DESIGN = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Access Token Tool | Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #050505;
            color: #ffffff;
            -webkit-font-smoothing: antialiased;
        }
        .main-card {
            background-color: #0f0f0f;
            border-radius: 12px;
        }
        .input-field {
            background-color: #1a1a1a;
            border: none;
            color: #fff;
            font-size: 13px;
        }
        .social-icon {
            background-color: #1a1a1a;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: 0.2s;
        }
        .social-icon:hover {
            background-color: #252525;
        }
        .btn-action {
            background-color: #ffffff;
            color: #000000;
            font-weight: 800;
            letter-spacing: -0.2px;
            transition: 0.2s;
        }
        .btn-action:hover {
            background-color: #e2e2e2;
        }
        .token-box {
            background-color: #141414;
            font-family: monospace;
        }
        /* No borders, no glow as requested */
        * { border: none !important; box-shadow: none !important; outline: none !important; }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-6">

    <div class="main-card w-full max-w-[420px] p-8">
        <!-- Header with Logo -->
        <div class="flex items-center gap-4 mb-10">
            <img src="https://i.ibb.co/Y4KjTgvP/Picsart-26-02-07-02-21-57-621.jpg" alt="Logo" class="w-14 h-14 rounded-lg object-cover">
            <div>
                <h1 class="text-[18px] font-extrabold leading-tight tracking-tight uppercase">FREE FIRE</h1>
                <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">GET EAT TOKEN</p>
            </div>
        </div>

        <!-- Social Login -->
        <div class="flex justify-between mb-8">
            <a href="https://auth.garena.com/universal/oauth?platform=8&response_type=code&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.gid.recargajogo.com.br/oauth/callback_redirect/" target="_blank" class="social-icon"><img src="https://raw.githubusercontent.com/KillerSharmaBot/Eat-Token/refs/heads/main/image/Google.png" class="w-5"></a>
            <a href="https://auth.garena.com/universal/oauth?platform=3&response_type=code&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.gid.recargajogo.com.br/oauth/callback_redirect/" target="_blank" class="social-icon"><img src="https://raw.githubusercontent.com/KillerSharmaBot/Eat-Token/refs/heads/main/image/Facebook.png" class="w-5"></a>
            <a href="https://auth.garena.com/universal/oauth?platform=10&response_type=code&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.gid.recargajogo.com.br/oauth/callback_redirect/" target="_blank" class="social-icon"><i class="fab fa-apple text-white text-lg"></i></a>
            <a href="https://auth.garena.com/universal/oauth?platform=11&response_type=code&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.gid.recargajogo.com.br/oauth/callback_redirect/" target="_blank" class="social-icon"><img src="https://raw.githubusercontent.com/KillerSharmaBot/Eat-Token/refs/heads/main/image/X.png" class="w-5"></a>
            <a href="https://auth.garena.com/universal/oauth?platform=5&response_type=code&client_id=100067&redirect_uri=https://api.ff.garena.co.id/auth/auth/callback_n?site=https://api-discountstore.gid.recargajogo.com.br/oauth/callback_redirect/" target="_blank" class="social-icon"><img src="https://raw.githubusercontent.com/KillerSharmaBot/Eat-Token/refs/heads/main/image/VK.png" class="w-5"></a>
        </div>

        <!-- Input Area -->
        <div class="space-y-4">
            <input type="text" id="tokenInp" placeholder="Paste Eat Link or Token" class="input-field w-full p-4 rounded-lg font-semibold placeholder-gray-600">
            <button onclick="convertToken()" id="btn" class="btn-action w-full py-4 rounded-lg text-[12px] uppercase tracking-tighter">Get Access Token</button>
        </div>

        <!-- Result Area -->
        <div id="outputArea" class="hidden mt-10 space-y-6">
            <div class="flex justify-between items-end border-b border-gray-800 pb-2">
                <span class="text-[10px] font-bold text-gray-500 uppercase">Player Data</span>
                <span id="playerNick" class="text-[12px] font-bold text-white">---</span>
            </div>

            <div class="space-y-2">
                <div class="flex justify-between">
                    <span class="text-[10px] font-bold text-gray-500 uppercase">Access Token</span>
                    <button onclick="copyToken()" class="text-[9px] font-bold text-gray-400 hover:text-white">COPY</button>
                </div>
                <div id="accessToken" class="token-box w-full p-4 rounded-lg text-[11px] font-bold text-white break-all leading-relaxed">
                    ---
                </div>
            </div>
        </div>

        <p class="text-center text-[9px] text-gray-700 mt-10 font-bold uppercase tracking-widest">  </p>
    </div>

    <script>
        async function convertToken() {
            const input = document.getElementById('tokenInp').value;
            const btn = document.getElementById('btn');
            const outputArea = document.getElementById('outputArea');
            const accessTokenDisplay = document.getElementById('accessToken');
            const playerNick = document.getElementById('playerNick');

            if(!input) return;

            btn.innerText = "PROCESSING...";
            btn.disabled = true;

            try {
                const response = await fetch('/convert', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: input})
                });
                const data = await response.json();
                
                outputArea.classList.remove('hidden');
                accessTokenDisplay.innerText = data.access_token || "Invalid Token";
                playerNick.innerText = data.nickname || "Unknown Player";
            } catch (err) {
                alert("Server Error!");
            } finally {
                btn.innerText = "CONVERT TOKEN";
                btn.disabled = false;
            }
        }

        function copyToken() {
            const text = document.getElementById('accessToken').innerText;
            navigator.clipboard.writeText(text);
            alert("Token Copied!");
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(UI_DESIGN)

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    url_input = data.get('url', '')
    
    # Extract eat token if URL is provided
    eat_token = url_input
    if "eat=" in url_input:
        try:
            parsed = urlparse(url_input)
            eat_token = parse_qs(parsed.query).get('eat', [url_input])[0]
        except:
            pass
    
    # API Request to convert Eat to Access
    try:
        api_res = requests.get(f"https://access.killersharmabot.online/access?access_token={eat_token}")
        return jsonify(api_res.json())
    except:
        return jsonify({"error": "API Connection Failed"})

if __name__ == '__main__':
    app.run(debug=True)