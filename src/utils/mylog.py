from functools import wraps
import time
from pathlib import Path
from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG
from logging.handlers import HTTPHandler


class SlackHandler(HTTPHandler):
    def __init__(self, host, url, token, channel, username):
        super().__init__(host, url, method='POST', secure=True)
        self._token = token
        self._channel = channel
        self._username = username

    def mapLogRecord(self, record):
        ret = {
            "token": self._token,
            "channel": self._channel,
            "text": self.format(record),
            "username": self._username
        }
        return ret

    def setFormatter(self, formatter):
        self.formatter = formatter

    def setLevel(self, level):
        self.level = level


def create_logger(type, config):
    '''
    This is a method to initialize logger for specified type and config.
    To initialize logger:
        create_logger('fizz', LogConfig())
    To get logger:
        from logging import getLogger
        logger_fizz = getLogger('fizz')
    '''
    c = config
    if type == 'main':
        formatter = Formatter('%(asctime)s - %(levelname)-5s >> %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        logger_ = getLogger(type)
        log_file = Path(c.LOGDIR / 'main' / (c.LOGFILE + '.log')).resolve()
    elif type == 'train':
        formatter = Formatter()
        logger_ = getLogger(type)
        log_file = Path(c.LOGDIR / 'train' / (c.LOGFILE + '.tsv')).resolve()
    else:
        raise Exception

    Path.mkdir(c.LOGDIR, exist_ok=True, parents=True)

    logger_.setLevel(DEBUG)

    file_handler = FileHandler(log_file, '+w')
    file_handler.setLevel(c.FILE_HANDLER_LEVEL)
    file_handler.setFormatter(formatter)

    stream_handler = StreamHandler()
    stream_handler.setLevel(c.STREAM_HANDLER_LEVEL)
    stream_handler.setFormatter(formatter)

    if c.slackauth.NO_SEND_MESSAGE:
        token = None
    else:
        token = __read_token(c.slackauth.TOKEN_PATH)

    slack_handler = SlackHandler(
        host=c.slackauth.HOST,
        url=c.slackauth.URL,
        channel=c.slackauth.CHANNEL,
        token=token,
        username='LogBot')
    slack_handler.setLevel(c.SLACK_HANDLER_LEVEL)
    slack_handler.setFormatter(formatter)

    logger_.addHandler(file_handler)
    logger_.addHandler(stream_handler)
    logger_.addHandler(slack_handler)


def __read_token(token_path):
    token = None
    if not token_path.exists():
        return None
    with open(token_path, 'r') as f:
        token = f.read()
    token = token.replace('\n', '')
    return token


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = getLogger('main')
        method_name = func.__qualname__
        start = time.time()
        text = f'Start {method_name}'
        logger.info(text)

        '''
        text = f'{method_name} args: \n {args[:]}'
        logger.debug(text)

        text = f'{method_name} kwargs: \n kwargs: \n {kwargs.items()}'
        logger.debug(text)
        '''

        result = func(*args, **kwargs)
        elapsed_time = int(time.time() - start)
        minutes, sec = divmod(elapsed_time, 60)
        hour, minutes = divmod(minutes, 60)
        text = f'End   {method_name}: [elapsed] >> {hour:0>2}:{minutes:0>2}:{sec:0>2}'
        logger.info(text)

        return result
    return wrapper
