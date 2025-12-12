import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from config import Config


def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


def _setup_email_handler(app):
    """Configure email handler for error logging."""
    mail_server = app.config.get('MAIL_SERVER')
    if not mail_server:
        return
    
    auth = None
    mail_username = app.config.get('MAIL_USERNAME')
    mail_password = app.config.get('MAIL_PASSWORD')
    if mail_username or mail_password:
        auth = (mail_username, mail_password)
    
    secure = () if app.config.get('MAIL_USE_TLS') else None
    mail_port = app.config.get('MAIL_PORT')
    admins = app.config.get('ADMINS')
    
    mail_handler = SMTPHandler(
        mailhost=(mail_server, mail_port),
        fromaddr=f'no-reply@{mail_server}',
        toaddrs=admins,
        subject='Microblog Failure',
        credentials=auth,
        secure=secure
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)


def _setup_logging_handlers(app):
    """Configure logging handlers (file or stdout)."""
    if app.config.get('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)
        
        file_handler = RotatingFileHandler(
            'logs/microblog.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


def _configure_production_logging(app):
    """Configure logging for production environment."""
    _setup_email_handler(app)
    _setup_logging_handlers(app)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


def _register_blueprints(app):
    """Register all application blueprints."""
    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.cli import bp as cli_bp
    from app.api import bp as api_bp
    
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(cli_bp)
    app.register_blueprint(api_bp, url_prefix='/api')


def _initialize_extensions(app):
    """Initialize Flask extensions."""
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    babel.init_app(app, locale_selector=get_locale)


def _configure_external_services(app):
    """Configure Elasticsearch, Redis, and task queue."""
    elasticsearch_url = app.config.get('ELASTICSEARCH_URL')
    app.elasticsearch = Elasticsearch([elasticsearch_url]) if elasticsearch_url else None
    
    redis_url = app.config.get('REDIS_URL')
    app.redis = Redis.from_url(redis_url)
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    _initialize_extensions(app)
    _configure_external_services(app)
    _register_blueprints(app)

    if not app.debug and not app.testing:
        _configure_production_logging(app)

    return app


from app import models
