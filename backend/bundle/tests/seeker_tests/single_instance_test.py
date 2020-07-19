from bundle.seeker import tracer

tr = tracer()
# check if it's evaluation first or inspection first? I bet it's evaluation first,
# so I need to prepare the store space for the next line

# use just one tracer instance or multiple tracer instance?
# 1. pro: easier to manage con: may affect coding styles
# 2. pro: users have more controls to their codes.
#    con: multiple watch list is difficult for users to manage


@tr
def fun(a, b):
    s = 0
    for i in range(a * b):
        s += i * i
    @tr
    def hh(k):
        if k == 1:
            return 1
        return hh(k-2) + 1

    return s, hh


@tr
def foo(c, d, e):
    s = 1
    while s < c * d * e:
        s += 3

    return s


if __name__ == '__main__':
    s, hh = fun(2, 3)
    hh(s)
    foo(2, 3, 4)
    tracer_list = tracer.get_recorder_change_list()
    print(tracer_list)
