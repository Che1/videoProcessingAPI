from abc import ABC
from celery.result import AsyncResult

from background_tasks.tasks import process_video


class TasksDataRepository(ABC):
    def __init__(self):
        pass

    def save_task(self, id):
        raise NotImplemented()

    def get_task_info_by_id(self, id):
        raise NotImplemented()

    def get_all_tasks_info(self):
        raise NotImplemented()

    def delete_task_by_id(self, id):
        raise NotImplemented()


class InMemoryDataRep(TasksDataRepository):
    data = dict()

    def save_task(self, id):
        self.data[id] = {}

    def get_task_info_by_id(self, id):
        raise NotImplemented()

    def get_all_tasks_info(self):
        info_list = []
        for id in self.data:
            res: AsyncResult = process_video.AsyncResult(id)
            info: dict = res.info
            info['id'] = id
            info['status'] = res.status
            info_list.append(info)
        return info_list

    def delete_task_by_id(self, id):
        raise NotImplemented()


class FaceDetectManager:

    def __init__(self, data_repo=InMemoryDataRep()):
        self.data_repository = data_repo

    def start_processing_task(self, filename, id):
        task = process_video.apply_async(kwargs={'filename':filename}, task_id=id)
        self.data_repository.save_task(task.id)

    def cancel_task(self, task_id):
        res: AsyncResult = process_video.AsyncResult(task_id)
        res.revoke(terminate=True)
        # todo remove file associated with task

    def get_info(self):
        return self.data_repository.get_all_tasks_info()
