from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

# Template folder set karna
app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def home():
    # Ye line zaroori hai: Design dikhane ke liye
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url')
    format_type = data.get('type', 'video')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best'
    else:
        ydl_opts['format'] = 'best'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': info.get('url', ''),
                'quality': format_type.upper(),
                'platform': info.get('extractor_key', 'Unknown')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)