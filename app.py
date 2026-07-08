from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import os

app = Flask(__name__, instance_path='/tmp/instance')

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def receive_cookie():
    cookies = request.cookies
    get_params = request.args.to_dict()
    
    if request.is_json:
        post_data = request.get_json(silent=True)
    else:
        post_data = request.form.to_dict()

    if not post_data and request.data:
        try:
            post_data = json.loads(request.data)
        except:
            post_data = {"raw_data": request.data.decode('utf-8', errors='ignore')}

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),  # <-- Fixed: lowercase 'utc'
        "cookies": cookies,
        "get_params": get_params,
        "post_data": post_data,
        "headers": dict(request.headers),
        "remote_addr": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    }

    print("=" * 70)
    print(f"📩 DATA RECEIVED at {log_entry['timestamp']}")
    print(f"🌐 From IP: {request.remote_addr}")
    print(f"🖥️  User-Agent: {request.headers.get('User-Agent')}")
    print("-" * 70)
    
    if cookies:
        print(f"🍪 COOKIES FOUND: {json.dumps(cookies, indent=2)}")
    else:
        print("🍪 No cookies found in the request.")
    
    if get_params:
        print(f"📦 GET PARAMETERS: {json.dumps(get_params, indent=2)}")
    
    if post_data:
        print(f"📨 POST DATA: {json.dumps(post_data, indent=2)}")
    
    print("=" * 70)

    return jsonify({
        "status": "success",
        "message": "Cookie received successfully!",
        "received": {
            "cookies": cookies,
            "params": get_params,
            "data": post_data
        }
    }), 200

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Cookie')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
