from config import Config

from flask import Flask

from flask_apscheduler import APScheduler

from flask_bootstrap import Bootstrap

from flask_caching import Cache

from flask_fontawesome import FontAwesome

from . import routes
from .middleware import PrefixMiddleware


app = Flask(__name__)
with app.app_context():
    bootstrap = Bootstrap(app)
    fa = FontAwesome(app)
    app.config.from_object(Config)
    cache = Cache(app)
    app.cache = cache
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(routes.app)

    if app.config.get("PROXY_PREFIX"):
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=app.config.get("PROXY_PREFIX").rstrip("/"))
