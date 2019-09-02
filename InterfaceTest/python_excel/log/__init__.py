import  logging.config
import datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
run_file = sys.argv[0]
run_file_name = os.path.basename(os.path.splitext(run_file)[0])
print(run_file_name)
log_name = run_file_name+datetime.datetime.now().strftime('%Y%m%d')+'.log'
LOG_DIR = os.path.join(BASE_DIR,log_name)
print(LOG_DIR)
LOGGING={
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(levelname)s] [%(pathname)s] [%(funcName)s ][%(name)s:%(lineno)d]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },

        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "simple",
            "filename": LOG_DIR,
            'mode': 'w+',
            "maxBytes": 1024*1024*1024,  # 5 MB
            "backupCount": 20,
            "encoding": "utf8"
        },
    },

    "loggers": {
        "app_name": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        'handlers': ['default'],
        'level': "INFO",
        'propagate': False
    }
}

logging.config.dictConfig(LOGGING)