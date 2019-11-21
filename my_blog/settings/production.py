from .base import *

DEBUG = False

EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 与SMTP服务器通信时，是否启动SSL安全链接
EMAIL_USE_SSL = True
#前缀
EMAIL_SUBJECT_PREFIX = '[QHL Blog]'


# 管理员邮箱设置
ADMINS = (
    ('admin', config('ADMIN_EMAIL')),
)

# 日志模块logging的配置
LOGGING = {
    'version': 1,  # 指明dictConfig的版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    # 根日志默认日志级别
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'log_file'],
    },
    # 格式化器, 指明了最终输出中日志记录的布局
    'formatters': {
        'verbose': {
            # [时间] 日志级别 [日志对象名称.日志记录所在的函数名.日志记录所在的行号.文件名部分名称] [具体的日志信息]
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d %(module)s] %(message)s',
        }
    },
    # 过滤器, 提供了更好的粒度控制,它可以决定输出哪些日志记录。
    'filters': {
        # 判断settings的DEBUG是否开启
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器,用来定义具体处理日志的方式，可以定义多种，"default"就是默认方式，"console"就是打印到控制台方式。file是写入到文件的方式，注意使用的class不同
    'handlers': {
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 与default相同
            'filename': '/home/my_blog.log',  # 日志输出文件
            'maxBytes': 16777216,  # 16MB
            'formatter': 'verbose'  # 制定输出的格式，注意 在上面的formatter配置里面选择一个，否则会报错
        },
        'console': {
            'level': 'DEBUG',
            # settings的DEBUG开启时才放行
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # 将 DEBUG 以上的日志写到 /dev/null 黑洞
        'null': {
            'class': 'logging.NullHandler',
        },
        # settings的DEBUG为false时，将所有 ERROR 以上的日志邮件发送给站点管理员，当
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        # 将所有 INFO 以上的日志，发送类 console 和 mail_admins 处理其，也就是说 INFO 以上的会打印到控制台，并输入到日志文件
        'my_blog': {
            'handlers': ['log_file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        # 将所有 ERROR 以上的日志写到 mail_admins 处理器，而且不再冒泡，也就是说 django 这个 logger 不会接到 django.request 产生的日志信息
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
