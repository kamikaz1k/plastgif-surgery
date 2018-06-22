import datetime
import os
import re
import time

from flask import (
    Flask,
    render_template,
    json,
    request,
    redirect,
    session,
    url_for,
    send_from_directory
)
from werkzeug.utils import secure_filename

from face_swap import plastgifSurgery

# from flask_socketio import SocketIO, emit

# App Configurations
app = Flask(__name__)
app.config["DEBUG"] = True
# socketio = SocketIO(app)

app.config['UPLOAD_FOLDER'] = './public/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def createShoop(request):

    gif_img = request.files['gif-img']
    face_img = request.files['face-img']
    files_names = []

    if gif_img and face_img:#and allowed_file(file.filename):
        timestamp = str(round(time.time() * 1000)) + "-"
        filename = timestamp + secure_filename(gif_img.filename)
        imagePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        gif_img.save(imagePath)
        files_names.append(url_for('uploads', filename=filename))

        filename = timestamp + secure_filename(face_img.filename)
        facePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        face_img.save(facePath)
        files_names.append(url_for('uploads', filename=filename))

        outputFileName = timestamp + "output"
        outputPath = os.path.join(app.config['UPLOAD_FOLDER'], outputFileName)

        outputPath = plastgifSurgery(imagePath, facePath, outputPath)
        outputFileName = outputFileName + "." + outputPath.split(".")[-1]

        files_names.append(url_for('uploads', filename=outputFileName, _external=True))

    return files_names


@app.route("/", methods=["GET"])
def main():
    return render_template(
        "upload.html",
       title="Title",
       msg="My Msg"
    )

@app.route("/", methods=["POST"])
def upload():
    files_names = createShoop(request)
    return render_template(
        "success.html",
        msg="Success",
        images=files_names
    )


@app.route("/surgery", methods=["POST"])
def surgery():
    files_names = createShoop(request)
    return json.dumps({"url": files_names[2]})


@app.route("/uploads/<filename>", methods=["GET"])
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

### Websockets Handlers
# @socketio.on('connect')
# def handle_connect(connect):
#     print('received connect: ' + connect)
#     emit('message', 'you are connected')

# @socketio.on('disconnect')
# def handle_disconnect(disconnect):
#     print('received disconnect: ' + disconnect)

# @socketio.on('message')
# def handle_message(message):
#     # print('received message: ' + message)
#     emit('message', "thanks")

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
