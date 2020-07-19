from bundle.seeker import tracer

# check if it's evaluation first or inspection first? I bet it's evaluation first,
# so I need to prepare the store space for the next line. ANSWER: no I don't need prepare a new dict
# but the evaluation does come first, the the 'access' field comes after.
# I need the make access a dict, since there may be multiple accesses in one line

# use just one tracer instance or multiple tracer instance?
# I support multiple tracers
# 1. pro: easier to manage con: may affect coding styles
# 2. pro: users have more controls to their codes.
#    con: multiple watch list is difficult for users to manage

# TODO what python version to support?


class TempClass:
    recorder = tracer.get_recorder()

    def __init__(self):
        self.value = 0

    @tracer.look_at
    def get_value(self):
        # TODO warp all the record write/read into functions, since the number of fields is limited
        # TempClass.recorder.add_ac_to_last_record('get value %s' % self.value)
        return self.value

    # TODO in the graph objects, I think you can start will getters first.
    #  setters can wait
    # TODO create a decorator that does this
    @tracer.look_at
    def set_value(self, value):
        # TODO same as noted above
        # TempClass.recorder.add_ac_to_last_record('set value %s' % self.value)
        self.value = value


def depth_func(a):
    a *= a
    for i in range(a):
        pass


@tracer('s', 'a', 'adsfa', depth=2)
def fun(a, b):
    depth_func(a)
    temp = TempClass()
    s = temp.get_value()
    for i in range(a * b):
        s += i * i
        temp.set_value(s)

    @tracer('k')
    def hh(k):
        print(k)
        if k == 1:
            return 1
        return hh(k-2) + 1

    return s, hh


# TODO manually inputting variables is not a efficient way.
@tracer('c', 'ik')
def foo(c, d, e):
    ik = 1
    while ik < c * d * e:
        ik += 3

    return ik


@tracer('tk', 'c', custom_repr=[(TempClass, lambda x: str(x) + ' hhh')])
def obj_try(c):
    tk = TempClass()
    # TODO may be add a change flag to record so that when objects are modified through accessors,
    #  the behaviors are recorded?
    tk.set_value(c)
    return tk


if __name__ == '__main__':
    re, boo = fun(2, 3)
    boo(re)
    foo(2, 3, 4)
    obj_try(10)
    tracer_list = tracer.get_recorder_change_list()
    print(tracer_list)
