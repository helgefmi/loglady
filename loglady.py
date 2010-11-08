import os
import datetime

class LogLady:
    def __init__(self, path, levels, append=False, format=None):
        levels = set(levels)
        default_format = '[%(date)s] [%(level)' + str(max(map(len, levels))) + 's]: %(message)s'

        assert type(path) == str
        assert os.path.isdir(path)
        assert 'all' not in levels

        self.format = format or default_format
        self.logfiles = {}

        levels.add('all')
        for level in levels:
            self.logfiles[level] = open(os.path.join(path, level) + '.log', append and 'a' or 'w')

    def __getattr__(self, key):
        levels = self.logfiles.keys()
        if key.lower() not in (level.lower() for level in levels):
            raise Exception('Invalid logtype: %s. This logger instance supports the following levels: %s.' % (key, ', '.join(levels)))

        def logfn(msg):
            format_dict = {
                'message': msg,
                'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'level': key
            }
            msg = (self.format % format_dict).rstrip('\n') + '\n'
            self.logfiles[key].write(msg)
            self.logfiles[key].flush()
            self.logfiles['all'].write(msg)
            self.logfiles['all'].flush()

        return logfn

    def close(self):
        for logfile in self.logfiles.values():
            logfile.close()

def test():
    TEST_PATH = '/tmp/loglady_testing'
    MESSAGES = (
        ('debug', (
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur semper imperdiet hendrerit. Praesent et lectus mauris. Praesent euismod mauris ligula.',
            'enatis euismod vulputate in, blandit vel orci. Nam egestas auctor nunc eu ultricies.',
            'Quisque tempus aliquet sapien, et hendrerit arcu ultrices ut. Cras placerat aliquam bibendum. Maecenas lobortis, dui sed tempor egestas, risus risus facilisis dolor, vel iaculis lorem magna sed libero.',
        )),
        ('test', (
            'Vivamus et ante ut lacus adipiscing mattis.',
            'Donec vestibulum facilisis dolor, ultrices condimentum neque eleifend et.',
            'lectus ligula luctus elit,'
        )),
        ('error', (
            'Maecenas sit amet ligula libero. ',
            '   ',
            '\x00\x01\x02\x03abc\x04\xff\xfe123\xfd\xfc\x00',
        )),
    )

    if not os.path.isdir(TEST_PATH):
        os.mkdir(TEST_PATH)

    levels = [level for level, _ in MESSAGES]
    logger = LogLady(TEST_PATH, levels, append=False, format='%(message)s')

    for level, messages in MESSAGES:
        for message in messages:
            getattr(logger, level)(message)

    logger.close()

    for level, messages in MESSAGES:
        path = os.path.join(TEST_PATH, level) + '.log'
        assert os.path.isfile(path)
        assert open(path, 'r').read() == ('\n'.join(messages) + '\n'), level
        os.remove(path)
    os.remove(os.path.join(TEST_PATH, 'all') + '.log')
    os.rmdir(TEST_PATH)

if __name__ == '__main__':
    test()
