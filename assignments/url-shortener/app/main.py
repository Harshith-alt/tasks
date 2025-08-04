from flask import Flask, request, jsonify, redirect
from utils import generate_short_code, is_valid_url
from models import save_url, get_url, increment_click, get_stats

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')

    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid or missing URL"}), 400

    short_code = generate_short_code()
    save_url(short_code, long_url)

    return jsonify({
        "short_code": short_code,
        "short_url": request.host_url + short_code
    }), 201

@app.route('/<short_code>')
def redirect_short_url(short_code):
    entry = get_url(short_code)
    if entry:
        increment_click(short_code)
        return redirect(entry['long_url'])
    return jsonify({"error": "Short URL not found"}), 404

@app.route('/api/stats/<short_code>')
def stats(short_code):
    entry = get_stats(short_code)
    if entry:
        return jsonify({
            "url": entry['long_url'],
            "clicks": entry['clicks'],
            "created_at": entry['created_at']
        })
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
