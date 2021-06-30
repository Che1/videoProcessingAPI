import celery

celery_app = celery.Celery(
    'myTasks',
    broker='pyamqp://guest@localhost//',
    backend='redis://localhost',
    include=['background_tasks.tasks']
)
