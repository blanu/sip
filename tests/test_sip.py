import sys

from sip.api import set_port, eval, evalNoun
from testify import TestCase, assert_equal, assert_raises
from iota.api import C
from iota.symbols import  *
import numpy as np # This is just for 32-bit floating-point math

#set_port(sys.argv[1])
set_port("/dev/cu.usbmodem1101")
# set_port("/dev/cu.usbmodem22101")

class NounTests(TestCase):
    def test_small_word(self):
        assert_equal(evalNoun(0), 0)
        assert_equal(evalNoun(1), 1)
        assert_equal(evalNoun(-1), -1)
        assert_equal(evalNoun(256), 256) # requires two bytes
        assert_equal(evalNoun(-256), -256)
        assert_equal(evalNoun(2048), 2048)
        assert_equal(evalNoun(-2048), -2048)
        assert_equal(evalNoun(32768), 32768) # requires two bytes
        assert_equal(evalNoun(-32768), -32768) # requires three bytes
        assert_equal(evalNoun(8388608), 8388608) # requires three bytes
        assert_equal(evalNoun(-8388608), -8388608) # requires three bytes
        assert_equal(evalNoun(16777215), 16777215) # three-byte maxint
        assert_equal(evalNoun(-16777215), -16777215)

    def test_big_word(self):
        assert_equal(evalNoun(2147483648), 2147483648)  # requires 4 bytes
        assert_equal(evalNoun(-2147483648), -2147483648)  # requires 4 bytes
        assert_equal(evalNoun(4294967295), 4294967295) # unsigned 32-bit maxint
        assert_equal(evalNoun(-4294967295), -4294967295)
        assert_equal(evalNoun(549755813888), 549755813888) # requires 5 bytes
        assert_equal(evalNoun(-549755813888), -549755813888) # requires 5 bytes
        assert_equal(evalNoun(10000000000), 10000000000) # too big for 32-bit
        assert_equal(evalNoun(-10000000000), -10000000000)
        assert_equal(evalNoun(9223372036854775807), 9223372036854775807) # signed 64-bit max
        assert_equal(evalNoun(-9223372036854775807), -9223372036854775807) # signed 64-bit max

    def test_float(self):
        assert_equal(evalNoun(0.0), 0.0)
        assert_equal(evalNoun(1.0), 1.0)
        assert_equal(evalNoun(-1.0), -1.0)
        assert_equal(evalNoun(100.0), 100.0)
        assert_equal(evalNoun(-100.0), -100.0)

    def test_words(self):
        assert_equal(evalNoun([0]), [0])
        assert_equal(evalNoun([1]), [1])
        assert_equal(evalNoun([-1]), [-1])
        assert_equal(evalNoun([256]), [256])
        assert_equal(evalNoun([-256]), [-256])

        assert_equal(evalNoun([0, 1]), [0, 1])
        assert_equal(evalNoun([1, 2]), [1, 2])
        assert_equal(evalNoun([-1, 1]), [-1, 1])
        assert_equal(evalNoun([256, 1024]), [256, 1024])
        assert_equal(evalNoun([-256, -1024]), [-256, -1024])

    def test_floats(self):
        assert_equal(evalNoun([0.0]), [0.0])
        assert_equal(evalNoun([1.0]), [1.0])
        assert_equal(evalNoun([-1.0]), [-1.0])
        assert_equal(evalNoun([256.0]), [256.0])
        assert_equal(evalNoun([-256.0]), [-256.0])

        assert_equal(evalNoun([0.0, 1.0]), [0.0, 1.0])
        assert_equal(evalNoun([1.0, 2.0]), [1.0, 2.0])
        assert_equal(evalNoun([-1.0, 1.0]), [-1.0, 1.0])
        assert_equal(evalNoun([256.0, 1024.0]), [256.0, 1024.0])
        assert_equal(evalNoun([-256.0, -1024.0]), [-256.0, -1024.0])

    def test_mixed(self):
        assert_equal(evalNoun([0, 0.0]), [0, 0.0])
        assert_equal(evalNoun([1.0, 1]), [1.0, 1])
        assert_equal(evalNoun([0, [0]]), [0, [0]])
        assert_equal(evalNoun([1.0, [2.0]]), [1.0, [2.0]])
        assert_equal(evalNoun([[0], [0]]), [[0], [0]])
        assert_equal(evalNoun([[1], [2]]), [[1], [2]])
        assert_equal(evalNoun([[1.0], [2.0]]), [[1.0], [2.0]])

    def test_character(self):
        assert_equal(evalNoun(C('a')), 'a')
        assert_equal(evalNoun(C('b')), 'b')
        assert_equal(evalNoun(C('\x00')), '\x00')

    def test_string(self):
        assert_equal(evalNoun('a'), 'a')
        assert_equal(evalNoun('b'), 'b')
        assert_equal(evalNoun('ab'), 'ab')
        assert_equal(evalNoun('😀'), '😀')

    def test_eval(self):
        assert_equal(eval(0, negate), 0)
        assert_equal(eval(1, negate), -1)
        assert_equal(eval(2, negate), -2)
        assert_equal(eval(-2, negate), 2)

        assert_equal(eval(1, negate, negate), 1)
        assert_equal(eval(1, negate, negate, negate), -1)

# # # Examples from the book "An Introduction to Array Programming in Klong" by Nils
# # class BookTests(TestCase):
# #     pass
# #
# # # Monads
class AtomTests(TestCase):
    # integer atom -> integer, 1)
    # real atom -> integer, 1)
    # list <i size equal 0> atom -> integer, 1)
    # list <i size {equal 0} not> atom -> integer, 0)
    # list atom -> integer, 0)
    # char atom -> integer, 1)

    def test_atom_integer(self):
        assert_equal(eval(1, atom), true)

    def test_atom_real(self):
        assert_equal(eval(1.0, atom),  true)

    def test_atom_list(self):
        assert_equal(eval([], atom),  true)

        assert_equal(eval([2, 3], atom),  false)
        assert_equal(eval([2.0, 3.0], atom),  false)
        assert_equal(eval([2, 3.0], atom),  false)

    def test_atom_integer(self):
        assert_equal(eval(C('a'), atom), true)

    def test_atom_charater(self):
        assert_equal(eval(C('a'), atom), true)

    def test_atom_string(self):
        assert_equal(eval("", atom), true)
        assert_equal(eval("abc", atom), false)

class CharTests(TestCase):
    def test_char_integer(self):
        assert_equal(eval(1, char), '\x01')

    def test_char_real(self):
        with assert_raises(Exception):
            eval(1.0, char)

    def test_char_list(self):
        assert_equal(eval([], char), [])

        assert_equal(eval([2, 3], char), ['\x02', '\x03'])

        with assert_raises(Exception):
            eval([2.0, 3.0], char)

        with assert_raises(Exception):
            eval([2, 3.0], char)

    def test_char_character(self):
        assert_equal(eval(C('a'), char), 'a')

# Monads
class EncloseTests(TestCase):
    def test_enclose_integer(self):
        assert_equal(eval(5, enclose), [5])

    def test_enclose_real(self):
        assert_equal(eval(5.5, enclose), [5.5])

    def test_enclose_list(self):
        assert_equal(eval([0, 1, 2], enclose), [[0, 1, 2]])
        assert_equal(eval([0.0, 1.0, 2.0], enclose), [[0, 1, 2]])
        assert_equal(eval([0.0, 1, 2.0], enclose), [[0.0, 1, 2.0]])

    def test_enclose_character(self):
        assert_equal(eval(C('a'), enclose), "a")

    def test_enclose_string(self):
        assert_equal(eval("a", enclose), ["a"])

class NotTests(TestCase):
    def test_not_integer(self):
        assert_equal(eval(5, inot), -4)

    def test_not_real(self):
        assert_equal(eval(5, inot), -4)

    def test_not_list(self):
        assert_equal(eval([0, 1, 2], inot), [1, 0, -1])
        assert_equal(eval([0.0, 1.0, 2.0], inot), [1, 0, -1])
        assert_equal(eval([0, 1.0, 2], inot), [1, 0.0, -1])

class EnumerateTests(TestCase):
    def test_enumerate_integer(self):
        assert_equal(eval(5, ienumerate), [1, 2, 3, 4, 5])

class FirstTests(TestCase):
    def test_first_integer(self):
        assert_equal(eval(5, first), 5)

    def test_first_real(self):
        assert_equal(eval(5.0, first), 5.0)

    def test_first_list(self):
        assert_equal(eval([], first), [])
        assert_equal(eval([0, 1, 2], first), 0)
        assert_equal(eval([0.0, 1.0, 2.0], first), 0.0)
        assert_equal(eval([0, 1.0, 2], first), 0)

    def test_first_character(self):
        assert_equal(eval(C('a'), first), 'a')

    def test_first_string(self):
        assert_equal(eval("abc", first), 'a')

class FloorTests(TestCase):
    def test_floor_integer(self):
        assert_equal(eval(5, floor), 5)

    def test_floor_real(self):
        assert_equal(eval(5.5, floor), 5)

    def test_floor_list(self):
        assert_equal(eval([], floor), [])
        assert_equal(eval([0, 1, 2], floor), [0, 1, 2])
        assert_equal(eval([0.1, 1.5, 2.9], floor), [0, 1, 2])
        assert_equal(eval([1, 2.0, 3, 4, 5], floor), [1, 2, 3, 4, 5])

# FIXME - format

class GradeDownTests(TestCase):
    def test_gradeDown_word_array(self):
        assert_equal(eval([0, 1, 0, 2], gradeDown), [4, 2, 1, 3])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], gradeDown), [4, 2, 1, 3])
        assert_equal(eval([0, 1.0, 0, 2.0], gradeDown), [4, 2, 1, 3])

    def test_gradeDown_string(self):
        assert_equal(eval("abac", gradeDown), [4, 2, 1, 3])

class GradeUpTests(TestCase):
    def test_gradeUp_list(self):
        assert_equal(eval([0, 1, 0, 2], gradeUp), [1, 3, 2, 4])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], gradeUp), [1, 3, 2, 4])
        assert_equal(eval([0, 1.0, 0, 2.0], gradeUp), [1, 3, 2, 4])

    def test_gradeUp_string(self):
        assert_equal(eval("abac", gradeUp), [4, 2, 1, 3])

class GroupTests(TestCase):
    def test_group_integer(self):
        assert_equal(eval([1, 2, 3, 4], group), [[1], [2], [3], [4]])
        assert_equal(eval([1.0, 2.0, 3.0, 4.0], group), [[1], [2], [3], [4]])
        assert_equal(eval([1.0, 2, 3.0, 4], group), [[1], [2], [3], [4]])
        assert_equal(eval("hello foo", group), [[1], [2], [3, 4], [5, 8, 9], [6], [7]])

class NegateTests(TestCase):
    def test_negate_integer(self):
        assert_equal(eval(1, negate), -1)

    def test_negate_real(self):
        assert_equal(eval(1.0, negate), -1.0)

    def test_negate_list(self):
        assert_equal(eval([2, 3], negate), [-2, -3])
        assert_equal(eval([2.0, 3.0], negate), [-2.0, -3.0])
        assert_equal(eval([2, 3.0], negate), [-2, -3.0])

class ReciprocalTests(TestCase):
    def test_reciprocal_integer(self):
        assert_equal(eval(2, reciprocal), 1.0/2.0)

    def test_reciprocal_real(self):
        assert_equal(eval(2.0, reciprocal), 1.0/2.0)

    def test_reciprocal_list(self):
        assert_equal(eval([], reciprocal), [])
        assert_equal(eval([2, 3], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])
        assert_equal(eval([2.0, 3.0], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])
        assert_equal(eval([2, 3.0], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])

class ReverseTests(TestCase):
    def test_reverse_integer(self):
        assert_equal(eval(2, reverse), 2)

    def test_reverse_real(self):
        assert_equal(eval(2.0, reverse), 2.0)

    def test_reverse_list(self):
        assert_equal(eval([2, 3], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])
        assert_equal(eval([2.0, 3.0], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])
        assert_equal(eval([2, 3.0], reciprocal), [np.float32(1.0)/np.float32(2.0), np.float32(1.0)/np.float32(3.0)])

class ReverseTests(TestCase):
    def test_reverse_integer(self):
        assert_equal(eval(2, reverse), 2)

    def test_reverse_real(self):
        assert_equal(eval(2.0, reverse), 2.0)

    def test_reverse_list(self):
        assert_equal(eval([], reverse), [])
        assert_equal(eval([2, 3], reverse), [3, 2])
        assert_equal(eval([2.0, 3.0], reverse), [3.0, 2.0])
        assert_equal(eval([2, 3.0], reverse), [3.0, 2])

    def test_reverse_character(self):
        assert_equal(eval(C('a'), reverse), 'a')

    def test_reverse_string(self):
        assert_equal(eval("abac", reverse), "caba")

class ShapeTests(TestCase):
    def test_shape_word(self):
        assert_equal(eval(5, shape), 0)

    def test_shape_real(self):
        assert_equal(eval(5.5, shape), 0)

    def test_shape_list(self):
        assert_equal(eval([], shape), [3])
        assert_equal(eval([], reverse), [])
        assert_equal(eval([2, 3], reverse), [3, 2])
        assert_equal(eval([2.0, 3.0], reverse), [3.0, 2.0])
        assert_equal(eval([2, 3.0], reverse), [3.0, 2])

    def test_reverse_character(self):
        assert_equal(eval(C('a'), reverse), 'a')

    def test_reverse_string(self):
        assert_equal(eval("abac", reverse), "caba")

class ShapeTests(TestCase):
    def test_shape_integer(self):
        assert_equal(eval(5, shape), 0)

    def test_shape_real(self):
        assert_equal(eval(5.5, shape), 0)

    def test_shape_list(self):
        assert_equal(eval([], shape), 0)
        assert_equal(eval([0, 1, 2], shape), [3])
        assert_equal(eval([0.1, 1.5, 2.9], shape), [3])
        assert_equal(eval([0, 1.0, 2], shape), [3])
        assert_equal(eval([0, 1, [1, 2, 3]], shape), [3])
        assert_equal(eval([[0], [1], [0]], shape), [3, 1])

class SizeTests(TestCase):
    def test_size_integer(self):
        assert_equal(eval(0, size), 0)
        assert_equal(eval(1, size), 1)
        assert_equal(eval(-1, size), 1)

    def test_size_real(self):
        assert_equal(eval(0.0, size), 0.0)
        assert_equal(eval(1.0, size), 1.0)
        assert_equal(eval(-1.0, size), 1.0)

    def test_size_list(self):
        assert_equal(eval([], size), 0)
        assert_equal(eval([0, 1, 2], size), 3)
        assert_equal(eval([0.1, 1.5, 2.9], size), 3)
        assert_equal(eval([0, 1.0, 2], size), 3)
        assert_equal(eval([0, 1, [1, 2, 3]], size), 3)
        assert_equal(eval([[0], [1], [0]], size), 3)

    def test_size_character(self):
        assert_equal(eval(C('a'), size), 97)

    def test_size_string(self):
        assert_equal(eval('', size), 0)
        assert_equal(eval('a', size), 1)
        assert_equal(eval('abc', size), 3)

class TransposeTests(TestCase):
    def test_transpose_list(self):
        assert_equal(eval([[1, 2], [3, 4]], transpose), [[1, 3], [2, 4]])
        assert_equal(eval([[1.0, 2.0], [3.0, 4.0]], transpose), [[1.0, 3.0], [2.0, 4.0]])
        # assert_equal(eval([[1, 2.0], [3, 4.0]], transpose), [[1, 3], [2.0, 4.0]])

class UniqueTests(TestCase):
    def test_unique_list(self):
        assert_equal(eval([0, 1, 0, 2], unique), [0, 1, 2])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], unique), [0.0, 1.0, 2.0])
        # assert_equal(eval([0, 1.0, 0, 2.0], unique), [0, 1.0, 2.0])

# Dyads
class CutTests(TestCase):
    def test_cut_integer_list(self):
        assert_equal(eval(0, cut, []), [[]])

        assert_equal(eval(0, cut, [1]), [[], [1]])
        assert_equal(eval(1, cut, [1]), [[1], []])
        assert_equal(eval(1, cut, [2, 3]), [[2], [3]])

        assert_equal(eval(0, cut, [1.0]), [[], [1.0]])
        assert_equal(eval(1, cut, [1.0]), [[1.0], []])
        assert_equal(eval(1, cut, [2.0, 3.0]), [[2.0], [3.0]])

        assert_equal(eval(0, cut, [1, 2.0]), [[], [1, 2.0]])
        assert_equal(eval(1, cut, [1, 2.0]), [[1], [2.0]])

        with assert_raises(Exception):
            eval(1, cut, [])
        with assert_raises(Exception):
            eval(-1, cut, [])

        with assert_raises(Exception):
            eval(-1, cut, [1])
        with assert_raises(Exception):
            eval(-1, cut, [2.0])
        with assert_raises(Exception):
            eval(-1, cut, [1, 2.0])

        with assert_raises(Exception):
            eval(5, cut, [1])
        with assert_raises(Exception):
            eval(5, cut, [2.0])
        with assert_raises(Exception):
            eval(5, cut, [1, 2.0])

    def test_cut_list_integer(self):
        assert_equal(eval([], cut, 0), [[]])

        assert_equal(eval([1], cut, 0), [[], [1]])
        assert_equal(eval([1], cut, 1), [[1], []])
        assert_equal(eval([2, 3], cut, 1), [[2], [3]])

        assert_equal(eval([1.0], cut, 0), [[], [1.0]])
        assert_equal(eval([1.0], cut, 1), [[1.0], []])
        assert_equal(eval([2.0, 3.0], cut, 1), [[2.0], [3.0]])

        assert_equal(eval([1, 2.0], cut, 0), [[], [1, 2.0]])
        assert_equal(eval([1, 2.0], cut, 1), [[1], [2.0]])

        with assert_raises(Exception):
            eval([], cut, 1)
        with assert_raises(Exception):
            eval([], cut, -1)

        with assert_raises(Exception):
            eval([1], cut, -1)
        with assert_raises(Exception):
            eval([2.0], cut, -1)
        with assert_raises(Exception):
            eval([1, 2.0], cut, -1)

        with assert_raises(Exception):
            eval([1], cut, 5)
        with assert_raises(Exception):
            eval([2.0], cut, 5)
        with assert_raises(Exception):
            eval([1, 2.0], cut, 5)

    def test_cut_integers(self):
        assert_equal(eval([2, 3], cut, []), [[2, 3]])
        assert_equal(eval([2, 3], cut, [1, 2]), [[2], [3], []])

        assert_equal(eval([2.0, 3.0], cut, []), [[2.0, 3.0]])
        assert_equal(eval([2.0, 3.0], cut, [1, 2]), [[2.0], [3.0], []])

        assert_equal(eval([2, 3.0], cut, [1, 2]), [[2], [3.0], []])
        assert_equal(eval([2, 3.0], cut, []), [[2, 3.0]])

        with assert_raises(Exception):
            eval([], cut, [1, 2])

class DivideTests(TestCase):
    def test_divide_integer_integer(self):
        assert_equal(eval(1, divide, 2), 1.0 / 2.0)
        with assert_raises(Exception):
            eval(1, divide, 0)

    def test_divide_integer_real(self):
        assert_equal(eval(1, divide, 2.0), 0.5)
        with assert_raises(Exception):
            eval(1, divide, 0)

    def test_divide_real_integer(self):
        assert_equal(eval(1.0, divide, -1), -1.0)
        with assert_raises(Exception):
            eval(1.0, divide, 0)
        assert_equal(eval(1.0, divide, 2.0), 0.5)
        with assert_raises(Exception):
            (eval(1.0, divide, 0))

    def test_divide_integer_list(self):
        assert_equal(eval(1, divide, [2, 4]), [1.0 / 2.0, 1.0 / 4.0])
        with assert_raises(Exception):
            eval(1, divide, [0, 3])
        assert_equal(eval(1, divide, [2.0, 4.0]), [1.0 / 2.0, 1.0 / 4.0])
        with assert_raises(Exception):
            eval(1, divide, [0.0, 3.0])
        assert_equal(eval(1, divide, [2, 4.0]), [1.0 / 2.0, 1.0 / 4.0])
        with assert_raises(Exception):
            eval(1, divide, [0, 3.0])

    def test_divide_real_list(self):
        assert_equal(eval(1.0, divide, [2, 4]), [1.0 / 2.0, 1.0 / 4.0])
        assert_equal(eval(1.0, divide, [2.0, 4.0]), [1.0/2.0, 1.0 / 4.0])
        assert_equal(eval(1, divide, [2, 4.0]), [1.0 / 2.0, 1.0 / 4.0])

    def test_divide_list_integer(self):
        assert_equal(eval([2, 4], divide, 1), [2, 4])

    def test_divide_list_real(self):
        assert_equal(eval([2, 4], divide, 1.0), [2, 4])

    def test_divide_list_list(self):
        assert_equal(eval([2, 4], divide, [2, 4]), [1, 1])
        assert_equal(eval([2, 4], divide, [2.0, 4.0]), [1, 1])
        assert_equal(eval([2, 4], divide, [2, 4.0]), [1, 1.0])
        assert_equal(eval([2.0, 4.0], divide, [2, 4]), [1, 1])
        assert_equal(eval([2.0, 4.0], divide, [2.0, 4.0]), [1, 1])
        assert_equal(eval([2.0, 4.0], divide, [2, 4.0]), [1, 1.0])
        assert_equal(eval([2, 4.0], divide, [2, 4]), [1, 1])
        assert_equal(eval([2, 4.0], divide, [2.0, 4.0]), [1, 1])
        assert_equal(eval([2, 4.0], divide, [2, 4.0]), [1, 1.0])

class DropTests(TestCase):
    def test_drop_list(self):
        assert_equal(eval([], drop, 0), [])
        assert_equal(eval([], drop, 1), [])
        assert_equal(eval([], drop, -1), [])
        assert_equal(eval([], drop, 10), [])
        assert_equal(eval([], drop, -10), [])

        assert_equal(eval([0, 1, 0, 2], drop, 0), [0, 1, 0, 2])
        assert_equal(eval([0, 1, 0, 2], drop, 2), [0, 2])
        assert_equal(eval([0, 1, 0, 2], drop, -2), [0, 1])
        assert_equal(eval([0, 1, 0, 2], drop, 100), [])
        assert_equal(eval([0, 1, 0, 2], drop, -100), [])

        assert_equal(eval([0.0, 1.0, 0.0, 2.0], drop, 0), [0.0, 1.0, 0.0, 2.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], drop, 2), [0.0, 2.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], drop, -2), [0.0, 1.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], drop, 100), [])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], drop, -100), [])

        assert_equal(eval([0, 1.0, 0, 2.0], drop, 0), [0, 1.0, 0, 2.0])
        assert_equal(eval([0, 1.0, 0, 2.0], drop, 2), [0, 2.0])
        assert_equal(eval([0, 1.0, 0, 2.0], drop, -2), [0, 1.0])
        assert_equal(eval([0, 1.0, 0, 2.0], drop, 100), [])
        assert_equal(eval([0, 1.0, 0, 2.0], drop, -100), [])

# FIXME equal for characters, strings
class EqualTests(TestCase):
    def test_equal_integer(self):
        assert_equal(eval(1, equal, 1), 1)
        assert_equal(eval(1, equal, 2), 0)
        assert_equal(eval(1, equal, -1), 0)

        with assert_raises(Exception):
            eval(1, equal, 1.0)
        with assert_raises(Exception):
            eval(1, equal, 2.0)
        with assert_raises(Exception):
            eval(1, equal, -1.0)

        with assert_raises(Exception):
            eval(1, equal, [])
        with assert_raises(Exception):
            eval(1, equal, [1])
        with assert_raises(Exception):
            eval(1, equal, [2.0])
        with assert_raises(Exception):
            eval(1, equal, [1, 2.0])

    def test_equal_real(self):
        with assert_raises(Exception):
            eval(1.0, equal, 1)
        with assert_raises(Exception):
            eval(1.0, equal, 2)
        with assert_raises(Exception):
            eval(1.0, equal, -1)

        with assert_raises(Exception):
            eval(1.0, equal, 1.0)
        with assert_raises(Exception):
            eval(1.0, equal, 2.0)
        with assert_raises(Exception):
            eval(1.0, equal, -1.0)

        with assert_raises(Exception):
            eval(1.0, equal, [])
        with assert_raises(Exception):
            eval(1.0, equal, [1])
        with assert_raises(Exception):
            eval(1.0, equal, [2.0])
        with assert_raises(Exception):
            eval(1.0, equal, [1, 2.0])

    def test_equal_list(self):
        assert_equal(eval([], equal, []), [])
        with assert_raises(Exception):
            eval([], equal, [1])
        with assert_raises(Exception):
            eval([], equal, [2.0])
        with assert_raises(Exception):
            eval([], equal, [1, 2.0])

        assert_equal(eval([1], equal, [1]), [1])
        assert_equal(eval([1], equal, [2]), [0])
        with assert_raises(Exception):
            eval([1], equal, [1, 2])
        with assert_raises(Exception):
            eval([1], equal, [1.0])
        with assert_raises(Exception):
            eval([1], equal, [1.0, 2.0])
        with assert_raises(Exception):
            eval([1], equal, [2.0])
        with assert_raises(Exception):
            eval([1], equal, [1, 2.0])

        with assert_raises(Exception):
            eval([1.0], equal, [1])
        with assert_raises(Exception):
            eval([1.0], equal, [1, 2])
        with assert_raises(Exception):
            eval([1.0], equal, [2])
        with assert_raises(Exception):
            eval([1.0], equal, [1.0])
        with assert_raises(Exception):
            eval([1.0], equal, [1.0, 2.0])
        with assert_raises(Exception):
            eval([1.0], equal, [2.0])
        with assert_raises(Exception):
            eval([1.0], equal, [1, 2.0])

        with assert_raises(Exception):
            eval([1, 2.0], equal, [1, 2.0])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [1.0, 2])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [1, 2])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [1.0, 2.0])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [1])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [2.0])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [2.0, 1.0])
        with assert_raises(Exception):
            eval([1, 2.0], equal, [2.0, 1])

# FIXME - expand
# FIXME - form
# FIXME - format2

class FindTests(TestCase):
    def test_find_list_integer(self):
        assert_equal(eval([1, 2, 3], find, 2), [2])
        assert_equal(eval([1.0, 2.0, 3.0], find, 2), [2])
        assert_equal(eval([1, 2.0, 3], find, 2), [2])
        assert_equal(eval([1.0, 2, 3.0], find, 2), [2])
        assert_equal(eval([1, 2, 3], find, 4), [])
        assert_equal(eval([1.0, 2.0, 3.0], find, 4), [])
        assert_equal(eval([1, 2.0, 3], find, 4), [])
        assert_equal(eval([1.0, 2, 3.0], find, 4), [])

    def test_find_list_real(self):
        assert_equal(eval([1, 2, 3], find, 2.0), [2])
        assert_equal(eval([1.0, 2.0, 3.0], find, 2.0), [2])
        assert_equal(eval([1, 2.0, 3], find, 2.0), [2])
        assert_equal(eval([1.0, 2, 3.0], find, 2.0), [2])
        assert_equal(eval([1, 2, 3], find, 4.0), [])
        assert_equal(eval([1.0, 2.0, 3.0], find, 4.0), [])
        assert_equal(eval([1, 2.0, 3], find, 4.0), [])
        assert_equal(eval([1.0, 2, 3.0], find, 4.0), [])

    def test_find_list_list(self):
        assert_equal(eval([1, 2, 3], find, [2, 3]), [2])
        assert_equal(eval([1.0, 2.0, 3.0], find, [2, 3]), [2])
        assert_equal(eval([1, 2.0, 3], find, [2, 3]), [2])
        assert_equal(eval([1.0, 2, 3.0], find, [2, 3]), [2])
        assert_equal(eval([1, 2, 3], find, [2, 4]), [])
        assert_equal(eval([1.0, 2.0, 3.0], find, [2, 4]), [])
        assert_equal(eval([1, 2.0, 3], find, [2, 4]), [])
        assert_equal(eval([1.0, 2, 3.0], find, [2, 4]), [])

    def test_find_string_character(self):
        assert_equal(eval("abc", find, C('b')), [2])
        assert_equal(eval("abc", find, C('d')), [])

    def test_find_string_string(self):
        assert_equal(eval("abc", find, "bc"), [2])
        assert_equal(eval("abc", find, "bd"), [])

class IndexTests(TestCase):
    def test_index_list_integer(self):
        assert_equal(eval([2, 3], index, 1), 2)
        assert_equal(eval([2.0, 3.0], index, 1), 2.0)
        assert_equal(eval([2, 3.0], index, 1), 2)

        with assert_raises(Exception):
            eval([2, 3], index, 0)
        with assert_raises(Exception):
            eval([2, 3], index, -1)

    def test_index_list_list(self):
        assert_equal(eval([2, 3], index, [1, 2]), [2, 3])
        assert_equal(eval([2.0, 3.0], index, [1, 2]), [2.0, 3.0])
        assert_equal(eval([2, 3.0], index, [1, 2]), [2, 3.0])

    def test_index_string_integer(self):
        assert_equal(eval("abc", index, 2), "b")

    def test_index_string_list(self):
        assert_equal(eval("abc", index, [2, 3]), "bc")

class IntegerDivide(TestCase):
    def test_integer_integer(self):
        assert_equal(eval(1, integerDivide, 1), 1)
        assert_equal(eval(2, integerDivide, 1), 2)
        assert_equal(eval(1, integerDivide, 2), 0)
        with assert_raises(Exception):
            eval(1, integerDivide, 0)

class JoinTests(TestCase):
    def test_join_scalar_scalar(self):
        assert_equal(eval(1, join, 2), [1, 2])
        assert_equal(eval(1, join, 2.0), [1, 2.0])
        assert_equal(eval(1, join, C('a')), [1, 'a'])
        assert_equal(eval(1, join, "a"), [1, "a"])

        assert_equal(eval(1.0, join, 2), [1.0, 2])
        assert_equal(eval(1.0, join, 2.0), [1.0, 2.0])
        assert_equal(eval(1.0, join, C('a')), [1.0, 'a'])
        assert_equal(eval(1.0, join, "a"), [1.0, "a"])

        assert_equal(eval(C('a'), join, 2), ['a', 2])
        assert_equal(eval(C('a'), join, 2.0), ['a', 2.0])
        assert_equal(eval(C('a'), join, C('b')), "ab")

    def test_join_integer_list(self):
        assert_equal(eval(1, join, []), [1])
        assert_equal(eval(1, join, [2, 3]), [1, 2, 3])
        assert_equal(eval(1, join, [2.0, 3.0]), [1, 2.0, 3.0])
        assert_equal(eval(1, join, [2.0, 3]), [1, 2.0, 3])

    def test_join_real_list(self):
        assert_equal(eval(1.0, join, []), [1.0])
        assert_equal(eval(1.0, join, [2, 3]), [1.0, 2, 3])
        assert_equal(eval(1.0, join, [2.0, 3.0]), [1.0, 2.0, 3.0])
        assert_equal(eval(1.0, join, [2.0, 3]), [1.0, 2.0, 3])

    def test_join_character_list(self):
        assert_equal(eval(C('a'), join, []), ['a'])
        assert_equal(eval(C('a'), join, [C('b')]), ['a', 'b'])
        assert_equal(eval(C('a'), join, ["bc"]), ['a', "bc"])

    def test_join_character_string(self):
        assert_equal(eval(C('a'), join, ""), "a")
        assert_equal(eval(C('a'), join, "b"), "ab")

    def test_join_string_character(self):
        assert_equal(eval("", join, C('a')), "a")
        assert_equal(eval("a", join, C('b')), "ab")

    def test_join_string_string(self):
        assert_equal(eval("", join, ""), "")
        assert_equal(eval("", join, "b"), "b")
        assert_equal(eval("a", join, ""), "a")
        assert_equal(eval("a", join, "b"), "ab")
        assert_equal(eval("ab", join, "cd"), "abcd")

class LessTests(TestCase):
    def test_less_integer_integer(self):
        assert_equal(eval(1, less, 2), 1)
        assert_equal(eval(2, less, 1), 0)

    def test_less_integer_real(self):
        assert_equal(eval(1, less, 2.0), 1)
        assert_equal(eval(2, less, 1.0), 0)

    def test_less_real_integer(self):
        assert_equal(eval(1.0, less, 2), 1)
        assert_equal(eval(2.0, less, 1), 0)

    def test_less_integer_list(self):
        assert_equal(eval(2, less, [1, 3]), [0, 1])
        assert_equal(eval(2, less, [1.0, 3.0]), [0, 1])
        assert_equal(eval(2, less, [1, 3.0]), [0, 1])

    def test_less_real_list(self):
        assert_equal(eval(2.0, less, [1, 3]), [0, 1])
        assert_equal(eval(2.0, less, [1.0, 3.0]), [0, 1])
        assert_equal(eval(2.0, less, [1, 3.0]), [0, 1])

    def test_less_list_integer(self):
        assert_equal(eval([1, 3], less, 2), [1, 0])
        assert_equal(eval([1.0, 3.0], less, 2), [1, 0])
        assert_equal(eval([1, 3.0], less, 2), [1, 0])

    def test_less_list_real(self):
        assert_equal(eval([1, 3], less, 2.0), [1, 0])
        assert_equal(eval([1.0, 3.0], less, 2.0), [1, 0])
        assert_equal(eval([1, 3.0], less, 2.0), [1, 0])

    def test_less_list_list(self):
        assert_equal(eval([2, 2], less, [1, 3]), [0, 1])
        assert_equal(eval([2, 2], less, [1.0, 3.0]), [0, 1])
        assert_equal(eval([2, 2], less, [1, 3.0]), [0, 1])

        assert_equal(eval([2.0, 2.0], less, [1, 3]), [0, 1])
        assert_equal(eval([2.0, 2.0], less, [1.0, 3.0]), [0, 1])
        assert_equal(eval([2.0, 2.0], less, [1, 3.0]), [0, 1])

        assert_equal(eval([2, 2.0], less, [1, 3]), [0, 1])
        assert_equal(eval([2, 2.0], less, [1.0, 3.0]), [0, 1])
        assert_equal(eval([2, 2.0], less, [1, 3.0]), [0, 1])

class MatchTests(TestCase):
    def test_match_integer_integer(self):
        assert_equal(eval(1, match, 1), 1)
        assert_equal(eval(1, match, 2), 0)

    def test_match_integer_real(self):
        assert_equal(eval(1, match, 1.0), 1)
        assert_equal(eval(1, match, 2.0), 0)

    def test_match_real_integer(self):
        assert_equal(eval(1.0, match, 1), 1)
        assert_equal(eval(1.0, match, 2), 0)

    def test_match_real_real(self):
        assert_equal(eval(1.0, match, 1.0), 1)
        assert_equal(eval(1.0, match, 2.0), 0)

    def test_match_integer_list(self):
        assert_equal(eval(1, match, []), 0)
        assert_equal(eval(1, match, [1]), 0)
        assert_equal(eval(1, match, [2]), 0)

    def test_match_real_list(self):
        assert_equal(eval(1.0, match, []), 0)
        assert_equal(eval(1.0, match, [1]), 0)
        assert_equal(eval(1.0, match, [2]), 0)

    def test_match_list_integer(self):
        assert_equal(eval([], match, 1), 0)
        assert_equal(eval([1], match, 1), 0)
        assert_equal(eval([2], match, 1), 0)

    def test_match_list_real(self):
        assert_equal(eval([], match, 1.0), 0)
        assert_equal(eval([1], match, 1.0), 0)
        assert_equal(eval([2], match, 1.0), 0)

    def test_match_list_list(self):
        assert_equal(eval([], match, []), 1)
        assert_equal(eval([1], match, [1]), 1)
        assert_equal(eval([1], match, [2]), 0)
        assert_equal(eval([1, 2], match, [1]), 0)
        assert_equal(eval([1], match, [1, 2]), 0)

        assert_equal(eval([1], match, [1.0]), 1)
        assert_equal(eval([1], match, [2.0]), 0)
        assert_equal(eval([1, 2], match, [1.0]), 0)
        assert_equal(eval([1], match, [1.0, 2.0]), 0)
        assert_equal(eval([1], match, [1, 2.0]), 0)

        assert_equal(eval([1.0], match, [1]), 1)
        assert_equal(eval([1.0], match, [2]), 0)
        assert_equal(eval([1.0, 2.0], match, [1]), 0)
        assert_equal(eval([1.0], match, [1, 2]), 0)

        assert_equal(eval([1.0], match, [1.0]), 1)
        assert_equal(eval([1.0], match, [2.0]), 0)
        assert_equal(eval([1.0, 2.0], match, [1.0]), 0)
        assert_equal(eval([1.0], match, [1.0, 2.0]), 0)
        assert_equal(eval([1.0], match, [1, 2.0]), 0)

        assert_equal(eval([1, 2.0], match, [1]), 0)
        assert_equal(eval([1, 2.0], match, [1.0]), 0)
        assert_equal(eval([1, 2.0], match, [1.0]), 0)
        assert_equal(eval([1, 2.0], match, [1, 2]), 1)
        assert_equal(eval([1, 2.0], match, [1.0, 2.0]), 1)
        assert_equal(eval([1, 2.0], match, [1, 2.0]), 1)
        assert_equal(eval([1, 2.0], match, [1.0, 2]), 1)

    def test_match_character(self):
        assert_equal(eval(C('a'), match, C('a')), 1)
        assert_equal(eval(C('a'), match, C('b')), 0)

        assert_equal(eval(C('a'), match, 0), 0)
        assert_equal(eval(C('a'), match, 0.0), 0)
        assert_equal(eval(C('a'), match, []), 0)
        assert_equal(eval(C('a'), match, [1]), 0)
        assert_equal(eval(C('a'), match, [1.0]), 0)
        assert_equal(eval(C('a'), match, [1, 2]), 0)
        assert_equal(eval(C('a'), match, [1.0, 2.0]), 0)
        assert_equal(eval(C('a'), match, [1, 2.0]), 0)
        assert_equal(eval(C('a'), match, ""), 0)
        assert_equal(eval(C('a'), match, "a"), 0)
        assert_equal(eval(C('a'), match, "ab"), 0)

    def test_match_string(self):
        assert_equal(eval("", match, ""), 1)
        assert_equal(eval("", match, "a"), 0)
        assert_equal(eval("", match, C('a')), 0)
        assert_equal(eval("", match, 0), 0)
        assert_equal(eval("", match, 0.0), 0)
        assert_equal(eval("", match, []), 0)
        assert_equal(eval("", match, [1]), 0)
        assert_equal(eval("", match, [1.0]), 0)
        assert_equal(eval("", match, [1, 2]), 0)
        assert_equal(eval("", match, [1.0, 2.0]), 0)
        assert_equal(eval("", match, [1, 2.0]), 0)

        assert_equal(eval("a", match, "a"), 1)
        assert_equal(eval("a", match, ""), 0)
        assert_equal(eval("a", match, C('a')), 0)
        assert_equal(eval("a", match, 0), 0)
        assert_equal(eval("a", match, 0.0), 0)
        assert_equal(eval("a", match, []), 0)
        assert_equal(eval("a", match, [1]), 0)
        assert_equal(eval("a", match, [1.0]), 0)
        assert_equal(eval("a", match, [1, 2]), 0)
        assert_equal(eval("a", match, [1.0, 2.0]), 0)
        assert_equal(eval("a", match, [1, 2.0]), 0)

        assert_equal(eval("ab", match, "ab"), 1)
        assert_equal(eval("ab", match, ""), 0)
        assert_equal(eval("ab", match, "a"), 0)
        assert_equal(eval("ab", match, C('a')), 0)
        assert_equal(eval("ab", match, 0), 0)
        assert_equal(eval("ab", match, 0.0), 0)
        assert_equal(eval("ab", match, []), 0)
        assert_equal(eval("ab", match, [1]), 0)
        assert_equal(eval("ab", match, [1.0]), 0)
        assert_equal(eval("ab", match, [1, 2]), 0)
        assert_equal(eval("ab", match, [1.0, 2.0]), 0)
        assert_equal(eval("ab", match, [1, 2.0]), 0)

class MaxTests(TestCase):
    def test_max_integer_integer(self):
        assert_equal(eval(1, imax, 2), 2)
        assert_equal(eval(2, imax, 1), 2)

    def test_max_integer_real(self):
        assert_equal(eval(1, imax, 2.0), 2.0)
        assert_equal(eval(2, imax, 1.0), 2)

    def test_max_real_integer(self):
        assert_equal(eval(1.0, imax, 2), 2)
        assert_equal(eval(2.0, imax, 1), 2.0)

    def test_max_integer_list(self):
        assert_equal(eval(2, imax, [1, 3]), [2, 3])
        assert_equal(eval(2, imax, [1.0, 3.0]), [2, 3.0])
        assert_equal(eval(2, imax, [1, 3.0]), [2, 3.0])

    def test_max_real_list(self):
        assert_equal(eval(2.0, imax, [1, 3]), [2.0, 3])
        assert_equal(eval(2.0, imax, [1.0, 3.0]), [2.0, 3.0])
        assert_equal(eval(2.0, imax, [1, 3.0]), [2.0, 3.0])

    def test_max_list_integer(self):
        assert_equal(eval([1, 3], imax, 2), [2, 3])
        assert_equal(eval([1.0, 3.0], imax, 2), [2, 3.0])
        assert_equal(eval([1, 3.0], imax, 2), [2, 3.0])

    def test_max_list_real(self):
        assert_equal(eval([1, 3], imax, 2.0), [2.0, 3])
        assert_equal(eval([1.0, 3.0], imax, 2.0), [2.0, 3.0])
        assert_equal(eval([1, 3.0], imax, 2.0), [2.0, 3.0])

    def test_max_list_list(self):
        assert_equal(eval([2, 2], imax, [1, 3]), [2, 3])
        assert_equal(eval([2, 2], imax, [1.0, 3.0]), [2, 3.0])
        assert_equal(eval([2, 2], imax, [1, 3.0]), [2, 3.0])

        assert_equal(eval([2.0, 2.0], imax, [1, 3]), [2.0, 3])
        assert_equal(eval([2.0, 2.0], imax, [1.0, 3.0]), [2.0, 3.0])
        assert_equal(eval([2.0, 2.0], imax, [1, 3.0]), [2.0, 3.0])

        assert_equal(eval([2, 2.0], imax, [1, 3]), [2, 3])
        assert_equal(eval([2, 2.0], imax, [1.0, 3.0]), [2, 3.0])
        assert_equal(eval([2, 2.0], imax, [1, 3.0]), [2, 3.0])

class MinTests(TestCase):
    def test_min_integer_integer(self):
        assert_equal(eval(1, imin, 2), 1)
        assert_equal(eval(2, imin, 1), 1)

    def test_min_integer_real(self):
        assert_equal(eval(1, imin, 2.0), 1)
        assert_equal(eval(2, imin, 1.0), 1.0)

    def test_min_real_integer(self):
        assert_equal(eval(1.0, imin, 2), 1.0)
        assert_equal(eval(2.0, imin, 1), 1)

    def test_min_integer_list(self):
        assert_equal(eval(2, imin, [1, 3]), [1, 2])
        assert_equal(eval(2, imin, [1.0, 3.0]), [1.0, 2])
        assert_equal(eval(2, imin, [1, 3.0]), [1, 2])

    def test_min_real_list(self):
        assert_equal(eval(2.0, imin, [1, 3]), [1, 2.0])
        assert_equal(eval(2.0, imin, [1.0, 3.0]), [1.0, 2.0])
        assert_equal(eval(2.0, imin, [1, 3.0]), [1, 2.0])

    def test_min_list_integer(self):
        assert_equal(eval([1, 3], imin, 2), [1, 2])
        assert_equal(eval([1.0, 3.0], imin, 2), [1.0, 2])
        assert_equal(eval([1, 3.0], imin, 2), [1, 2])

    def test_min_list_real(self):
        assert_equal(eval([1, 3], imin, 2.0), [1, 2.0])
        assert_equal(eval([1.0, 3.0], imin, 2.0), [1.0, 2.0])
        assert_equal(eval([1, 3.0], imin, 2.0), [1, 2.0])

    def test_min_list_list(self):
        assert_equal(eval([2, 2], imin, [1, 3]), [1, 2])
        assert_equal(eval([2, 2], imin, [1.0, 3.0]), [1.0, 2])
        assert_equal(eval([2, 2], imin, [1, 3.0]), [1, 2])

        assert_equal(eval([2.0, 2.0], imin, [1, 3]), [1, 2.0])
        assert_equal(eval([2.0, 2.0], imin, [1.0, 3.0]), [1.0, 2.0])
        assert_equal(eval([2.0, 2.0], imin, [1, 3.0]), [1, 2.0])

        assert_equal(eval([2, 2.0], imin, [1, 3]), [1, 2.0])
        assert_equal(eval([2, 2.0], imin, [1.0, 3.0]), [1.0, 2.0])
        assert_equal(eval([2, 2.0], imin, [1, 3.0]), [1, 2.0])

class MinusTests(TestCase):
    def test_minus_integer_integer(self):
        assert_equal(eval(1, minus, 2), -1)
        assert_equal(eval(-1, minus, -1), 0)
        assert_equal(eval(0, minus, 0), 0)

    def test_minus_integer_real(self):
        assert_equal(eval(1, minus, 2.0), -1.0)
        assert_equal(eval(-1, minus, 1.0), -2.0)
        assert_equal(eval(0, minus, 0.0), 0.0)

    def test_minus_integer_list(self):
        assert_equal(eval(1, minus, [2, 3]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1]), [0, -1])

        assert_equal(eval(1, minus, [2, 3]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1]), [0, -1])

        assert_equal(eval(1, minus, [2, 3.0]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1.0]), [0, -1])

    def test_minus_real_integer(self):
        assert_equal(eval(1, minus, -1), 2.0)
        assert_equal(eval(-1, minus, 0), -1.0)
        assert_equal(eval(0, minus, 0), 0.0)

    def test_minus_real_real(self):
        assert_equal(eval(1.0, minus, 2.0), -1.0)
        assert_equal(eval(-1.0, minus, 1.0), -2.0)
        assert_equal(eval(0.0, minus, 0.0), 0.0)

    def test_minus_real_list(self):
        assert_equal(eval(1, minus, [2, 3]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1]), [0, -1])

        assert_equal(eval(1, minus, [2, 3]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1]), [0, -1])

        assert_equal(eval(1, minus, [2, 3.0]), [-1, -2])
        assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
        assert_equal(eval(0, minus, [0, 1.0]), [0, -1])

    def test_minus_list_integer(self):
        assert_equal(eval([2, 3], minus, 1), [1, 2])
        assert_equal(eval([-1, 0], minus, -1), [0, 1])
        assert_equal(eval([0, 1], minus, 0), [0, 1])

        assert_equal(eval([2, 3.0], minus, 2), [0, 1.0])
        assert_equal(eval([-1, 0], minus, 2), [-3, -2])
        assert_equal(eval([0, 1.0], minus, 2), [-2, -1])

    def test_minus_list_real(self):
        assert_equal(eval([2, 3], minus, 1.0), [1.0, 2.0])
        assert_equal(eval([-1, 0], minus, 1.0), [-2.0, -1.0])
        assert_equal(eval([0, 1], minus, 0.0), [0.0, 1.0])

        assert_equal(eval([2, 3.0], minus, 2.0), [0, 1.0])
        assert_equal(eval([-1, 0], minus, 2.0), [-3, -2])
        assert_equal(eval([0, 1.0], minus, 2.0), [-2, -1])

    def test_minus_list_list(self):
        assert_equal(eval([2, 3], minus, [2, 3]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
        assert_equal(eval([0, 1], minus, [2, 3]), [-2, -2])

        assert_equal(eval([2, 3], minus, [2, 3]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
        assert_equal(eval([0, 1], minus, [2, 3]), [-2, -2])

        assert_equal(eval([2, 3], minus, [2, 3.0]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3.0]), [-3, -3])
        assert_equal(eval([0, 1], minus, [2, 3.0]), [-2, -2])

        assert_equal(eval([2, 3.0], minus, [2, 3]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
        assert_equal(eval([0, 1.0], minus, [2, 3]), [-2, -2])

        assert_equal(eval([2, 3.0], minus, [2, 3]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
        assert_equal(eval([0, 1.0], minus, [2, 3]), [-2, -2])

        assert_equal(eval([2, 3.0], minus, [2, 3.0]), [0, 0])
        assert_equal(eval([-1, 0], minus, [2, 3.0]), [-3, -3])
        assert_equal(eval([0, 1.0], minus, [2, 3.0]), [-2, -2])

class MoreTests(TestCase):
    def test_more_integer_integer(self):
        assert_equal(eval(1, more, 2), 0)
        assert_equal(eval(2, more, 1), 1)

    def test_more_integer_real(self):
        assert_equal(eval(1, more, 2.0), 0)
        assert_equal(eval(2, more, 1.0), 1)

    def test_more_real_integer(self):
        assert_equal(eval(1.0, more, 2), 0)
        assert_equal(eval(2.0, more, 1), 1)

    def test_more_integer_list(self):
        assert_equal(eval(2, more, [1, 3]), [1, 0])
        assert_equal(eval(2, more, [1.0, 3.0]), [1, 0])
        assert_equal(eval(2, more, [1, 3.0]), [1, 0])

    def test_more_real_list(self):
        assert_equal(eval(2.0, more, [1, 3]), [1, 0])
        assert_equal(eval(2.0, more, [1.0, 3.0]), [1, 0])
        assert_equal(eval(2.0, more, [1, 3.0]), [1, 0])

    def test_more_list_integer(self):
        assert_equal(eval([1, 3], more, 2), [0, 1])
        assert_equal(eval([1.0, 3.0], more, 2), [0, 1])
        assert_equal(eval([1, 3.0], more, 2), [0, 1])

    def test_more_list_real(self):
        assert_equal(eval([1, 3], more, 2.0), [0, 1])
        assert_equal(eval([1.0, 3.0], more, 2.0), [0, 1])
        assert_equal(eval([1, 3.0], more, 2.0), [0, 1])

    def test_more_list_list(self):
        assert_equal(eval([2, 2], more, [1, 3]), [1, 0])
        assert_equal(eval([2, 2], more, [1.0, 3.0]), [1, 0])
        assert_equal(eval([2, 2], more, [1, 3.0]), [1, 0])

        assert_equal(eval([2.0, 2.0], more, [1, 3]), [1, 0])
        assert_equal(eval([2.0, 2.0], more, [1.0, 3.0]), [1, 0])
        assert_equal(eval([2.0, 2.0], more, [1, 3.0]), [1, 0])

        assert_equal(eval([2, 2.0], more, [1, 3]), [1, 0])
        assert_equal(eval([2, 2.0], more, [1.0, 3.0]), [1, 0])
        assert_equal(eval([2, 2.0], more, [1, 3.0]), [1, 0])

class PlusTests(TestCase):
    def test_plus_integer_integer(self):
        assert_equal(eval(1, plus, 2), 3)
        assert_equal(eval(-1, plus, -1), -2)
        assert_equal(eval(0, plus, 0), 0)

    def test_plus_integer_real(self):
        assert_equal(eval(1, plus, 2.0), 3.0)
        assert_equal(eval(-1, plus, 1.0), 0.0)
        assert_equal(eval(0, plus, 0.0), 0.0)

    def test_plus_integer_list(self):
        assert_equal(eval(1, plus, [2, 3]), [3, 4])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1]), [0, 1])

        assert_equal(eval(1, plus, [2, 3]), [3, 4])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1]), [0, 1])

        assert_equal(eval(1, plus, [2, 3.0]), [3, 4.0])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1.0]), [0, 1.0])

    def test_plus_real_integer(self):
        assert_equal(eval(1, plus, -1), 0)
        assert_equal(eval(-1, plus, 0), -1)
        assert_equal(eval(0, plus, 0), 0.0)

    def test_plus_real_real(self):
        assert_equal(eval(1.0, plus, 2.0), 3.0)
        assert_equal(eval(-1.0, plus, 1.0), 0.0)
        assert_equal(eval(0.0, plus, 0.0), 0.0)

    def test_plus_real_list(self):
        assert_equal(eval(1, plus, [2, 3]), [3, 4])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1]), [0, 1])

        assert_equal(eval(1, plus, [2, 3]), [3, 4])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1]), [0, 1])

        assert_equal(eval(1, plus, [2, 3.0]), [3, 4.0])
        assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
        assert_equal(eval(0, plus, [0, 1.0]), [0, 1.0])

    def test_plus_list_integer(self):
        assert_equal(eval([2, 3], plus, 1), [3, 4])
        assert_equal(eval([-1, 0], plus, -1), [-2, -1])
        assert_equal(eval([0, 1], plus, 0), [0, 1])

        assert_equal(eval([2, 3.0], plus, 2), [4, 5.0])
        assert_equal(eval([-1, 0], plus, 2), [1, 2])
        assert_equal(eval([0, 1.0], plus, 2), [2, 3.0])

    def test_plus_list_real(self):
        assert_equal(eval([2, 3], plus, 1.0), [3.0, 4.0])
        assert_equal(eval([-1, 0], plus, 1.0), [0.0, 1.0])
        assert_equal(eval([0, 1], plus, 0.0), [0.0, 1.0])

        assert_equal(eval([2, 3.0], plus, 2.0), [4.0, 5.0])
        assert_equal(eval([-1, 0], plus, 2.0), [1.0, 2.0])
        assert_equal(eval([0, 1.0], plus, 2.0), [2.0, 3.0])

    def test_plus_list_list(self):
        assert_equal(eval([2, 3], plus, [2, 3]), [4, 6])
        assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
        assert_equal(eval([0, 1], plus, [2, 3]), [2, 4])

        assert_equal(eval([2, 3], plus, [2, 3]), [4, 6])
        assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
        assert_equal(eval([0, 1], plus, [2, 3]), [2, 4])

        assert_equal(eval([2, 3], plus, [2, 3.0]), [4, 6.0])
        assert_equal(eval([-1, 0], plus, [2, 3.0]), [1, 3.0])
        assert_equal(eval([0, 1], plus, [2, 3.0]), [2, 4.0])

        assert_equal(eval([2, 3.0], plus, [2, 3]), [4, 6.0])
        assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
        assert_equal(eval([0, 1.0], plus, [2, 3]), [2, 4.0])

        assert_equal(eval([2, 3.0], plus, [2, 3]), [4, 6.0])
        assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
        assert_equal(eval([0, 1.0], plus, [2, 3]), [2, 4.0])

        assert_equal(eval([2, 3.0], plus, [2, 3.0]), [4, 6.0])
        assert_equal(eval([-1, 0], plus, [2, 3.0]), [1, 3.0])
        assert_equal(eval([0, 1.0], plus, [2, 3.0]), [2, 4.0])

class PowerTests(TestCase):
    def test_power_integer_integer(self):
        assert_equal(eval(2, power, 2), 4.0)

    def test_power_integer_real(self):
        assert_equal(eval(2, power, 2.0), 4.0)

    def test_power_integer_list(self):
        assert_equal(eval(2, power, [2, 3]), [4, 8])
        assert_equal(eval(2, power, [2, 3]), [4, 8])
        assert_equal(eval(2, power, [2, 3.0]), [4.0, 8.0])

    def test_power_real_integer(self):
        assert_equal(eval(2, power, 2), 4.0)

    def test_power_real_real(self):
        assert_equal(eval(2, power, 2.0), 4.0)

    def test_power_real_list(self):
        assert_equal(eval(2, power, [2, 3]), [4, 8])
        assert_equal(eval(2, power, [2, 3]), [4, 8])
        assert_equal(eval(2, power, [2, 3.0]), [4, 8])

    def test_power_list_integer(self):
        assert_equal(eval([2, 3], power, 3), [8, 27])
        assert_equal(eval([2, 3], power, 3), [8, 27])
        assert_equal(eval([2, 3.0], power, 2), [4.0, 9.0])

    def test_power_list_real(self):
        assert_equal(eval([2, 3], power, 1.0), [2, 3])
        assert_equal(eval([2, 3], power, 1.0), [2, 3])
        assert_equal(eval([2, 3.0], power, 2.0), [4, 9])

    def test_power_list_list(self):
        assert_equal(eval([2, 3], power, [2, 3]), [4.0, 27.0])
        assert_equal(eval([2, 3], power, [2.0, 3.0]), [4.0, 27.0])
        assert_equal(eval([2, 3], power, [2, 3.0]), [4.0, 27.0])
        assert_equal(eval([2.0, 3.0], power, [2, 3]), [4.0, 27.0])
        assert_equal(eval([2.0, 3.0], power, [2, 3]), [4.0, 27.0])
        assert_equal(eval([2.0, 3.0], power, [2, 3.0]), [4.0, 27.0])
        assert_equal(eval([2, 3.0], power, [2, 3]), [4.0, 27.0])
        assert_equal(eval([2, 3.0], power, [2, 3]), [4.0, 27.0])
        assert_equal(eval([2, 3.0], power, [2, 3.0]), [4.0, 27.0])

class RemainderTests(TestCase):
    def test_remainder_integer_integer(self):
        assert_equal(eval(7, remainder, 5), 2)
        assert_equal(eval(7, remainder, -5), 2)
        assert_equal(eval(-7, remainder, 5), -2)
        assert_equal(eval(-7, remainder, -5), -2)

# class ReshapeTests(TestCase):
#     def test_reshape_integer(self):
        # assert_equal(eval([1, 2, 3, 4, 5, 6, 7, 8, 9], reshape, [3, 3]), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        # assert_equal(eval([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], reshape, [-1, 2]), [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        # assert_equal(eval([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], reshape, [2, -1]), [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]])
        # assert_equal(eval(1, reshape, 5), [1, 1, 1, 1, 1])
        #
        # assert_equal(eval(0, reshape, 5), [0, 0, 0, 0, 0])
        # assert_equal(eval(0, reshape, 2), [0, 0])
        # assert_equal(eval(0, reshape, [2]), [0, 0])
        # assert_equal(eval(0, reshape, [2, 2]), [[0, 0], [0, 0]])
        # assert_equal(eval([1], reshape, [3]), [1, 1, 1])
        # assert_equal(eval([1, 2], reshape, [2, 2]), [[1, 2], [1, 2]])
        # assert_equal(eval([1, 2, 3], reshape, [2, 2, 2]), [[[1, 2], [3, 1]], [[2, 3], [1, 2]]])
        # assert_equal(eval([[1, 2, 3]], reshape, [2]), [[1, 2, 3], [1, 2, 3]])

class RotateTests(TestCase):
    def test_rotate_list(self):
        assert_equal(eval([], rotate, 1), [])

        assert_equal(eval([0, 1, 2], rotate, 0), [0, 1, 2])

        assert_equal(eval([0, 1, 2], rotate, 1), [2, 0, 1])
        assert_equal(eval([0, 1, 2], rotate, 4), [2, 0, 1])
        assert_equal(eval([0, 1, 2], rotate, -1), [1, 2, 0])
        assert_equal(eval([0, 1, 2], rotate, -4), [1, 2, 0])

        assert_equal(eval([0.0, 1.0, 2.0], rotate, 0), [0.0, 1.0, 2.0])

        assert_equal(eval([0.0, 1.0, 2.0], rotate, 1), [2.0, 0.0, 1.0])
        assert_equal(eval([0.0, 1.0, 2.0], rotate, 4), [2.0, 0.0, 1.0])
        assert_equal(eval([0.0, 1.0, 2.0], rotate, -1), [1.0, 2.0, 0.0])
        assert_equal(eval([0.0, 1.0, 2.0], rotate, -4), [1.0, 2.0, 0.0])

        assert_equal(eval([0, 1.0, 2], rotate, 0), [0, 1.0, 2])

        assert_equal(eval([0, 1.0, 2], rotate, 1), [2, 0, 1.0])
        assert_equal(eval([0, 1.0, 2], rotate, 4), [2, 0, 1.0])
        assert_equal(eval([0, 1.0, 2], rotate, -1), [1.0, 2, 0])
        assert_equal(eval([0, 1.0, 2], rotate, -4), [1.0, 2, 0])

        assert_equal(eval([0, 1, [1, 2, 3]], rotate, 0), [0, 1, [1, 2, 3]])

        assert_equal(eval([0, 1, [1, 2, 3]], rotate, 1), [[1, 2, 3], 0, 1])
        assert_equal(eval([0, 1, [1, 2, 3]], rotate, 4), [[1, 2, 3], 0, 1])
        assert_equal(eval([0, 1, [1, 2, 3]], rotate, -1), [1.0, [1, 2, 3], 0])
        assert_equal(eval([0, 1, [1, 2, 3]], rotate, -4), [1.0, [1, 2, 3], 0])

    def test_rotate_ref(self):
        #Examples:           1:+[1 2 3 4 5]     -->  [5 1 2 3 4]
        #                    (-1):+[1 2 3 4 5]  -->  [2 3 4 5 1]
        #               1:+[[1 2] [4 5] [5 6]]  -->  [[1 2] [4 5] [5 6]] # errata - should be [[5 6] [1 2] [4 5]], tested with klong
        #           {1:+x}'[[1 2] [4 5] [5 6]]  -->  [[2 1] [5 4] [6 5]]

        assert_equal(eval([1, 2, 3, 4, 5], rotate, 1), [5, 1, 2, 3, 4])
        assert_equal(eval([1, 2, 3, 4, 5], rotate, -1), [2, 3, 4, 5, 1])
        assert_equal(eval([[1, 2], [4, 5], [5, 6]], rotate, 1), [[5, 6], [1, 2], [4, 5]])
        # FIXME - implement test for rotate in an expression with each

    def test_rotate_errors(self):
        with assert_raises(Exception):
            (eval(test_error(), rotate, [1, 2, 3]))

        with assert_raises(Exception):
            (eval(test_error(), rotate, [1, 2, 3]))

        with assert_raises(Exception):
            (eval(test_error(), rotate, [1, 2.0, 3]))

        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, 1.0))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, 1.0))
        with assert_raises(Exception):
            (eval([1, 2, [3, 4, 5]], rotate, 1.0))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, test_error()))

        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, [3, 4, 5]], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, test_error()))

        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, [3, 4, 5]], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, test_error()))

        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, test_error()))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, [3, 4, 5]], rotate, [1]))
        with assert_raises(Exception):
            (eval([1, 2, 3], rotate, [1]))

class SplitTests(TestCase):
    def test_split_ref(self):
        # Examples:         2:#[1 2 3 4]  -->  [[1 2] [3 4]]
        #                   3:#[1 2 3 4]  -->  [[1 2 3] [4]]
        #                   3:#"abcdefg"  -->  ["abc" "def" "g"]
        #           [1 2]:#[1 2 3 4 5 6]  -->  [[1] [2 3] [4] [5 6]]

        assert_equal(eval([1, 2, 3, 4], split, 2), [[1, 2], [3, 4]])
        assert_equal(eval([1, 2, 3, 4], split, 3), [[1, 2, 3], [4]])
        assert_equal(eval("abcdefg", split, 3), ["abc", "def", "g"])
        assert_equal(eval([1, 2, 3, 4, 5, 6], split, [1, 2]), [[1], [2, 3], [4], [5, 6]])

    def test_split_integer(self):
        assert_equal(eval([2, 3], split, 1), [[2], [3]])
        with assert_raises(Exception):
            eval([2, 3], split, -1)
        assert_equal(eval([2.0, 3.0], split, 1), [[2.0], [3.0]])

    def test_split_list(self):
        assert_equal(eval([2, 3, 4], split, [1, 1]), [[2], [3], [4]])
        with assert_raises(Exception):
            eval([2, 3, 4], split, [])

        assert_equal(eval([2, 3, 4], split, [1, 1]), [[2], [3], [4]])
        with assert_raises(Exception):
            eval([2, 3, 4], split, [])

        assert_equal(eval([2, 3.0, 4], split, 1), [[2], [3.0], [4]])
        assert_equal(eval([2, 3.0, 1], split, [1, 2]), [[2], [3.0, 1]])
        with assert_raises(Exception):
            eval([2, 3.0, 1], split, [])

    def test_split_errors(self):
        with assert_raises(Exception):
            (eval(1, split, 4))
        with assert_raises(Exception):
            (eval(1, split, 4))

        with assert_raises(Exception):
            (eval(1, split, 4))
        with assert_raises(Exception):
            (eval(1, split, 4))

        with assert_raises(Exception):
            (eval([1], split, 0))
        with assert_raises(Exception):
            (eval([1], split, -1))
        with assert_raises(Exception):
            (eval([1], split, 2.0))

        with assert_raises(Exception):
            (eval([1], split, 0))
        with assert_raises(Exception):
            (eval([1], split, -1))

        with assert_raises(Exception):
            (eval([1], split, 0))
        with assert_raises(Exception):
            (eval([1], split, -1))

class TakeTests(TestCase):
    def test_take_ref(self):
        # Examples:     1#[1 2 3]  -->  [1]
        #               2#[1 2 3]  -->  [1 2]
        #               5#[1 2 3]  -->  [1 2 3 1 2]
        #            (-2)#[1 2 3]  -->  [2 3]
        #            (-5)#[1 2 3]  -->  [2 3 1 2 3]
        #              3#"abcdef"  -->  "abc"
        #           (-3)#"abcdef"  -->  "def"
        #                    0#[]  -->  []
        #                    0#""  -->  ""

        assert_equal(eval([1, 2, 3], take, 1), [1])
        assert_equal(eval([1, 2 ,3], take, 2), [1, 2])
        assert_equal(eval([1, 2, 3], take, 5), [1, 2, 3, 1, 2])
        assert_equal(eval([1, 2, 3], take, -2), [2, 3])
        assert_equal(eval([1, 2, 3], take, -5), [2, 3, 1, 2, 3])
        assert_equal(eval("abcdef", take, 3), "abc")
        assert_equal(eval("abcdef", take, -3), "def")
        assert_equal(eval([], take, 0), [])
        assert_equal(eval("", take, 0), "")

    def test_take_integer(self):
        assert_equal(eval([], take, 1), [])

        assert_equal(eval([0, 1, 0, 2], take, 0), [])
        assert_equal(eval([0, 1, 0, 2], take, 2), [0, 1])
        assert_equal(eval([0, 1, 0, 2], take, -2), [0, 2])
        assert_equal(eval([0, 1, 0, 2], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
        assert_equal(eval([0, 1, 0, 2], take, 6), [0, 1, 0, 2, 0, 1])
        assert_equal(eval([0, 1, 0, 2], take, -6), [0, 2, 0, 1, 0, 2])

        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 2), [0, 1.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, -2), [0, 2.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 0), [])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 6), [0, 1, 0, 2, 0, 1.0])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, -6), [0, 2, 0, 1, 0, 2.0])

        assert_equal(eval([0, 1.0, 0, 2.0], take, 2), [0, 1.0])
        assert_equal(eval([0, 1.0, 0, 2.0], take, -2), [0, 2.0])
        assert_equal(eval([0, 1.0, 0, 2.0], take, 0), [])
        assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
        assert_equal(eval([0, 1.0, 0, 2.0], take, 6), [0, 1, 0, 2, 0, 1.0])
        assert_equal(eval([0, 1.0, 0, 2.0], take, -6), [0, 2, 0, 1, 0, 2.0])

    def test_take_errors(self):
        with assert_raises(Exception):
            eval([], take, [1, 2])
        with assert_raises(Exception):
            eval([0, 1, 0, 2], take, [])

class TimesTests(TestCase):
    def test_times_errors(self):
        with assert_raises(Exception):
            eval(0, times, test_error()())

        with assert_raises(Exception):
            eval([0], times, test_error()())

    def test_times_integer_integer(self):
        assert_equal(eval(1, times, 2), 2)

    def test_times_integer_real(self):
        assert_equal(eval(1, times, 2.0), 2.0)

    def test_times_integer_list(self):
        assert_equal(eval(1, times, [2, 3]), [2, 3])
        assert_equal(eval(1, times, [2.0, 3.0]), [2.0, 3.0])
        assert_equal(eval(1, times, [2, 3.0]), [2, 3.0])

    def test_times_real_integer(self):
        assert_equal(eval(1.0, times, -1), -1.0)

    def test_times_real_real(self):
        assert_equal(eval(1.0, times, 2.0), 2.0)

    def test_times_real_list(self):
        assert_equal(eval(1.0, times, [2, 3]), [2, 3])
        assert_equal(eval(1.0, times, [2.0, 3.0]), [2.0, 3.0])
        assert_equal(eval(1.0, times, [2, 3.0]), [2.0, 3.0])

    def test_times_list_integer(self):
        assert_equal(eval([2, 3], times, 1), [2, 3])
        assert_equal(eval([2.0, 3.0], times, 1), [2.0, 3.0])
        assert_equal(eval([2, 3.0], times, 2), [4, 6.0])

    def test_times_list_real(self):
        assert_equal(eval([2, 3], times, 1.0), [2, 3])
        assert_equal(eval([2.0, 3.0], times, 1.0), [2.0, 3.0])
        assert_equal(eval([2, 3.0], times, 2.0), [4.0, 6.0])

    def test_times_list_list(self):
        assert_equal(eval([2, 3], times, [2, 3]), [4, 9])
        assert_equal(eval([2.0, 3.0], times, [2, 3]), [4.0, 9.0])
        assert_equal(eval([2, 3.0], times, [2, 3]), [4, 9.0])

        assert_equal(eval([2.0, 3.0], times, [2, 3]), [4.0, 9.0])
        assert_equal(eval([2.0, 3.0], times, [2.0, 3.0]), [4.0, 9.0])
        assert_equal(eval([2.0, 3.0], times, [2, 3.0]), [4.0, 9.0])

        assert_equal(eval([2, 3.0], times, [2, 3]), [4, 9.0])
        assert_equal(eval([2, 3.0], times, [2.0, 3.0]), [4.0, 9.0])
        assert_equal(eval([2, 3.0], times, [2, 3.0]), [4, 9])

# Monadic Adverbs
class AdverbTests(TestCase):
    def test_converge(self):
        assert_equal(eval(1, converge, shape), 0)
        assert_equal(eval(1.0, converge, shape), 0)
        assert_equal(eval(C('a'), converge, shape), 0)
        assert_equal(eval([1, 2, 3], converge, shape), [1])
        assert_equal(eval([1.0, 2.0, 3.0], converge, shape), [1])
        assert_equal(eval([1, 2.0, 3], converge, shape), [1])
        assert_equal(eval([1, [2], 3], converge, shape), [1])
        assert_equal(eval("abc", converge, shape), [1])

    def test_each(self):
        assert_equal(eval(1, each, negate), -1)
        assert_equal(eval(1.0, each, negate), -1.0)
        assert_equal(eval([1, 2, 3], each, negate), [-1, -2, -3])
        assert_equal(eval([1.0, 2.0, 3.0], each, negate), [-1.0, -2.0, -3.0])
        assert_equal(eval([1, 2.0, 3], each, negate), [-1, -2, -3])
        assert_equal(eval([1, [2], 3], each, negate), [-1, [-2], -3])
        assert_equal(eval(C('a'), each, reverse), 'a')
        assert_equal(eval("abc", each, reverse), "abc")

    def test_eachPair(self):
        assert_equal(eval(1, eachPair, plus), 1)
        assert_equal(eval(1.0, eachPair, plus), 1.0)
        assert_equal(eval([4, 5, 6], eachPair, plus), [9, 11])
        assert_equal(eval([4.0, 5.0, 6.0], eachPair, plus), [9.0, 11.0])
        assert_equal(eval([4, 5.0, 6], eachPair, plus), [9.0, 11.0])

    def test_over(self):
        assert_equal(eval(4, over, plus), 4)
        assert_equal(eval(4, over, plus), 4.0)

        assert_equal(eval([], over, plus), [])
        assert_equal(eval([4], over, plus), 4)
        assert_equal(eval([4, 5, 6], over, plus), 15)

        assert_equal(eval([4.0], over, plus), 4.0)
        assert_equal(eval([4.0, 5.0, 6.0], over, plus), 15.0)

        assert_equal(eval([4, 5.0, 6], over, plus), 15)

    def test_scanConverging(self):
        assert_equal(eval(1, scanConverging, shape), [1, 0])
        assert_equal(eval(1.0, scanConverging, shape), [1.0, 0])
        assert_equal(eval([1, 2, 3], scanConverging, shape), [[1, 2, 3], [3], [1]])
        assert_equal(eval([1.0, 2.0, 3.0], scanConverging, shape), [[1.0, 2.0, 3.0], [3], [1]])
        assert_equal(eval([1, 2.0, 3], scanConverging, shape),[[1, 2.0, 3], [3], [1]])

    def test_scanOver(self):
        assert_equal(eval(1, scanOver, shape), [1])
        assert_equal(eval(1.0, scanOver, shape), [1])

        assert_equal(eval([], scanOver, plus), [])
        assert_equal(eval([1, 2, 3], scanOver, plus), [1, 3, 6])

        assert_equal(eval([1.0, 2.0, 3.0], scanOver, plus), [1.0, 3.0, 6.0])

        assert_equal(eval([1, 2.0, 3], scanOver, plus), [1, 3.0, 6.0])

    def test_each2(self):
        assert_equal(eval(1, each2, plus, 1), 2)
        assert_equal(eval(1, each2, plus, 1.0), 2.0)
        assert_equal(eval(1.0, each2, plus, 1.0), 2.0)
        assert_equal(eval(1.0, each2, plus, 1), 2.0)

        assert_equal(eval([1, 2, 3], each2, plus, 4), [5, 6, 7])
        assert_equal(eval([1, 2, 3], each2, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1, 2, 3], each2, plus, [4, 5, 6]), [5, 7, 9])
        assert_equal(eval([1, 2, 3], each2, plus, [4.0, 5.0, 6.0]), [5.0, 7.0, 9.0])
        assert_equal(eval([1, 2, 3], each2, plus, [4, 5.0, 6]), [5, 7.0, 9])

        assert_equal(eval([1.0, 2.0, 3.0], each2, plus, 4), [5, 6, 7])
        assert_equal(eval([1.0, 2.0, 3.0], each2, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1.0, 2.0, 3.0], each2, plus, [4, 5, 6]), [5, 7.0, 9])
        assert_equal(eval([1.0, 2.0, 3.0], each2, plus, [4.0, 5.0, 6.0]), [5, 7.0, 9])
        assert_equal(eval([1.0, 2.0, 3.0], each2, plus, [4, 5.0, 6]), [5, 7.0, 9])

        assert_equal(eval([1, 2.0, 3], each2, plus, 4), [5, 6, 7])
        assert_equal(eval([1, 2.0, 3], each2, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1, 2.0, 3], each2, plus, [4, 5, 6]), [5, 7.0, 9])
        assert_equal(eval([1, 2.0, 3], each2, plus, [4.0, 5.0, 6.0]), [5, 7.0, 9])
        assert_equal(eval([1, 2.0, 3], each2, plus, [4, 5.0, 6]), [5, 7.0, 9])

    def test_eachLeft(self):
        assert_equal(eval(1, eachLeft, plus, 4), 5)
        assert_equal(eval(1, eachLeft, plus, 1.0), 2.0)
        assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5, 6, 7])
        assert_equal(eval(1, eachLeft, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1, eachLeft, plus, [4, 5.0, 6]), [5, 6.0, 7])

        assert_equal(eval(1.0, eachLeft, plus, 4), 5.0)
        assert_equal(eval(1.0, eachLeft, plus, 4.0), 5.0)
        assert_equal(eval(1.0, eachLeft, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
        assert_equal(eval(1.0, eachLeft, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1.0, eachLeft, plus, [4, 5.0, 6]), [5.0, 6.0, 7.0])

        assert_equal(eval([1, 2, 3], eachLeft, plus, 4), [5, 6, 7])
        assert_equal(eval([1, 2, 3], eachLeft, plus, 4.0), [5, 6, 7])
        assert_equal(eval([1, 2, 3], eachLeft, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1, 2, 3], eachLeft, plus, [4.0, 5.0, 6.0]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1, 2, 3], eachLeft, plus, [4, 5.0, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])

        assert_equal(eval([1.0, 2.0, 3.0], eachLeft, plus, 4), [5, 6, 7])
        assert_equal(eval([1.0, 2.0, 3.0], eachLeft, plus, 4.0), [5, 6, 7])
        assert_equal(eval([1.0, 2.0, 3.0], eachLeft, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1.0, 2.0, 3.0], eachLeft, plus, [4.0, 5.0, 6.0]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1.0, 2.0, 3.0], eachLeft, plus, [4, 5.0, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])

        assert_equal(eval([1, 2.0, 3], eachLeft, plus, 4), [5, 6.0, 7])
        assert_equal(eval([1, 2.0, 3], eachLeft, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1, 2.0, 3], eachLeft, plus, [4, 5, 6]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])
        assert_equal(eval([1, 2.0, 3], eachLeft, plus, [4.0, 5.0, 6.0]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])
        assert_equal(eval([1, 2.0, 3], eachLeft, plus, [4, 5.0, 6]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])

    def test_eachRight(self):
        assert_equal(eval(1, eachRight, plus, 4), 5)
        assert_equal(eval(1, eachRight, plus, 4.0), 5.0)
        assert_equal(eval(1, eachRight, plus, [4, 5, 6]), [5, 6, 7])
        assert_equal(eval(1, eachRight, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1, eachRight, plus, [4, 5.0, 6]), [5, 6.0, 7])

        assert_equal(eval(1.0, eachRight, plus, 4), 5.0)
        assert_equal(eval(1.0, eachRight, plus, 4.0), 5.0)
        assert_equal(eval(1.0, eachRight, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
        assert_equal(eval(1.0, eachRight, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1.0, eachRight, plus, [4, 5.0, 6]), [5.0, 6.0, 7.0])

        assert_equal(eval([1, 2, 3], eachRight, plus, 4), [5, 6, 7])
        assert_equal(eval([1, 2, 3], eachRight, plus, 4.0), [5, 6, 7])
        assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1, 2, 3], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
        assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5.0, 6]), [[5, 6, 7], [6.0, 7.0, 8.0], [7, 8, 9]])

        assert_equal(eval([1.0, 2.0, 3.0], eachRight, plus, 4), [5, 6, 7])
        assert_equal(eval([1.0, 2.0, 3.0], eachRight, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1.0, 2.0, 3.0], eachRight, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
        assert_equal(eval([1.0, 2.0, 3.0], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
        assert_equal(eval([1.0, 2.0, 3.0], eachRight, plus, [4, 5.0, 6]), [[5, 6, 7], [6.0, 7.0, 8.0], [7, 8, 9]])

        assert_equal(eval([1, 2.0, 3], eachRight, plus, 4), [5, 6.0, 7])
        assert_equal(eval([1, 2.0, 3], eachRight, plus, 4.0), [5.0, 6.0, 7.0])
        assert_equal(eval([1, 2.0, 3], eachRight, plus, [4, 5, 6]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])
        assert_equal(eval([1, 2.0, 3], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
        assert_equal(eval([1, 2.0, 3], eachRight, plus, [4, 5.0, 6]), [[5, 6.0, 7], [6.0, 7.0, 8.0], [7, 8.0, 9]])

    def test_overNeutral(self):
        assert_equal(eval(1, overNeutral, plus, 1), 2)
        assert_equal(eval(1, overNeutral, plus, 1.0), 2.0)
        assert_equal(eval(1, overNeutral, plus, [4, 5, 6]), [5, 6, 7])
        assert_equal(eval(1, overNeutral, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1, overNeutral, plus, [4, 5.0, 6]), [5, 6.0, 7])

        assert_equal(eval(1.0, overNeutral, plus, 1), 2.0)
        assert_equal(eval(1.0, overNeutral, plus, 1.0), 2.0)
        assert_equal(eval(1.0, overNeutral, plus, [4, 5, 6]), [5, 6, 7])
        assert_equal(eval(1.0, overNeutral, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
        assert_equal(eval(1.0, overNeutral, plus, [4, 5.0, 6]), [5.0, 6.0, 7.0])

        assert_equal(eval([], overNeutral, plus, 1), 1)
        assert_equal(eval([1, 2], overNeutral, plus, 1), 4)
        assert_equal(eval([1, 2], overNeutral, plus, 1.0), 4.0)
        assert_equal(eval([1, 2], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
        assert_equal(eval([1, 2], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
        assert_equal(eval([1, 2], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])

        assert_equal(eval([1.0, 2.0], overNeutral, plus, 1), 4)
        assert_equal(eval([1.0, 2.0], overNeutral, plus, 1.0), 4.0)
        assert_equal(eval([1.0, 2.0], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
        assert_equal(eval([1.0, 2.0], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
        assert_equal(eval([1.0, 2.0], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])

        assert_equal(eval([1, 2.0], overNeutral, plus, 1), 4.0)
        assert_equal(eval([1, 2.0], overNeutral, plus, 4.0), 7.0)
        assert_equal(eval([1, 2.0], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
        assert_equal(eval([1, 2.0], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
        assert_equal(eval([1, 2.0], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])

    def test_iterate(self):
        assert_equal(eval(1, iterate, negate, 2), 1)
        assert_equal(eval(1, iterate, negate, 3), -1)

        assert_equal(eval(1.0, iterate, negate, 2), 1.0)
        assert_equal(eval(1.0, iterate, negate, 3), -1.0)

        assert_equal(eval([1, 2, 3], iterate, shape, 2), [1])
        assert_equal(eval([1.0, 2.0, 3.0], iterate, shape, 2), [1])
        assert_equal(eval([1, 2.0, 3], iterate, shape, 2), [1])

    def test_scanIterating(self):
        assert_equal(eval(1, scanIterating, negate, 2), [1, -1, 1])
        assert_equal(eval(1, scanIterating, negate, 3), [1, -1, 1, -1])

        assert_equal(eval(1.0, scanIterating, negate, 2), [1.0, -1.0, 1.0])
        assert_equal(eval(1.0, scanIterating, negate, 3), [1.0, -1.0, 1.0, -1.0])

        assert_equal(eval([1, 2, 3], scanIterating, shape, 2), [[1, 2, 3], [3], [1]])
        assert_equal(eval([1.0, 2.0, 3.0], scanIterating, shape, 2), [[1.0, 2.0, 3.0], [3], [1]])
        assert_equal(eval([1, 2.0, 3], scanIterating, shape, 2), [[1, 2.0, 3], [3], [1]])

    def test_scanOverNeutral(self):
        assert_equal(eval(1, scanOverNeutral, plus, 1), [1, 2])

        assert_equal(eval(1.0, scanOverNeutral, plus, 1), [1, 2])

        assert_equal(eval([1, 2, 3], scanOverNeutral, plus, 1), [1, 2, 4, 7])
        assert_equal(eval([1.0, 2.0, 3.0], scanOverNeutral, plus, 1), [1, 2.0, 4.0, 7.0])
        assert_equal(eval([1, 2.0, 3], scanOverNeutral, plus, 1), [1, 2, 4.0, 7.0])

    def test_scanWhileOne(self):
        assert_equal(eval(0, scanWhileOne, atom, enclose), [0])

        assert_equal(eval(0.0, scanWhileOne, atom, enclose), [0.0])

        assert_equal(eval([], scanWhileOne, atom, enclose), [[]])
        assert_equal(eval([1], scanWhileOne, atom, enclose), [])

        assert_equal(eval([1.0], scanWhileOne, atom, enclose), [])

        assert_equal(eval([1, 2.0], scanWhileOne, atom, enclose), [])

    def test_whileOne(self):
        assert_equal(eval(0, whileOne, atom, enclose), [0])

        assert_equal(eval(0.0, whileOne, atom, enclose), [0.0])

        assert_equal(eval([], whileOne, atom, enclose), [[]])
        assert_equal(eval([1], whileOne, atom, enclose), [1])

        assert_equal(eval([1.0], whileOne, atom, enclose), [1.0])

        assert_equal(eval([1, 2.0], whileOne, atom, enclose), [1, 2.0])

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
