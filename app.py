import logging

from flask import send_from_directory
from werkzeug.utils import secure_filename

from modules.libraries import *
from modules.config import Props

app=Flask(__name__)


YOUTUBE_URL_PATTERN = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'

@app.route('/')
def index():

    return render_template('index.html')

def sanitize_filename(filename):
    return secure_filename(filename)

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url')
    if not video_url:
        return "Error: Please provide a video URL.", 400

    if not re.match(YOUTUBE_URL_PATTERN, video_url):
        return "Error: The entered URL is not a valid YouTube video link.", 400

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': Props.DOWNLOAD_PATH + '%(title)s.%(ext)s',
            'cookiefile': 'cookies.txt',  # Make sure cookies.txt is in your project directory
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_filename = ydl.prepare_filename(info)

        sanitized_filename = sanitize_filename(os.path.basename(downloaded_filename))
        os.rename(downloaded_filename, os.path.join(Props.DOWNLOAD_PATH, sanitized_filename))

        return render_template('download.html', filename=sanitized_filename)

    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        return f"Error: {str(e)}", 500
@app.route('/get-video/<filename>')
def get_video(filename):

    safe_filename = secure_filename(filename)
    file_path = os.path.join(Props.DOWNLOAD_PATH, safe_filename)

    if not os.path.exists(file_path):

        return f"Error: The requested file could not be found.", 404

    return send_from_directory(Props.DOWNLOAD_PATH, safe_filename)





if __name__=="__main__":
    app.run(debug=True)