from flask import Flask
from celery import Celery, Task
from src.blueprint.wx_blueprint import wx_blueprint
from src.worker import wx_task
from src.worker import *
from src.db import *

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs:object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def create_app() -> Flask:
    app = Flask("LNSFOCOLNS", static_folder="./static")
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://127.0.0.1:63789/0",
            result_backend="redis://127.0.0.1:63789/0",
            task_ignore_result=True
        ),
    )
    app.config.from_prefixed_env()
    celery_init_app(app)
    return app

app = create_app()
app.register_blueprint(wx_blueprint)
celery = app.extensions["celery"]

scheduled = celery.control.inspect().scheduled()
if scheduled is None or len(scheduled) == 0:
    wx_task.fresh_wx_access_token.apply_async(countdown=5)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

