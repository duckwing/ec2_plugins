import os, sys, tempfile

def isolate(functor, *args):
    child_pid = os.fork()
    if child_pid > 0:
        print('Forked off {}'.format(child_pid))
        child_pid2, ret_code = os.wait()
        assert child_pid2 == child_pid
        print('Child {} finished with exit code {}'
              .format(child_pid, ret_code))
        return ret_code

    with tempfile.TemporaryDirectory(dir='.') as temp_dir:
        base_dir = os.getcwd()
        os.chdir(temp_dir)
        try:
            sys.exit(functor(*args))
        finally:
            os.chdir(base_dir)

def test_isolate():
    def reporter():
        print('Isolated with PID {} and DIR {}'
              .format(os.getpid(), os.getcwd()))
    isolate(reporter)
