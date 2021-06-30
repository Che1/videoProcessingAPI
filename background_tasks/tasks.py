import cv2
import os

from background_tasks import celery_app

FACE_CASCADE = 'haarcascade_frontalface_alt.xml'


@celery_app.task(name='background_tasks.tasks.process_video', bind=True)
def process_video(self, filename):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + FACE_CASCADE)

    video = cv2.VideoCapture(filename)
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    current_frame = 0
    total_founded_faces = 0
    percentage = -1

    return_data = {'current_progress':0,
                   'result_aggregation':
                       {
                           'faces_count': total_founded_faces
                       }
                   }

    while True:
        current_frame += 1
        is_next_frame_exist, frame = video.read()

        if not is_next_frame_exist:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray
        )

        total_founded_faces += len(faces)

        new_percentage = int(current_frame / total_frames * 100)
        if new_percentage != percentage:
            percentage = new_percentage
            return_data['current_progress'] = percentage
            return_data['result_aggregation']['faces_count'] = total_founded_faces
            self.update_state(state='processing', meta=return_data)
    video.release()
    os.remove(filename)
    return return_data
