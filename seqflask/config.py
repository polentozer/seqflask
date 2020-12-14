import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOGGING_CONFIG = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(filename)s %(name)s %(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'filename': 'seqtools.log'
            }
        },
        'loggers': {
            '__main__': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }

