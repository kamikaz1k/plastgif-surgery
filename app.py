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
app.config['PUBLIC_FOLDER'] = './public'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def createShoop(request):

    gif_img = request.files['gif-img']
    face_img = request.files['face-img']

    if not gif_img or not face_img:
        return []

    # timestamp = str(round(time.time() * 1000)) + "-"
    # gif_img_filename, gif_img_filepath = saveImage(gif_img, timestamp)
    # face_img_filename, face_img_filepath = saveImage(face_img, timestamp)
    gif_img_filename, face_img_filename = saveInputPictures(gif_img, face_img)

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

def savePicsFromRequest(request):

    gif_img = request.files['gif-img']
    face_img = request.files['face-img']

    if not gif_img or not face_img:
        return []

    gif_img_filename, face_img_filename = saveInputPictures(gif_img, face_img)

    return {
        'gif_url': url_for('uploads', filename=gif_img_filename),
        'face_url': url_for('uploads', filename=face_img_filename)
    }

def saveInputPictures(gif_img, face_img):

    timestamp = str(round(time.time() * 1000)) + "-"
    gif_img_filename, gif_img_filepath = saveImage(gif_img, timestamp)
    face_img_filename, face_img_filepath = saveImage(face_img, timestamp)

    return gif_img_filename, face_img_filename

def breakdownFramesWithFaces(gif_url):

    gif_img_filepath = getFilepathFromUrl(gif_url)

    frames = face_swap.getFrames(gif_img_filepath)
    faces = [face_swap.findFaces(frame) for frame in frames]

    return [
        buildFrameFaceDict(
            # url_for('uploads', filename=frame_filename_list[idx]),
            frames[idx].meta['duration']/1000,
            *faces[idx][0]
        )
        for idx in range(len(frames))
    ]

def getFilepathFromUrl(public_upload_file_url):
    url_prefix = url_for('uploads', filename="")
    filename = public_upload_file_url.replace(url_prefix, "")
    return os.path.join(app.config['UPLOAD_FOLDER'], filename)

def buildFrameFaceDict(duration, face_box_x, face_box_y, face_box_w, face_box_h):
    return {
        # 'url': url,
        'face_box_x': int(face_box_x),
        'face_box_y': int(face_box_y),
        'face_box_w': int(face_box_w),
        'face_box_h': int(face_box_h),
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

@app.route("/breakdown", methods=["GET", "POST"])
def breakdown():

    if request.method == "GET":
        return render_template("upload-breakdown.html")

    url_dict = savePicsFromRequest(request)

    return redirect(url_for('breakdown_edit', gif=url_dict['gif_url'], face=url_dict['face_url']))

@app.route("/breakdown/edit", methods=["GET"])
def breakdown_edit():

    gif_url = request.args.get('gif')
    face_url = request.args.get('face')
    # import pdb; pdb.set_trace()
    # frames = breakdownFramesWithFaces(gif_url)
    frames = [{"duration":0.03,"face_box_h":73,"face_box_w":73,"face_box_x":286,"face_box_y":148},{"duration":0.03,"face_box_h":75,"face_box_w":75,"face_box_x":271,"face_box_y":147},{"duration":0.03,"face_box_h":77,"face_box_w":77,"face_box_x":257,"face_box_y":146},{"duration":0.03,"face_box_h":79,"face_box_w":79,"face_box_x":256,"face_box_y":145},{"duration":0.03,"face_box_h":80,"face_box_w":80,"face_box_x":244,"face_box_y":145},{"duration":0.03,"face_box_h":80,"face_box_w":80,"face_box_x":235,"face_box_y":143},{"duration":0.03,"face_box_h":79,"face_box_w":79,"face_box_x":232,"face_box_y":140},{"duration":0.03,"face_box_h":79,"face_box_w":79,"face_box_x":232,"face_box_y":140},{"duration":0.03,"face_box_h":72,"face_box_w":72,"face_box_x":240,"face_box_y":139},{"duration":0.03,"face_box_h":75,"face_box_w":75,"face_box_x":239,"face_box_y":138},{"duration":0.03,"face_box_h":73,"face_box_w":73,"face_box_x":253,"face_box_y":136},{"duration":0.03,"face_box_h":68,"face_box_w":68,"face_box_x":269,"face_box_y":139},{"duration":0.03,"face_box_h":67,"face_box_w":67,"face_box_x":285,"face_box_y":139},{"duration":0.03,"face_box_h":68,"face_box_w":68,"face_box_x":299,"face_box_y":141},{"duration":0.03,"face_box_h":69,"face_box_w":69,"face_box_x":298,"face_box_y":141},{"duration":0.03,"face_box_h":64,"face_box_w":64,"face_box_x":314,"face_box_y":147},{"duration":0.03,"face_box_h":65,"face_box_w":65,"face_box_x":324,"face_box_y":149},{"duration":0.03,"face_box_h":73,"face_box_w":73,"face_box_x":307,"face_box_y":148},{"duration":0.03,"face_box_h":72,"face_box_w":72,"face_box_x":298,"face_box_y":151}]

    return render_template(
        "breakdown.htm.j2",
        gif_url=gif_url,
        face_url=face_url,
        frames=frames,
        framesJson=json.dumps(frames)
    )

@app.route("/build", methods=["POST"])
def build():
    path_to_built_gif = buildGifFromBreakdown(request)
    return

@app.route("/uploads/<filename>", methods=["GET"])
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/public/<filename>", methods=["GET"])
def public(filename):
    return send_from_directory(app.config['PUBLIC_FOLDER'], filename)


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
