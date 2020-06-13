from bundle import seeker


@seeker.tracer(depth=2, only_watch=False)
def main():
    f2()


def f2():
    f3()


def f3():
    f4()


@seeker.tracer(depth=2, only_watch=False)
def f4():
    f5()


def f5():
    pass


expected_output = '''
Source path:... Whatever
                call         5 def main():
                line         6     f2()
                    call         9 def f2():
                    line        10     f3()
        Source path:... Whatever
                        call        18 def f4():
                        line        19     f5()
                            call        22 def f5():
                            line        23     pass
                            return      23     pass
            Return value:.. None
                        return      19     f5()
        Return value:.. None
        Elapsed time: 00:00:00.000134
                    return      10     f3()
    Return value:.. None
                return       6     f2()
Return value:.. None
Elapsed time: 00:00:00.000885
'''
