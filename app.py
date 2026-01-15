from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "StreamSnap Engine v3 (Quality Select) is Running!"

@app.route('/get-video', methods=['POST'])
def get_video():
    data = request.get_json()
    url = data.get('url')
    # Frontend se check karein ke user ne "video" manga hai ya "audio"
    format_type = data.get('type', 'video') 
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    # Basic Settings
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'geo_bypass': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    # Agar User ko AUDIO chahiye
    if format_type == 'audio':
        ydl_opts['format'] = 'bestaudio/best' # Sirf Audio dhoondo
    else:
        # Agar User ko VIDEO chahiye (Default)
        # 'best' ka matlab: Video + Audio (Single file) jo best quality mein ho
        ydl_opts['format'] = 'best' 

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return jsonify({
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': info.get('url', ''),
                'quality': format_type.upper(), # Batayega ke Audio hai ya Video
                'platform': info.get('extractor_key', 'Unknown')
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)