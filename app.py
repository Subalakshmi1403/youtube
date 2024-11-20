import logging

from flask import send_from_directory
from werkzeug.utils import secure_filename

from modules.libraries import *
from modules.config import Props

app=Flask(__name__)

DOWNLOAD_FOLDER="downloads"

# Ensure the download folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def LoggerObject():
    Today=datetime.now().strftime("%Y-%m-%d")
    log_file_name=Props.LOGS_PATH+"downloads%s.log" % Today
    logging.basicConfig(filename=log_file_name,format='%(asctime)s %(message)s',filemode="a")
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return logger

YOUTUBE_URL_PATTERN = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'

@app.route('/')
def index():
    logger=LoggerObject()

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
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            downloaded_filename = ydl.prepare_filename(info)

        # Sanitize filename before returning it
        sanitized_filename = sanitize_filename(os.path.basename(downloaded_filename))

        # Rename the file to the sanitized version
        os.rename(downloaded_filename, os.path.join(Props.DOWNLOAD_PATH, sanitized_filename))

        return render_template('download.html', filename=sanitized_filename)

    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/get-video/<filename>')
def get_video(filename):
    logger = LoggerObject()
    safe_filename = secure_filename(filename)
    file_path = os.path.join(Props.DOWNLOAD_PATH, safe_filename)

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return f"Error: The requested file could not be found.", 404

    return send_from_directory(Props.DOWNLOAD_PATH, safe_filename)





if __name__=="__main__":
    app.run(debug=True)