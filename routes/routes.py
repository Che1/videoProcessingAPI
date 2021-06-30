from uuid import uuid4

from flask import request, abort, Blueprint, jsonify

import faceDetect

faceManeger = faceDetect.FaceDetectManager()

video_bp = Blueprint('video',import_name='video_bp', url_prefix='/processing/video/')

@video_bp.route('/', methods=["POST"])
def upload_video_route():
    if 'video' not in request.files:
        abort(400, {'error': "file named 'video' not found"})
    video = request.files['video']
    uuid = str(uuid4())
    filename = './uploaded-videos/' + uuid
    video.save(filename)

    faceManeger.start_processing_task(filename, uuid)
    return {'video_id': uuid}


@video_bp.route('/', methods=["GET"])
def get_info_route():
    return jsonify({'videos': faceManeger.get_info()})


@video_bp.route('/<id>/cancel/', methods=["POST"])
def stop_proccesing_route(id):
    task_id = id
    faceManeger.cancel_task(task_id)
    return {}, 200
