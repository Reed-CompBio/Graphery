# Copyright 2019 Ram Rachum and collaborators.
# This program is distributed under the MIT license.

import io
import textwrap
import threading
import time
import sys

from bundle.seeker.utils import truncate
import pytest

from bundle import seeker
# from bundle import seeker
from bundle.seeker.variables import needs_parentheses
from .utils import (assert_output, assert_sample_output, VariableEntry,
                    CallEntry, LineEntry, ReturnEntry, ReturnValueEntry, ExceptionEntry, ExceptionValueEntry,
                    SourcePathEntry, CallEndedByExceptionEntry,
                    ElapsedTimeEntry)
from . import mini_toolbox

from importlib import import_module


@pytest.fixture()
def long_arr_value():
    return '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, ' \
           '26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, ' \
           '50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, ' \
           '74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, ' \
           '98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, ' \
           '117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, ' \
           '136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, ' \
           '155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, ' \
           '174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, ' \
           '193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, ' \
           '212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, ' \
           '231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, ' \
           '250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, ' \
           '269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, ' \
           '288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, ' \
           '307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, ' \
           '326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, ' \
           '345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, ' \
           '364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, ' \
           '383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, ' \
           '402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, ' \
           '421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, ' \
           '440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, ' \
           '459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, ' \
           '478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, ' \
           '497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, ' \
           '516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, ' \
           '535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, ' \
           '554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, ' \
           '573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, ' \
           '592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, ' \
           '611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, ' \
           '630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, ' \
           '649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, ' \
           '668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, ' \
           '687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, ' \
           '706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, ' \
           '725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, ' \
           '744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, ' \
           '763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, ' \
           '782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, ' \
           '801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, ' \
           '820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, ' \
           '839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, ' \
           '858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, ' \
           '877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, ' \
           '896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, ' \
           '915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, ' \
           '934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, ' \
           '953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, ' \
           '972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, ' \
           '991, 992, 993, 994, 995, 996, 997, 998, 999]'


def test_string_io_no_watch():
    string_io = io.StringIO()

    @seeker.tracer(output=string_io)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            LineEntry('y = 8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        )
    )


def test_string_io_one_entry():
    string_io = io.StringIO()

    @seeker.tracer('foo', output=string_io)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            LineEntry('y = 8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        )
    )


def test_string_io_multiple_entries():
    string_io = io.StringIO()

    @seeker.tracer('foo', 'x', 'y', output=string_io)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            VariableEntry('x', '7'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        )
    )


def test_callable_watch_all():
    string_io = io.StringIO()

    def write(msg):
        string_io.write(msg)

    @seeker.tracer(only_watch=False, output=write)
    def my_function(foo):
        x = 7
        y = 9
        return y + x

    result = my_function('beebeebooboo')
    assert result == 16
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'beebeebooboo'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            VariableEntry('x', '7'),
            LineEntry('y = 9'),
            VariableEntry('y', '9'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('16'),
            ElapsedTimeEntry(),
        )
    )


def test_relative_time():
    snoop = seeker.tracer(only_watch=False, relative_time=True)

    def foo(x):
        if x == 0:
            bar1(x)
            qux()
            return

        with snoop:
            # There should be line entries for these three lines,
            # no line entries for anything else in this function,
            # but calls to all bar functions should be traced
            foo(x - 1)
            bar2(x)
            qux()
        int(4)
        bar3(9)
        return x

    @snoop
    def bar1(_x):
        qux()

    @snoop
    def bar2(_x):
        qux()

    @snoop
    def bar3(_x):
        qux()

    def qux():
        time.sleep(0.1)
        return 9  # not traced, mustn't show up

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = foo(2)
    assert result == 2
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            # In first with
            SourcePathEntry(),
            VariableEntry('x', '2'),
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            LineEntry('foo(x - 1)'),

            # In with in recursive call
            VariableEntry('x', '1'),
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            LineEntry('foo(x - 1)'),

            # Call to bar1 from if block outside with
            VariableEntry('_x', '0'),
            VariableEntry('qux'),
            CallEntry('def bar1(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(0.1),

            # In with in recursive call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '1'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(0.1),

            # In with in recursive call
            LineEntry('qux()'),
            ElapsedTimeEntry(0.4),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(0.1),

            # -- Similar to previous few sections,
            # -- but from first call to foo

            # In with in first call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '2'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(0.1),

            # In with in first call
            LineEntry('qux()'),
            ElapsedTimeEntry(0.7),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(0.1),
        ),
    )


def test_thread_info():
    @seeker.tracer(only_watch=False, thread_info=True)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function('baba')
    assert result == 15
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry('x = 7'),
            VariableEntry('x', '7'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + x'),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        )
    )


def test_multi_thread_info():
    @seeker.tracer(only_watch=False, thread_info=True)
    def my_function(foo):
        x = 7
        y = 8
        return y + x

    def parse_call_content(line):
        return line.split('{event:9} '.format(event='call'))[-1]

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        my_function('baba')
        t1 = threading.Thread(target=my_function, name="test123", args=['bubu'])
        t1.start()
        t1.join()
        t1 = threading.Thread(target=my_function, name="bibi", args=['bibi'])
        t1.start()
        t1.join()
    output = output_capturer.string_io.getvalue()
    calls = [line for line in output.split("\n") if "call" in line]
    main_thread = calls[0]
    assert parse_call_content(main_thread) == parse_call_content(calls[1])
    assert parse_call_content(main_thread) == parse_call_content(calls[2])
    thread_info_regex = '([0-9]+-{name}+[ ]+)'
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):',
                      thread_info_regex=thread_info_regex.format(
                          name="MainThread")),
            LineEntry('x = 7',
                      thread_info_regex=thread_info_regex.format(
                          name="MainThread")),
            VariableEntry('x', '7'),
            LineEntry('y = 8',
                      thread_info_regex=thread_info_regex.format(
                          name="MainThread")),
            VariableEntry('y', '8'),
            LineEntry('return y + x',
                      thread_info_regex=thread_info_regex.format(
                          name="MainThread")),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
            VariableEntry('foo', value_regex="u?'bubu'"),
            CallEntry('def my_function(foo):',
                      thread_info_regex=thread_info_regex.format(
                          name="test123")),
            LineEntry('x = 7',
                      thread_info_regex=thread_info_regex.format(
                          name="test123")),
            VariableEntry('x', '7'),
            LineEntry('y = 8',
                      thread_info_regex=thread_info_regex.format(
                          name="test123")),
            VariableEntry('y', '8'),
            LineEntry('return y + x',
                      thread_info_regex=thread_info_regex.format(
                          name="test123")),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
            VariableEntry('foo', value_regex="u?'bibi'"),
            CallEntry('def my_function(foo):',
                      thread_info_regex=thread_info_regex.format(name='bibi')),
            LineEntry('x = 7',
                      thread_info_regex=thread_info_regex.format(name='bibi')),
            VariableEntry('x', '7'),
            LineEntry('y = 8',
                      thread_info_regex=thread_info_regex.format(name='bibi')),
            VariableEntry('y', '8'),
            LineEntry('return y + x',
                      thread_info_regex=thread_info_regex.format(name='bibi')),
            ReturnEntry('return y + x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        )
    )


def test_watch_only():
    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @seeker.tracer(
        'foo.x',
        'io.__name__',
        'len(foo.__dict__["x"] * "abc")',
    )
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('io.__name__', "'io'"),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo.x', '2'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '6'),
            LineEntry(),
            LineEntry(),
            VariableEntry('foo.x', '4'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '12'),
            LineEntry(),
            LineEntry(),
            VariableEntry('foo.x', '16'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '48'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_watch_all():
    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @seeker.tracer(
        'foo.x',
        'io.__name__',
        'len(foo.__dict__["x"] * "abc")',
        only_watch=False,
    )
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('Foo'),
            VariableEntry('io.__name__', "'io'"),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            VariableEntry('foo.x', '2'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '6'),
            LineEntry(),
            VariableEntry('i', '0'),
            LineEntry(),
            VariableEntry('foo.x', '4'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '12'),
            LineEntry(),
            VariableEntry('i', '1'),
            LineEntry(),
            VariableEntry('foo.x', '16'),
            VariableEntry('len(foo.__dict__["x"] * "abc")', '48'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_watch_explode_only():
    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # thoughts what is list + []?
    @seeker.tracer(watch_explode=('_d', '_point', 'lst'))
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _point = Foo(x=3, y=4)
        lst = [7, 8, 9]
        lst.append(10)

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            VariableEntry("_d['c']", "'ignore'"),
            LineEntry(),
            VariableEntry('_point'),
            VariableEntry('_point.x', '3'),
            VariableEntry('_point.y', '4'),
            LineEntry(),
            VariableEntry('lst'),
            VariableEntry('lst[0]', '7'),
            VariableEntry('lst[1]', '8'),
            VariableEntry('lst[2]', '9'),
            # VariableEntry('lst'),
            LineEntry(),
            VariableEntry('lst'),
            VariableEntry('lst[3]', '10'),
            # VariableEntry('lst'),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_watch_explode_with_others():
    class Foo:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    @seeker.tracer(watch_explode=('_d', '_point', 'lst + []'), only_watch=False)
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _point = Foo(x=3, y=4)
        lst = [7, 8, 9]
        lst.append(10)

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('Foo'),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            VariableEntry("_d['c']", "'ignore'"),
            LineEntry(),
            VariableEntry('_point'),
            VariableEntry('_point.x', '3'),
            VariableEntry('_point.y', '4'),
            LineEntry(),
            VariableEntry('lst'),
            VariableEntry('(lst + [])[0]', '7'),
            VariableEntry('(lst + [])[1]', '8'),
            VariableEntry('(lst + [])[2]', '9'),
            VariableEntry('lst + []'),
            LineEntry(),
            VariableEntry('lst'),
            VariableEntry('(lst + [])[3]', '10'),
            VariableEntry('lst + []'),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_variables_classes_only():
    class WithSlots(object):
        __slots__ = ('x', 'y')

        def __init__(self):
            self.x = 3
            self.y = 4

    @seeker.tracer(
        seeker.Keys('_d', exclude='c'),
        seeker.Attrs('_d'),  # doesn't have attributes
        seeker.Attrs('_s'),
        seeker.Indices('_lst')[-3:],
    )
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _s = WithSlots()
        _lst = list(range(1000))

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            LineEntry(),
            VariableEntry('_s'),
            VariableEntry('_s.x', '3'),
            VariableEntry('_s.y', '4'),
            LineEntry(),
            VariableEntry('_lst'),
            VariableEntry('_lst[997]', '997'),
            VariableEntry('_lst[998]', '998'),
            VariableEntry('_lst[999]', '999'),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_variables_classes_with_others():
    class WithSlots(object):
        __slots__ = ('x', 'y')

        def __init__(self):
            self.x = 3
            self.y = 4

    @seeker.tracer(
        seeker.Keys('_d', exclude='c'),
        seeker.Attrs('_d'),  # doesn't have attributes
        seeker.Attrs('_s'),
        seeker.Indices('_lst')[-3:],
        only_watch=False
    )
    def my_function():
        _d = {'a': 1, 'b': 2, 'c': 'ignore'}
        _s = WithSlots()
        _lst = list(range(1000))

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('WithSlots'),
            CallEntry('def my_function():'),
            LineEntry(),
            VariableEntry('_d'),
            VariableEntry("_d['a']", '1'),
            VariableEntry("_d['b']", '2'),
            LineEntry(),
            VariableEntry('_s'),
            VariableEntry('_s.x', '3'),
            VariableEntry('_s.y', '4'),
            LineEntry(),
            VariableEntry('_lst'),
            VariableEntry('_lst[997]', '997'),
            VariableEntry('_lst[998]', '998'),
            VariableEntry('_lst[999]', '999'),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_single_keyword_watch_no_comma_only():
    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @seeker.tracer(watch='foo')
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_single_watch_no_comma_only():
    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @seeker.tracer('foo')
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_single_keyword_watch_no_comma_with_others():
    class Foo(object):
        def __init__(self):
            self.x = 2

        def square(self):
            self.x **= 2

    @seeker.tracer(watch='foo', only_watch=False)
    def my_function():
        foo = Foo()
        for i in range(2):
            foo.square()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('Foo'),
            CallEntry('def my_function():'),
            LineEntry('foo = Foo()'),
            VariableEntry('foo'),
            LineEntry(),
            VariableEntry('i', '0'),
            LineEntry(),
            LineEntry(),
            VariableEntry('i', '1'),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_long_variable(long_arr_value):
    @seeker.tracer('foo')
    def my_function():
        foo = list(range(1000))
        return foo

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result == list(range(1000))
    output = output_capturer.string_io.getvalue()
    regex = r'^(?=.{100}$)\[0, 1, 2, .*\.\.\..*, 997, 998, 999\]$'

    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('foo = list(range(1000))'),
            VariableEntry('foo', value=long_arr_value),
            LineEntry(),
            ReturnEntry(),
            # TODO use shortish value or use original value
            ReturnValueEntry(value_regex=regex),
            ElapsedTimeEntry(),
        ),
    )


def test_long_variable_with_custom_max_variable_length(long_arr_value):
    @seeker.tracer('foo', max_variable_length=200)
    def my_function():
        foo = list(range(1000))
        return foo

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result == list(range(1000))
    output = output_capturer.string_io.getvalue()
    regex = r'^(?=.{200}$)\[0, 1, 2, .*\.\.\..*, 997, 998, 999\]$'
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('foo = list(range(1000))'),
            VariableEntry('foo', value=long_arr_value),
            LineEntry(),
            ReturnEntry(),
            # TODO here is a bug, if you don't specify 'foo' in watch, the return value is a full0-length arr
            #  however, it you do specify the watch value, the return is a shortish repr
            ReturnValueEntry(value_regex=regex),
            ElapsedTimeEntry(),
        ),
    )


def test_long_variable_with_infinite_max_variable_length():
    @seeker.tracer('foo', max_variable_length=None)
    def my_function():
        foo = list(range(1000))
        return foo

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result == list(range(1000))
    output = output_capturer.string_io.getvalue()
    # TODO LMAO, I definitely need to learn regular exp
    regex = r'^(?=.{1000,100000}$)\[0, 1, 2, [^.]+ 997, 998, 999\]$'
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('foo = list(range(1000))'),
            VariableEntry('foo', value_regex=regex),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry(value_regex=regex),
            ElapsedTimeEntry(),
        ),
    )


def test_repr_exception():
    class Bad(object):
        def __repr__(self):
            1 / 0

    @seeker.tracer('bad')
    def my_function():
        bad = Bad()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = my_function()
    assert result is None
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry('def my_function():'),
            LineEntry('bad = Bad()'),
            # TODO should I change the bad repr thing?
            VariableEntry('bad', value='REPR FAILED'),
            ReturnEntry(),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_depth():
    string_io = io.StringIO()

    def f4(x4):
        result4 = x4 * 2
        return result4

    def f3(x3):
        result3 = f4(x3)
        return result3

    def f2(x2):
        result2 = f3(x2)
        return result2

    @seeker.tracer(output=string_io, depth=3, only_watch=False)
    def f1(x1):
        result1 = f2(x1)
        return result1

    result = f1(10)
    assert result == 20
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry(),
            VariableEntry(),
            CallEntry('def f1(x1):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f2(x2):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f3(x3):'),
            LineEntry(),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),
            ElapsedTimeEntry(),
        ),
    )


@pytest.mark.skip(reason='Use custom prefix as identifier')
def test_method_and_prefix():
    class Baz(object):
        def __init__(self):
            self.x = 2

        @seeker.tracer(watch=('self.x',), prefix='ZZZ', only_watch=False)
        def square(self):
            foo = 7
            self.x **= 2
            return self

    baz = Baz()

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = baz.square()
    assert result is baz
    assert result.x == 4
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(prefix='ZZZ'),
            VariableEntry('self', prefix='ZZZ'),
            VariableEntry('self.x', '2', prefix='ZZZ'),
            CallEntry('def square(self):', prefix='ZZZ'),
            LineEntry('foo = 7', prefix='ZZZ'),
            VariableEntry('foo', '7', prefix='ZZZ'),
            LineEntry('self.x **= 2', prefix='ZZZ'),
            VariableEntry('self.x', '4', prefix='ZZZ'),
            LineEntry(prefix='ZZZ'),
            ReturnEntry(prefix='ZZZ'),
            ReturnValueEntry(prefix='ZZZ'),
            ElapsedTimeEntry(prefix='ZZZ'),
        ),
        prefix='ZZZ',
    )


def test_file_output():
    with mini_toolbox.create_temp_folder(prefix='seeker') as folder:
        path = folder / 'foo.log'

        @seeker.tracer(output=path, only_watch=False)
        def my_function(_foo):
            x = 7
            y = 8
            return y + x

        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert_output(
            output,
            (
                SourcePathEntry(),
                VariableEntry('_foo', value_regex="u?'baba'"),
                CallEntry('def my_function(_foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
                ElapsedTimeEntry(),
            ),
        )


def test_confusing_decorator_lines():
    string_io = io.StringIO()

    def empty_decorator(function):
        return function

    @empty_decorator
    @seeker.tracer('foo', 'x', 'y', 'bar', output=string_io, depth=2)  # Multi-line decorator for extra confusion!
    @empty_decorator
    @empty_decorator
    def my_function(foo):
        x = lambda bar: 7
        y = 8
        return y + x(foo)

    result = my_function('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_function(foo):'),
            LineEntry(),
            VariableEntry(),
            LineEntry(),
            VariableEntry(),
            LineEntry(),
            # inside lambda
            VariableEntry('bar', value_regex="u?'baba'"),
            CallEntry('x = lambda bar: 7'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('7'),
            # back in my_function
            ReturnEntry(),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        ),
    )


def test_lambda():
    string_io = io.StringIO()
    my_function = seeker.tracer('x', output=string_io)(lambda x: x ** 2)
    result = my_function(7)
    assert result == 49
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('x', '7'),
            CallEntry(source_regex='^my_function = seeker.*'),
            LineEntry(source_regex='^my_function = seeker.*'),
            ReturnEntry(source_regex='^my_function = seeker.*'),
            ReturnValueEntry('49'),
            ElapsedTimeEntry(),
        ),
    )


def test_unavailable_source():
    with mini_toolbox.create_temp_folder(prefix='seeker') as folder, \
            mini_toolbox.TempSysPathAdder(str(folder)):
        module_name = 'iaerojajsijf'
        python_file_path = folder / ('%s.py' % (module_name,))
        # ideas: this is import, you can use the same method to import modules!!!
        content = textwrap.dedent(u'''
            from bundle import seeker
            from bundle.GraphObjects.Node import Node
            node = Node('1')
            @seeker.tracer(only_watch=False)
            def f(x):
                return x
            node_id_list = [1, 2, 5, 7, 11]
            node_list = []
            for node_id in node_id_list:
                node_list.append(Node(node_id))
        ''')
        with python_file_path.open('w') as python_file:
            python_file.write(content)
        module = import_module(module_name)
        python_file_path.unlink()
        with mini_toolbox.OutputCapturer(stdout=False,
                                         stderr=True) as output_capturer:
            result = getattr(module, 'f')(7)
            node = getattr(module, 'node_list')
        assert result == 7
        assert str(node) == '[Node(id: 1), Node(id: 2), Node(id: 5), Node(id: 7), Node(id: 11)]'
        output = output_capturer.output
        assert_output(
            output,
            (
                SourcePathEntry(),
                VariableEntry(stage='starting'),
                CallEntry('SOURCE IS UNAVAILABLE'),
                LineEntry('SOURCE IS UNAVAILABLE'),
                ReturnEntry('SOURCE IS UNAVAILABLE'),
                ReturnValueEntry('7'),
                ElapsedTimeEntry(),
            )
        )


def test_no_overwrite_by_default():
    with mini_toolbox.create_temp_folder(prefix='seeker') as folder:
        path = folder / 'foo.log'
        with path.open('w') as output_file:
            output_file.write(u'lala')

        @seeker.tracer(output=str(path), only_watch=False)
        def my_function(foo):
            x = 7
            y = 8
            return y + x

        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert output.startswith('lala')
        shortened_output = output[4:]
        assert_output(
            shortened_output,
            (
                SourcePathEntry(),
                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
                ElapsedTimeEntry(),
            )
        )


def test_overwrite():
    with mini_toolbox.create_temp_folder(prefix='seeker') as folder:
        path = folder / 'foo.log'
        with path.open('w') as output_file:
            output_file.write(u'lala')

        @seeker.tracer(output=str(path), overwrite=True, only_watch=False)
        def my_function(foo):
            x = 7
            y = 8
            return y + x

        result = my_function('baba')
        result = my_function('baba')
        assert result == 15
        with path.open() as output_file:
            output = output_file.read()
        assert 'lala' not in output
        assert_output(
            output,
            (
                SourcePathEntry(),
                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
                ElapsedTimeEntry(),

                VariableEntry('foo', value_regex="u?'baba'"),
                CallEntry('def my_function(foo):'),
                LineEntry('x = 7'),
                VariableEntry('x', '7'),
                LineEntry('y = 8'),
                VariableEntry('y', '8'),
                LineEntry('return y + x'),
                ReturnEntry('return y + x'),
                ReturnValueEntry('15'),
                ElapsedTimeEntry(),
            )
        )


def test_error_in_overwrite_argument():
    with mini_toolbox.create_temp_folder(prefix='seeker') as folder:
        with pytest.raises(Exception, match='can only be used when writing'):
            @seeker.tracer(overwrite=True, only_watch=False)
            def my_function(foo):
                x = 7
                y = 8
                return y + x


def test_needs_parentheses():
    assert not needs_parentheses('x')
    assert not needs_parentheses('x.y')
    assert not needs_parentheses('x.y.z')
    assert not needs_parentheses('x.y.z[0]')
    assert not needs_parentheses('x.y.z[0]()')
    assert not needs_parentheses('x.y.z[0]()(3, 4 * 5)')
    assert not needs_parentheses('foo(x)')
    assert not needs_parentheses('foo(x+y)')
    assert not needs_parentheses('(x+y)')
    assert not needs_parentheses('[x+1 for x in ()]')
    assert needs_parentheses('x + y')
    assert needs_parentheses('x * y')
    assert needs_parentheses('x and y')
    assert needs_parentheses('x if z else y')


def test_with_block():
    # Testing that a single Tracer can handle many mixed uses
    snoop = seeker.tracer(only_watch=False)

    def foo(x):
        if x == 0:
            bar1(x)
            qux()
            return

        with snoop:
            # There should be line entries for these three lines,
            # no line entries for anything else in this function,
            # but calls to all bar functions should be traced
            foo(x - 1)
            bar2(x)
            qux()
        int(4)
        bar3(9)
        return x

    @snoop
    def bar1(_x):
        qux()

    @snoop
    def bar2(_x):
        qux()

    @snoop
    def bar3(_x):
        qux()

    def qux():
        return 9  # not traced, mustn't show up

    with mini_toolbox.OutputCapturer(stdout=False,
                                     stderr=True) as output_capturer:
        result = foo(2)
    assert result == 2
    output = output_capturer.string_io.getvalue()
    assert_output(
        output,
        (
            # In first with
            SourcePathEntry(),
            VariableEntry('x', '2'),
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            LineEntry('foo(x - 1)'),

            # In with in recursive call
            VariableEntry('x', '1'),
            VariableEntry('bar1'),
            VariableEntry('bar2'),
            VariableEntry('bar3'),
            VariableEntry('foo'),
            VariableEntry('qux'),
            VariableEntry('snoop'),
            LineEntry('foo(x - 1)'),

            # Call to bar1 from if block outside with
            VariableEntry('_x', '0'),
            VariableEntry('qux'),
            CallEntry('def bar1(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # In with in recursive call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '1'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # In with in recursive call
            LineEntry('qux()'),
            ElapsedTimeEntry(),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # -- Similar to previous few sections,
            # -- but from first call to foo

            # In with in first call
            LineEntry('bar2(x)'),

            # Call to bar2 from within with
            VariableEntry('_x', '2'),
            VariableEntry('qux'),
            CallEntry('def bar2(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # In with in first call
            LineEntry('qux()'),
            ElapsedTimeEntry(),

            # Call to bar3 from after with
            VariableEntry('_x', '9'),
            VariableEntry('qux'),
            CallEntry('def bar3(_x):'),
            LineEntry('qux()'),
            ReturnEntry('qux()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_with_block_depth():
    string_io = io.StringIO()

    def f4(x4):
        result4 = x4 * 2
        return result4

    def f3(x3):
        result3 = f4(x3)
        return result3

    def f2(x2):
        result2 = f3(x2)
        return result2

    def f1(x1):
        str(3)
        with seeker.tracer(output=string_io, depth=3, only_watch=False):
            result1 = f2(x1)
        return result1

    result = f1(10)
    assert result == 20
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry(),
            VariableEntry(),
            # the next line corresponds to normalize = true and we don't have normalize in the
            # with block in f1()
            # VariableEntry(),
            VariableEntry(),
            LineEntry('result1 = f2(x1)'),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f2(x2):'),
            LineEntry(),

            VariableEntry(),
            VariableEntry(),
            CallEntry('def f3(x3):'),
            LineEntry(),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),

            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('20'),
            ElapsedTimeEntry(),
        ),
    )


def test_cellvars():
    string_io = io.StringIO()

    def f2(a):
        def f3(a):
            x = 0
            x += 1

            def f4(a):
                y = x
                return 42

            return f4(a)

        return f3(a)

    def f1(a):
        # the sequence matters here,
        with seeker.tracer('result1', 'f2', 'f3', 'f4', 'a', 'x', 'y', 'string_io', output=string_io, depth=4):
            result1 = f2(a)
        return result1

    result = f1(42)
    assert result == 42
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry(),
            VariableEntry(),
            # again, we don't have normalize here
            # VariableEntry(),
            VariableEntry(),
            LineEntry('result1 = f2(a)'),

            VariableEntry(),
            CallEntry('def f2(a):'),
            LineEntry(),
            VariableEntry(),
            LineEntry(),

            VariableEntry("a"),
            CallEntry('def f3(a):'),
            LineEntry(),
            VariableEntry("x"),
            LineEntry(),
            VariableEntry("x"),
            LineEntry(),
            VariableEntry(),

            LineEntry(),
            VariableEntry(),
            VariableEntry("x"),
            CallEntry('def f4(a):'),
            LineEntry(),
            VariableEntry(),
            LineEntry(),

            ReturnEntry(),
            ReturnValueEntry(),
            ReturnEntry(),
            ReturnValueEntry(),
            ReturnEntry(),
            ReturnValueEntry(),
            ElapsedTimeEntry(),
        ),
    )


def test_var_order():
    string_io = io.StringIO()

    def f(one, two, three, four):
        five = None
        six = None
        seven = None

        five, six, seven = 5, 6, 7

    with seeker.tracer('f', 'string_io', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
                       output=string_io, depth=2):
        result = f(1, 2, 3, 4)

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry(),
            VariableEntry(),
            # again we don't have normalize
            # VariableEntry(),

            LineEntry('result = f(1, 2, 3, 4)'),
            VariableEntry("one", "1"),
            VariableEntry("two", "2"),
            VariableEntry("three", "3"),
            VariableEntry("four", "4"),

            CallEntry('def f(one, two, three, four):'),
            LineEntry(),
            VariableEntry("five"),
            LineEntry(),
            VariableEntry("six"),
            LineEntry(),
            VariableEntry("seven"),
            LineEntry(),
            VariableEntry("five", "5"),
            VariableEntry("six", "6"),
            VariableEntry("seven", "7"),
            ReturnEntry(),
            ReturnValueEntry(),
            ElapsedTimeEntry(),
        ),
    )


def test_truncate():
    max_length = 20
    for i in range(max_length * 2):
        string = i * 'a'
        truncated = truncate(string, max_length)
        if len(string) <= max_length:
            assert string == truncated
        else:
            assert truncated == 'aaaaaaaa...aaaaaaaaa'
            assert len(truncated) == max_length


def test_indentation():
    from .samples import indentation, recursion
    assert_sample_output(indentation)
    assert_sample_output(recursion)


def test_exception():
    from .samples import exception
    assert_sample_output(exception)


def test_generator():
    string_io = io.StringIO()
    original_tracer = sys.gettrace()
    original_tracer_active = lambda: (sys.gettrace() is original_tracer)

    @seeker.tracer(only_watch=False, output=string_io)
    # thoughts: a few pitfalls here
    #   > first, the `original_tracer_active` is not in the function but it's in the functions' closure.
    #   if you want to trace that, `original_tracer_active` should also be included in the watch list
    #   > second, the assertion will also create new variables. In the following code,
    #   `@py_assert1`, and `@py_assert3` are
    def f(x1):
        assert not original_tracer_active()
        x2 = (yield x1)
        assert not original_tracer_active()
        x3 = 'foo'
        assert not original_tracer_active()
        x4 = (yield 2)
        assert not original_tracer_active()
        return

    assert original_tracer_active()
    generator = f(0)
    assert original_tracer_active()
    first_item = next(generator)
    assert original_tracer_active()
    assert first_item == 0
    second_item = generator.send('blabla')
    assert original_tracer_active()
    assert second_item == 2
    with pytest.raises(StopIteration) as exc_info:
        generator.send('looloo')
    assert original_tracer_active()
    # thoughts: interesting

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('x1', '0'),
            VariableEntry(),
            CallEntry(),
            LineEntry(),
            VariableEntry(),
            VariableEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('0'),
            ElapsedTimeEntry(),

            # Pause and resume:

            VariableEntry('x1', '0'),
            VariableEntry(),
            VariableEntry(),
            VariableEntry(),
            CallEntry(),
            VariableEntry('x2', "'blabla'"),
            LineEntry(),
            LineEntry(),
            VariableEntry('x3', "'foo'"),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('2'),
            ElapsedTimeEntry(),

            # Pause and resume:

            VariableEntry('x1', '0'),
            VariableEntry(),
            VariableEntry(),
            VariableEntry(),
            VariableEntry(),
            VariableEntry(),
            CallEntry(),
            VariableEntry('x4', "'looloo'"),
            LineEntry(),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry(None),
            ElapsedTimeEntry(),
        )
    )


def test_custom_repr():
    string_io = io.StringIO()

    def large(l):
        return isinstance(l, list) and len(l) > 5

    def print_list_size(l):
        return 'list(size={})'.format(len(l))

    def print_dict(d):
        return 'dict(keys={})'.format(sorted(list(d.keys())))

    def evil_condition(x):
        return large(x) or isinstance(x, dict)

    @seeker.tracer(output=string_io, custom_repr=(
            (large, print_list_size),
            (dict, print_dict),
            (evil_condition, lambda x: 'I am evil')),
                   only_watch=False)
    def sum_to_x(x):
        l = list(range(x))
        a = {'1': 1, '2': 2}
        return sum(l)

    result = sum_to_x(10000)

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('x', '10000'),
            CallEntry(),
            LineEntry(),
            VariableEntry('l', 'list(size=10000)'),
            LineEntry(),
            VariableEntry('a', "dict(keys=['1', '2'])"),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('49995000'),
            ElapsedTimeEntry(),
        ),
    )


def test_custom_repr_single():
    string_io = io.StringIO()

    @seeker.tracer(output=string_io, custom_repr=(list, lambda l: 'foofoo!'), only_watch=False)
    def sum_to_x(x):
        l = list(range(x))
        return 7

    result = sum_to_x(10000)

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('x', '10000'),
            CallEntry(),
            LineEntry(),
            VariableEntry('l', 'foofoo!'),
            LineEntry(),
            ReturnEntry(),
            ReturnValueEntry('7'),
            ElapsedTimeEntry(),
        ),
    )


def test_disable():
    string_io = io.StringIO()

    def my_function(foo):
        x = 7
        y = 8
        return x + y

    with mini_toolbox.TempValueSetter((seeker.sight, 'DISABLED'), True):
        tracer = seeker.tracer(output=string_io)
        with tracer:
            result = my_function('baba')
        my_decorated_function = tracer(my_function)
        my_decorated_function('booboo')

    output = string_io.getvalue()
    assert not output


# -k 'test_class'
def test_class():
    string_io = io.StringIO()

    @seeker.tracer(output=string_io, only_watch=False)
    class MyClass(object):
        def __init__(self):
            self.x = 7

        def my_method(self, foo):
            y = 8
            return y + self.x

    instance = MyClass()
    result = instance.my_method('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.+MyClass object"),
            CallEntry('def __init__(self):'),
            LineEntry('self.x = 7'),
            ReturnEntry('self.x = 7'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
            VariableEntry('self', value_regex="u?.+MyClass object"),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_method(self, foo):'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + self.x'),
            ReturnEntry('return y + self.x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        ),
    )


def test_class_with_decorated_method():
    string_io = io.StringIO()

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result

        return wrapper

    @seeker.tracer(output=string_io, only_watch=False)
    class MyClass(object):
        def __init__(self):
            self.x = 7

        @decorator
        def my_method(self, foo):
            y = 8
            return y + self.x

    instance = MyClass()
    result = instance.my_method('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.+MyClass object"),
            CallEntry('def __init__(self):'),
            LineEntry('self.x = 7'),
            ReturnEntry('self.x = 7'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
            VariableEntry('args', value_regex=r"\(<.+>, 'baba'\)"),
            VariableEntry('kwargs', value_regex=r"\{\}"),
            VariableEntry('function', value_regex="u?.+my_method"),
            CallEntry('def wrapper(*args, **kwargs):'),
            LineEntry('result = function(*args, **kwargs)'),
            VariableEntry('result', '15'),
            LineEntry('return result'),
            ReturnEntry('return result'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        ),
    )


def test_class_with_decorated_method_and_snoop_applied_to_method():
    string_io = io.StringIO()

    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result

        return wrapper

    @seeker.tracer(output=string_io, only_watch=False)
    class MyClass(object):
        def __init__(self):
            self.x = 7

        @decorator
        @seeker.tracer(output=string_io, only_watch=False)
        def my_method(self, foo):
            y = 8
            return y + self.x

    instance = MyClass()
    result = instance.my_method('baba')
    assert result == 15
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def __init__(self):'),
            LineEntry('self.x = 7'),
            ReturnEntry('self.x = 7'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
            VariableEntry('args', value_regex=r"u?\(<.+>, 'baba'\)"),
            VariableEntry('kwargs', value_regex=r"u?\{\}"),
            VariableEntry('function', value_regex="u?.*my_method"),
            CallEntry('def wrapper(*args, **kwargs):'),
            LineEntry('result = function(*args, **kwargs)'),
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.*MyClass object"),
            VariableEntry('foo', value_regex="u?'baba'"),
            CallEntry('def my_method(self, foo):'),
            LineEntry('y = 8'),
            VariableEntry('y', '8'),
            LineEntry('return y + self.x'),
            ReturnEntry('return y + self.x'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
            VariableEntry('result', '15'),
            LineEntry('return result'),
            ReturnEntry('return result'),
            ReturnValueEntry('15'),
            ElapsedTimeEntry(),
        ),
    )


def test_class_with_property():
    string_io = io.StringIO()

    @seeker.tracer(output=string_io, only_watch=False)
    class MyClass(object):
        def __init__(self):
            self._x = 0

        def plain_method(self):
            pass

        @property
        def x(self):
            self.plain_method()
            return self._x

        @x.setter
        def x(self, value):
            self.plain_method()
            self._x = value

        @x.deleter
        def x(self):
            self.plain_method()
            del self._x

    instance = MyClass()

    # Do simple property operations, make sure we didn't mess up the normal behavior
    result = instance.x
    assert result == instance._x

    instance.x = 1
    assert instance._x == 1

    del instance.x
    with pytest.raises(AttributeError):
        instance._x

    # The property methods will not be traced, but their calls to plain_method will be.
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def __init__(self):'),
            LineEntry('self._x = 0'),
            ReturnEntry('self._x = 0'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # Called from getter
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def plain_method(self):'),
            LineEntry('pass'),
            ReturnEntry('pass'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # Called from setter
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def plain_method(self):'),
            LineEntry('pass'),
            ReturnEntry('pass'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),

            # Called from deleter
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def plain_method(self):'),
            LineEntry('pass'),
            ReturnEntry('pass'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


def test_snooping_on_class_does_not_cause_base_class_to_be_snooped():
    string_io = io.StringIO()

    class UnsnoopedBaseClass(object):
        def __init__(self):
            self.method_on_base_class_was_called = False

        def method_on_base_class(self):
            self.method_on_base_class_was_called = True

    @seeker.tracer(output=string_io, only_watch=False)
    class MyClass(UnsnoopedBaseClass):
        def method_on_child_class(self):
            self.method_on_base_class()

    instance = MyClass()

    assert not instance.method_on_base_class_was_called
    instance.method_on_child_class()
    assert instance.method_on_base_class_was_called

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            VariableEntry('self', value_regex="u?.*MyClass object"),
            CallEntry('def method_on_child_class(self):'),
            LineEntry('self.method_on_base_class()'),
            ReturnEntry('self.method_on_base_class()'),
            ReturnValueEntry('None'),
            ElapsedTimeEntry(),
        ),
    )


@pytest.mark.skip(reason='No normalization')
def test_normalize():
    string_io = io.StringIO()

    class A:
        def __init__(self, a):
            self.a = a

    @seeker.tracer(output=string_io)
    def add():
        a = A(19)
        b = A(22)
        res = a.a + b.a
        return res

    add()
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry('test_pysnooper.py'),
            VariableEntry('A', value_regex=r"<class .*\.A.?>"),
            CallEntry('def add():'),
            LineEntry('a = A(19)'),
            VariableEntry('a', value_regex=r"<.*\.A (?:object|instance)>"),
            LineEntry('b = A(22)'),
            VariableEntry('b', value_regex=r"<.*\.A (?:object|instance)>"),
            LineEntry('res = a.a + b.a'),
            VariableEntry('res', value="41"),
            LineEntry('return res'),
            ReturnEntry('return res'),
            ReturnValueEntry('41'),
            ElapsedTimeEntry(),
        )
    )


@pytest.mark.skip(reason='No normalization')
def test_normalize_prefix():
    string_io = io.StringIO()
    _prefix = 'ZZZZ'

    class A:
        def __init__(self, a):
            self.a = a

    @seeker.tracer(output=string_io, prefix=_prefix, only_watch=False)
    def add():
        a = A(19)
        b = A(22)
        res = a.a + b.a
        return res

    add()
    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(prefix=_prefix),
            VariableEntry('A', value_regex=r"<class .*\.A.?>", prefix=_prefix),
            CallEntry('def add():', prefix=_prefix),
            LineEntry('a = A(19)', prefix=_prefix),
            VariableEntry('a', value_regex=r"<.*\.A (?:object|instance) at 0x[0-9a-z]+>", prefix=_prefix),
            LineEntry('b = A(22)', prefix=_prefix),
            VariableEntry('b', value_regex=r"<.*\.A (?:object|instance) at 0x[0-9a-z]+>", prefix=_prefix),
            LineEntry('res = a.a + b.a', prefix=_prefix),
            VariableEntry('res', value="41", prefix=_prefix),
            LineEntry('return res', prefix=_prefix),
            ReturnEntry('return res', prefix=_prefix),
            ReturnValueEntry('41', prefix=_prefix),
            ElapsedTimeEntry(prefix=_prefix),
        )
    )


@pytest.mark.skip(reason='No normalization')
def test_normalize_thread_info():
    string_io = io.StringIO()

    class A:
        def __init__(self, a):
            self.a = a

    @seeker.tracer(output=string_io, thread_info=True)
    def add():
        a = A(19)
        b = A(22)
        res = a.a + b.a
        return res

    with pytest.raises(NotImplementedError):
        add()


def test_exception():
    string_io = io.StringIO()

    @seeker.tracer(output=string_io, only_watch=False)
    def f():
        x = 8
        raise MemoryError

    with pytest.raises(MemoryError):
        f()

    output = string_io.getvalue()
    assert_output(
        output,
        (
            SourcePathEntry(),
            CallEntry(),
            LineEntry(),
            VariableEntry(),
            LineEntry(),
            ExceptionEntry(),
            ExceptionValueEntry('MemoryError'),
            CallEndedByExceptionEntry(),
            ElapsedTimeEntry(),
        )
    )
