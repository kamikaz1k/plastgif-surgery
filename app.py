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
import face_swap

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

    if not gif_img or not face_img:
        return []

    timestamp = str(round(time.time() * 1000)) + "-"
    gif_img_filename, gif_img_filepath = saveImage(gif_img, timestamp)
    face_img_filename, face_img_filepath = saveImage(face_img, timestamp)

    output_file_name = timestamp + "output"
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file_name)

    output_file_path = plastgifSurgery(gif_img_filepath, face_img_filepath, output_file_path)
    output_file_name = output_file_name + "." + output_file_path.split(".")[-1]

    filenames = [
        url_for('uploads', filename=gif_img_filename),
        url_for('uploads', filename=face_img_filename),
        url_for('uploads', filename=output_file_name)
    ]

    return filenames

def breakdownFramesWithFaces(request):

    gif_img = request.files['gif-img']
    face_img = request.files['face-img']
    filenames = []

    if not gif_img or not face_img:
        return filenames

    timestamp = str(round(time.time() * 1000)) + "-"
    gif_img_filename, gif_img_filepath = saveImage(gif_img, timestamp)
    face_img_filename, face_img_filepath = saveImage(face_img, timestamp)

    frames = face_swap.getFrames(gif_img_filepath)
    faces = [face_swap.findFaces(frame) for frame in frames]

    filename_components = gif_img_filename.split(".")
    path_components = gif_img_filepath.split(".")
    filename_components.insert(-1, "0")
    path_components.insert(-1, "0")
    frame_filename_list = []

    for idx, frame in enumerate(frames):
        frame_num = str(idx)
        frame_num.zfill(3)
        path_components[-2] = frame_num
        filename_components[-2] = frame_num

        frame_file_path = ".".join(path_components)
        face_swap.saveGifImage(image=frame, imagePath=frame_file_path)
        frame_filename_list.append(".".join(filename_components))

    return [
        buildFrameFaceDict(
            url_for('uploads', filename=frame_filename_list[idx]),
            frames[idx].meta['duration']/1000,
            *faces[idx][0]
        )
        for idx in range(len(frames))
    ]

def buildFrameFaceDict(url, duration, face_box_x, face_box_y, face_box_w, face_box_h):
    return {
        'url': url,
        'face_box_x': face_box_x,
        'face_box_y': face_box_y,
        'face_box_w': face_box_w,
        'face_box_h': face_box_h,
        'duration': duration
    }

def saveImage(file, prepend_name_with=""):
    filename = prepend_name_with + secure_filename(file.filename)
    image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_file_path)
    return filename, image_file_path

@app.route("/", methods=["GET"])
def main():
    return render_template("upload.html")

@app.route("/", methods=["POST"])
def upload():
    files_names = createShoop(request)
    return render_template("success.html", images=files_names)

@app.route("/surgery", methods=["POST"])
def surgery():
    files_names = createShoop(request)
    return json.dumps({"url": files_names[2]})

@app.route("/breakdown", methods=["GET"])
def breakdown():
    return render_template("upload-breakdown.html")

@app.route("/breakdown", methods=["POST"])
def breakdown_frames():
    frames = breakdownFramesWithFaces(request)
    # frames = {
    #     'url', 'face_box_x', 'face_box_y', 'face_box_w', 'face_box_h', 'duration'
    # }
    # error msg?
    return render_template(
        "breakdown.htm.j2",
        frames=frames
    )

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