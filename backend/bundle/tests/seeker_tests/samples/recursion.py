from bundle import seeker


@seeker.tracer(depth=2, only_watch=False)
def factorial(x):
    if x <= 1:
        return 1
    return mul(x, factorial(x - 1))


def mul(a, b):
    return a * b


def main():
    factorial(4)


expected_output = '''
Source path:... Whatever
Starting var:.. x = 4
                call         5 def factorial(x):
                line         6     if x <= 1:
                line         8     return mul(x, factorial(x - 1))
    Starting var:.. x = 3
                    call         5 def factorial(x):
                    line         6     if x <= 1:
                    line         8     return mul(x, factorial(x - 1))
        Starting var:.. x = 2
                        call         5 def factorial(x):
                        line         6     if x <= 1:
                        line         8     return mul(x, factorial(x - 1))
            Starting var:.. x = 1
                            call         5 def factorial(x):
                            line         6     if x <= 1:
                            line         7         return 1
                            return       7         return 1
            Return value:.. 1
            Elapsed time: 00:00:00.000092
            Starting var:.. a = 2
            Starting var:.. b = 1
                            call        11 def mul(a, b):
                            line        12     return a * b
                            return      12     return a * b
            Return value:.. 2
                        return       8     return mul(x, factorial(x - 1))
        Return value:.. 2
        Elapsed time: 00:00:00.000283
        Starting var:.. a = 3
        Starting var:.. b = 2
                        call        11 def mul(a, b):
                        line        12     return a * b
                        return      12     return a * b
        Return value:.. 6
                    return       8     return mul(x, factorial(x - 1))
    Return value:.. 6
    Elapsed time: 00:00:00.000468
    Starting var:.. a = 4
    Starting var:.. b = 6
                    call        11 def mul(a, b):
                    line        12     return a * b
                    return      12     return a * b
    Return value:.. 24
                return       8     return mul(x, factorial(x - 1))
Return value:.. 24
Elapsed time: 00:00:00.000760
'''
