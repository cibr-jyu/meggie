""" je suis un chat """

from Queue import Queue
from Queue import Empty
from multiprocessing.pool import ThreadPool
from time import sleep
from sys import exc_info

def threaded(func):
    def decorated(*args, **kwargs):
        pool = ThreadPool(processes=1)
        do_meanwhile = kwargs.pop('do_meanwhile', None)
        bucket = Queue()

        def exception_wrapper():
            try:
                result = func(*args, **kwargs)
            except:
                bucket.put(exc_info())
            return result

        async_result = pool.apply_async(exception_wrapper)
        while True:
            try:
                exc = bucket.get(block=False)
                raise exc[0], exc[1].message, exc[2]
            except Empty:
                pass
            if async_result.ready():
                break
            if do_meanwhile:
                do_meanwhile()
            sleep(0.2)

        return async_result.get()
    return decorated
