from bundle import seeker


def foo():
    raise TypeError('bad')


def bar():
    try:
        foo()
    except Exception:
        str(1)
        raise


@seeker.tracer(depth=3, only_watch=False)
def main():
    try:
        bar()
    except:
        pass


# timestamp is not import but anyway
expected_output = '''
Source path:... Whatever
                call        17 def main():
                line        18     try:
                line        19         bar()
                    call         8 def bar():
                    line         9     try:
                    line        10         foo()
                        call         4 def foo():
                        line         5     raise TypeError('bad')
                        exception    5     raise TypeError('bad')
        TypeError: bad
        Call ended by exception
                    exception   10         foo()
    TypeError: bad
                    line        11     except Exception:
                    line        12         str(1)
                    line        13         raise
    Call ended by exception
                exception   19         bar()
TypeError: bad
                line        20     except:
                line        21         pass
                return      21         pass
Return value:.. None
Elapsed time: 00:00:00.000885
'''
