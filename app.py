from flask import Flask,render_template,request,send_file, redirect
import os
import sqlite3
import argparse
import socket
# import netifaces


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'


# host = None
# for interface in netifaces.interfaces():
#     addresses = netifaces.ifaddresses(interface)
#     if netifaces.AF_INET in addresses:
#         for addr in addresses[netifaces.AF_INET]:
#             if addr.get('addr') and not addr.get('addr').startswith('127.'):
#                 host = addr['addr']
#                 break
#     if host:
#         break

# if not host:
#     raise RuntimeError('Could not find wireless LAN IP address')





conn = sqlite3.connect('videos.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY, path TEXT)')
conn.commit()
conn.close()
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return 'No video file uploaded'
    
    video_file = request.files['video']
    if video_file.filename == '':
        return 'No video file selected'
    if not allowed_file(video_file.filename):
        return 'Invalid file type. Only MP4, AVI, and MOV video files are allowed.'
    
    filename = video_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_file.save(filepath)
    
    if not os.path.exists(filepath):
        return f'Error: file {filename} was not saved'
    
    save_to_database(filepath)
    
    return render_template('home.html')

def save_to_database(filepath):
    conn = sqlite3.connect('videos.db')
    c = conn.cursor()
    c.execute('INSERT INTO videos (path) VALUES (?)', (filepath,))
    conn.commit()
    conn.close()

# @app.route('/')
# def index():
#     ip_address = request.remote_addr
#     return f"Your IP address is {ip_address}"


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')


@app.route('/v/')
def videoplayer():
    if not request.args.get('url'): return redirect('/')
    return render_template('videoplayer.html', url=request.args.get('url'));


@app.route('/video/playing/<video>')
def playing(video):
    return render_template("videoplayer.html ", host=host, port=port, video=video)


@app.route('/video')
def video():
    filename = request.args.get('filename')
    return send_file("uploads/" + filename, mimetype='video/mp4')

@app.route('/home')
def home():
    videos = os.listdir('C:/Users/flash/Desktop/Project TUBE/uploads')
    return render_template('home.html', host=host, port=port, videos=videos )


@app.route('/upload')
def uploads():
    return render_template('uploads.html')


if __name__ == '__main__':

    host  = '192.168.29.16'
    port = 5000


    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    # ip_address = s.getsockname()[0]
    # s.close()


    # parser = argparse.ArgumentParser()
    # parser.add_argument('--host', default='localhost')
    # parser.add_argument('--port', default='5000')
    # parser.add_argument('--debug', action='store_true')
    # args = parser.parse_args()

app.run(host=host, port=port, debug=True)

    #  app.run(host='192.168.29.16' , port='5000' , debug=True)
    # else  if app.run(host='192.168.29.152' , port='5000' , debug=True)