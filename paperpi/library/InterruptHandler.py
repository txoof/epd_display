#!/usr/bin/env python3
# coding: utf-8




import logging
import signal






logger = logging.getLogger(__name__)






class InterruptHandler(object):
    '''catch SIGINT and SIGTERM gracefully for terminating long-running process or loops
    
        see: https://stackoverflow.com/a/35798485/5530152
    
        EXAMPLE:
            counter = 0
            with InterruptHandler() as h:
                while True:
                    # long running process/loop here
                    counter += 1
                    print(counter)
                    time.sleep(0.25)

                    if h.interrupted:
                        print('interrupted')
                        break
            print('cleanup happens here')
            print(f'I counted {counter} times')
    
    '''
    def __init__(self, signals=(signal.SIGINT, signal.SIGTERM)):
        self.signals = signals
        self.original_handlers = {}

    def __enter__(self):
        self.interrupted = False
        self.released = False

        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self.handler)

        return self

    def handler(self, signum, frame):
        self.release()
        self.interrupted = True

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False

        for sig in self.signals:
            signal.signal(sig, self.original_handlers[sig])

        self.released = True
        return True






class SIGINT_handler():
    def __init__(self):
        self.SIGINT = False

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self.SIGINT = True




