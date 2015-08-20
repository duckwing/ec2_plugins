import os, tempfile
from concurrent.futures import ProcessPoolExecutor

def isolate(functor, *args):
    with ProcessPoolExecutor(1) as pool:
        with tempfile.TemporaryDirectory(dir='.') as temp_dir:
            f =  pool.submit(_run_isolated, temp_dir, functor, *args)
            f.result()

def test_isolate():
    isolate(_isolator_test_reporter)

def _isolator_test_reporter():
    print('Isolated with PID {} and DIR {}'
          .format(os.getpid(), os.getcwd()))

def _run_isolated(tdir, functor, *args):
    os.chdir(tdir)
    return functor(*args)
