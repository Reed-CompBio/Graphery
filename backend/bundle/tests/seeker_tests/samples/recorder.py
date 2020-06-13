from bundle.seeker import tracer


@tracer()
def simple_loop_trace_non():
    for i in range(10):
        pass


@tracer('i')
def simple_loop_trace_index():
    for i in range(10):
        pass


@tracer('i')
def simple_while_loop_trace_index():
    i = 0
    while i < 10:
        pass
