import sys

from sip.api import set_port, eval, evalNoun
from testify import TestCase, assert_equal

#set_port(sys.argv[1])
set_port("/dev/cu.usbmodem1101")

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

# # Examples from the book "An Introduction to Array Programming in Klong" by Nils
# class BookTests(TestCase):
#     pass
#
# # Monads
# class AtomTests(TestCase):
#     # integer atom -> integer, 1)
#     # real atom -> integer, 1)
#     # list <i size equal 0> atom -> integer, 1)
#     # list <i size {equal 0} not> atom -> integer, 0)
#     # list atom -> integer, 0)
#     # char atom -> integer, 1)
#
#     def test_atom_word(self):
#         assert_equal(eval(1, atom), true)
#
#     def test_atom_float(self):
#         assert_equal(eval(1, atom), true)
#
#     def test_atom_word_array(self):
#         assert_equal(eval([2, 3], atom), false)
#
#     def test_atom_real_array(self):
#         assert_equal(eval([2, 3], atom), false)
#
#     def test_atom_mixed_array(self):
#         assert_equal(eval([2, 3.0], atom), false)
#
#     def test_atom_integer(self):
#         assert_equal(eval(1, atom), true)
#
#     def test_atom_real(self):
#         assert_equal(eval(1, atom),  true)
#
#     def test_atom_list(self):
#         assert_equal(eval([2, 3], atom),  false)
#         assert_equal(eval([2.0, 3.0], atom),  false)
#         assert_equal(eval([2, 3.0], atom),  false)
#
# class PlusTests(TestCase):
#     def test_plus_errors(self):
#         with assert_raises(Exception):
#             (eval(0, plus, test_error()))
#         with assert_raises(Exception):
#             (eval([0], plus, test_error()))
#
#     def test_plus_word_word(self):
#         assert_equal(eval(1, plus, 2),  3)
#         assert_equal(eval(-1, plus, -1),  -2)
#         assert_equal(eval(0, plus, 0),  0)
#
#     def test_plus_word_real(self):
#         assert_equal(eval(1, plus, 2.0),  3.0)
#         assert_equal(eval(-1, plus, 1.0),  0.0)
#         assert_equal(eval(0, plus, 0),  0.0)
#
#     def test_plus_word_word_array(self):
#         assert_equal(eval(1, plus, [2, 3]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1]), [0, 1])
#
#     def test_plus_word_real_array(self):
#         assert_equal(eval(1, plus, [2, 3]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1]), [0, 1])
#
#     def test_plus_word_mixed_array(self):
#         assert_equal(eval(1, plus, [2, 3.0]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1.0]), [0, 1.0])
#
#     def test_plus_real_word(self):
#         assert_equal(eval(1.0, plus, 2), 3.0)
#         assert_equal(eval(-1.0, plus, -1), -2.0)
#         assert_equal(eval(0.0, plus, 0), 0.0)
#
#     def test_plus_real_real(self):
#         assert_equal(eval(1.0, plus, 2.0), 3.0)
#         assert_equal(eval(-1.0, plus, 1.0), 0.0)
#         assert_equal(eval(0.0, plus, 0.0), 0.0)
#
#     def test_plus_real_word_array(self):
#         assert_equal(eval(1, plus, [2, 3]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1]), [0, 1])
#
#     def test_plus_real_real_array(self):
#         assert_equal(eval(1, plus, [2, 3]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1]), [0, 1])
#
#     def test_plus_real_mixed_array(self):
#         assert_equal(eval(1, plus, [2, 3.0]), [3, 4])
#         assert_equal(eval(-1, plus, [-1, 0]), [-2, -1])
#         assert_equal(eval(0, plus, [0, 1.0]), [0, 1.0])
#
#     def test_plus_word_array_word(self):
#         assert_equal(eval([2, 3], plus, 1), [3, 4])
#         assert_equal(eval([-1, 0], plus, -1), [-2, -1])
#         assert_equal(eval([0, 1], plus, 0), [0, 1])
#
#     def test_plus_word_array_real(self):
#         assert_equal(eval([2, 3], plus, 1.0), [3.0, 4.0])
#         assert_equal(eval([-1, 0], plus, 1.0), [0.0, 1.0])
#         assert_equal(eval([0, 1], plus, 0.0), [0.0, 1.0])
#
#     def test_plus_word_array_word_array(self):
#         assert_equal(eval([2, 3], plus, [2, 3]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
#         assert_equal(eval([0, 1], plus, [2, 3]), [2, 4])
#
#     def test_plus_word_array_real_array(self):
#         assert_equal(eval([2, 3], plus, [2, 3]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3]),[1, 3])
#         assert_equal(eval([0, 1], plus, [2, 3]), [2, 4])
#
#     def test_plus_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], plus, [2, 3.0]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3.0]), [1, 3])
#         assert_equal(eval([0, 1], plus, [2, 3.0]), [2, 4])
#
#     def test_plus_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], plus, 2), [4, 5])
#         assert_equal(eval([-1, 0], plus, 2), [1, 2.0])
#         assert_equal(eval([0, 1.0], plus, 2), [2, 3.0])
#
#     def test_plus_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], plus, 2.0), [4, 5])
#         assert_equal(eval([-1, 0], plus, 2.0), [1, 2.0])
#         assert_equal(eval([0, 1.0], plus, 2.0), [2, 3])
#
#     def test_plus_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], plus, [2, 3]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
#         assert_equal(eval([0, 1.0], plus, [2, 3]), [2, 4])
#
#     def test_plus_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], plus, [2, 3]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3]), [1, 3])
#         assert_equal(eval([0, 1.0], plus, [2, 3]), [2, 4])
#
#     def test_plus_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], plus, [2, 3.0]), [4, 6])
#         assert_equal(eval([-1, 0], plus, [2, 3.0]), [1, 3])
#         assert_equal(eval([0, 1.0], plus, [2, 3.0]), [2, 4])
#
# class MinusTests(TestCase):
#     def test_minus_errors(self):
#         with assert_raises(Exception):
#             (eval(0, minus, test_error()))
#         with assert_raises(Exception):
#             (eval(0, minus, test_error()))
#         with assert_raises(Exception):
#             (eval([0], minus, test_error()))
#         with assert_raises(Exception):
#             (eval([0], minus, test_error()))
#         with assert_raises(Exception):
#             (eval([0], minus, test_error()))
#
#     def test_minus_word_word(self):
#         assert_equal(eval(1, minus, 2), -1)
#         assert_equal(eval(-1, minus, -1), 0)
#         assert_equal(eval(0, minus, 0), 0)
#
#     def test_minus_word_real(self):
#         assert_equal(eval(1, minus, 2.0), -1.0)
#         assert_equal(eval(-1, minus, 1.0), -2.0)
#         assert_equal(eval(0, minus, 0.0), 0.0)
#
#     def test_minus_word_word_array(self):
#         assert_equal(eval(1, minus, [2, 3]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1]), [0, -1])
#
#     def test_minus_word_real_array(self):
#         assert_equal(eval(1, minus, [2, 3]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1]), [0, -1])
#
#     def test_minus_word_mixed_array(self):
#         assert_equal(eval(1, minus, [2, 3.0]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1.0]), [0, -1])
#
#     def test_minus_real_word(self):
#         assert_equal(eval(1, minus, -1), 2.0)
#         assert_equal(eval(-1, minus, 0), -1.0)
#         assert_equal(eval(0, minus, 0), 0.0)
#
#     def test_minus_real_real(self):
#         assert_equal(eval(1.0, minus, 2.0), -1.0)
#         assert_equal(eval(-1.0, minus, 1.0), -2.0)
#         assert_equal(eval(0.0, minus, 0.0), 0.0)
#
#     def test_minus_real_word_array(self):
#         assert_equal(eval(1, minus, [2, 3]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1]), [0, -1])
#
#     def test_minus_real_real_array(self):
#         assert_equal(eval(1, minus, [2, 3]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1]), [0, -1])
#
#     def test_minus_real_mixed_array(self):
#         assert_equal(eval(1, minus, [2, 3.0]), [-1, -2])
#         assert_equal(eval(-1, minus, [-1, 0]), [0, -1])
#         assert_equal(eval(0, minus, [0, 1.0]), [0, -1])
#
#     def test_minus_word_array_word(self):
#         assert_equal(eval([2, 3], minus, 1), [1, 2])
#         assert_equal(eval([-1, 0], minus, -1), [0, 1])
#         assert_equal(eval([0, 1], minus, 0), [0, 1])
#
#     def test_minus_word_array_real(self):
#         assert_equal(eval([2, 3], minus, 1.0), [1.0, 2.0])
#         assert_equal(eval([-1, 0], minus, 1.0), [-2.0, -1.0])
#         assert_equal(eval([0, 1], minus, 0.0), [0.0, 1.0])
#
#     def test_minus_word_array_word_array(self):
#         assert_equal(eval([2, 3], minus, [2, 3]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
#         assert_equal(eval([0, 1], minus, [2, 3]), [-2, -2])
#
#     def test_minus_word_array_real_array(self):
#         assert_equal(eval([2, 3], minus, [2, 3]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
#         assert_equal(eval([0, 1], minus, [2, 3]), [-2, -2])
#
#     def test_minus_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], minus, [2, 3.0]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3.0]), [-3, -3])
#         assert_equal(eval([0, 1], minus, [2, 3.0]), [-2, -2])
#
#     def test_minus_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], minus, 2), [0, 1.0])
#         assert_equal(eval([-1, 0], minus, 2), [-3, -2])
#         assert_equal(eval([0, 1.0], minus, 2), [-2, -1])
#
#     def test_minus_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], minus, 2.0), [0, 1.0])
#         assert_equal(eval([-1, 0], minus, 2.0), [-3, -2])
#         assert_equal(eval([0, 1.0], minus, 2.0), [-2, -1])
#
#     def test_minus_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], minus, [2, 3]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
#         assert_equal(eval([0, 1.0], minus, [2, 3]), [-2, -2])
#
#     def test_minus_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], minus, [2, 3]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3]), [-3, -3])
#         assert_equal(eval([0, 1.0], minus, [2, 3]), [-2, -2])
#
#     def test_minus_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], minus, [2, 3.0]), [0, 0])
#         assert_equal(eval([-1, 0], minus, [2, 3.0]), [-3, -3])
#         assert_equal(eval([0, 1.0], minus, [2, 3.0]), [-2, -2])
#
# class TimesTests(TestCase):
#     def test_times_errors(self):
#         with assert_raises(Exception):
#             eval(0, times, test_error()())
#
#         with assert_raises(Exception):
#             eval([0], times, test_error()())
#
#     def test_times_word_word(self):
#         assert_equal(eval(1, times, 2), 2)
#
#     def test_times_word_real(self):
#         assert_equal(eval(1, times, 2.0), 2.0)
#
#     def test_times_word_word_array(self):
#         assert_equal(eval(1, times, [2, 3]), [2, 3])
#
#     def test_times_word_real_array(self):
#         assert_equal(eval(1, times, [2, 3]), [2, 3])
#
#     def test_times_word_mixed_array(self):
#         assert_equal(eval(1, times, [2, 3.0]), [2, 3.0])
#
#     def test_times_real_word(self):
#         assert_equal(eval(1, times, -1), -1.0)
#
#     def test_times_real_real(self):
#         assert_equal(eval(1, times, 2.0), 2.0)
#
#     def test_times_real_word_array(self):
#         assert_equal(eval(1, times, [2, 3]), [2, 3])
#
#     def test_times_real_real_array(self):
#         assert_equal(eval(1, times, [2, 3]), [2, 3])
#
#     def test_times_real_mixed_array(self):
#         assert_equal(eval(1, times, [2, 3.0]), [2.0, 3.0])
#
#     def test_times_word_array_word(self):
#         assert_equal(eval([2, 3], times, 1), [2, 3])
#
#     def test_times_word_array_real(self):
#         assert_equal(eval([2, 3], times, 1.0), [2, 3])
#
#     def test_times_word_array_word_array(self):
#         assert_equal(eval([2, 3], times, [2, 3]), [4, 9])
#
#     def test_times_word_array_real_array(self):
#         assert_equal(eval([2, 3], times, [2, 3]), [4, 9])
#
#     def test_times_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], times, [2, 3.0]), [4, 9.0])
#
#     def test_times_real_array_word(self):
#         assert_equal(eval([2, 3], times, 1), [2, 3])
#
#     def test_times_real_array_real(self):
#         assert_equal(eval([2, 3], times, 1.0), [2, 3])
#
#     def test_times_real_array_word_array(self):
#         assert_equal(eval([2, 3], times, [2, 3]), [4, 9])
#
#     def test_times_real_array_real_array(self):
#         assert_equal(eval([2, 3], times, [2, 3]), [4, 9])
#
#     def test_times_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], times, [2, 3.0]), [4.0, 9.0])
#
#     def test_times_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], times, 2), [4, 6.0])
#
#     def test_times_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], times, 2.0), [4.0, 6.0])
#
#     def test_times_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], times, [2, 3]), [4, 9.0])
#
#     def test_times_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], times, [2, 3]), [4.0, 9.0])
#
#     def test_times_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], times, [2, 3.0]), [4, 9])
#
# class PowerTests(TestCase):
#     def test_power_word_word(self):
#         assert_equal(eval(2, power, 2), 4.0)
#
#     def test_power_word_real(self):
#         assert_equal(eval(2, power, 2.0), 4.0)
#
#     def test_power_word_word_array(self):
#         assert_equal(eval(2, power, [2, 3]), [4, 8])
#
#     def test_power_word_real_array(self):
#         assert_equal(eval(2, power, [2, 3]), [4, 8])
#
#     def test_power_word_mixed_array(self):
#         assert_equal(eval(2, power, [2, 3.0]), [4.0, 8.0])
#
#     def test_power_real_word(self):
#         assert_equal(eval(2, power, 2), 4.0)
#
#     def test_power_real_real(self):
#         assert_equal(eval(2, power, 2.0), 4.0)
#
#     def test_power_real_word_array(self):
#         assert_equal(eval(2, power, [2, 3]), [4, 8])
#
#     def test_power_real_real_array(self):
#         assert_equal(eval(2, power, [2, 3]), [4, 8])
#
#     def test_power_real_mixed_array(self):
#         assert_equal(eval(2, power, [2, 3.0]), [4, 8])
#
#     def test_power_word_array_word(self):
#         assert_equal(eval([2, 3], power, 3), [8, 27])
#
#     def test_power_word_array_real(self):
#         assert_equal(eval([2, 3], power, 1.0), [2, 3])
#
#     def test_power_word_array_word_array(self):
#         assert_equal(eval([2, 3], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_word_array_real_array(self):
#         assert_equal(eval([2, 3], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], power, [2, 3.0]), [[4.0, 8.0], [9.0, 27.0]])
#
#     def test_power_real_array_word(self):
#         assert_equal(eval([2, 3], power, 3), [8, 27])
#
#     def test_power_real_array_real(self):
#         assert_equal(eval([2, 3], power, 1.0), [2, 3])
#
#     def test_power_real_array_word_array(self):
#         assert_equal(eval([2, 3], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_real_array_real_array(self):
#         assert_equal(eval([2, 3], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], power, [2, 3.0]), [[4.0, 8.0], [9.0, 27.0]])
#
#     def test_power_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], power, 2), [4.0, 9.0])
#
#     def test_power_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], power, 2.0), [4, 9])
#
#     def test_power_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], power, [2, 3]), [[4, 8], [9, 27]])
#
#     def test_power_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], power, [2, 3.0]), [[4.0, 8.0], [9.0, 27.0]])
#
# class DivideTests(TestCase):
#     def test_divide_errors(self):
#         with assert_raises(Exception):
#             (eval(0, divide, test_error()))
#         with assert_raises(Exception):
#             (eval(0, divide, test_error()))
#         with assert_raises(Exception):
#             (eval([0], divide, test_error()))
#         with assert_raises(Exception):
#             (eval([0], divide, test_error()))
#         with assert_raises(Exception):
#             (eval([0], divide, test_error()))
#
#     def test_divide_word_word(self):
#         assert_equal(eval(1, divide, 2), 1.0 / 2.0)
#         with assert_raises(Exception):
#             (eval(1, divide, 0))
#
#     def test_divide_word_real(self):
#         assert_equal(eval(1, divide, 2.0), 0.5)
#         with assert_raises(Exception):
#             (eval(1, divide, 0))
#
#     def test_divide_word_word_array(self):
#         assert_equal(eval(1, divide, [2, 3]), [1.0 / 2.0, 1.0 / 3.0])
#         with assert_raises(Exception):
#             (eval(1, divide, [0, 3]))
#
#     def test_divide_word_real_array(self):
#         assert_equal(eval(1, divide, [2, 3]), [1.0 / 2.0, 1.0 / 3.0])
#         with assert_raises(Exception):
#             (eval(1, divide, [0, 3]))
#
#     def test_divide_word_mixed_array(self):
#         assert_equal(eval(1, divide, [2, 3.0]), [1.0 / 2.0, 1.0 / 3.0])
#         with assert_raises(Exception):
#             (eval(1, divide, [0, 3]))
#
#     def test_divide_real_word(self):
#         assert_equal(eval(1, divide, -1), -1.0)
#         with assert_raises(Exception):
#             (eval(1, divide, 0))
#
#     def test_divide_real_real(self):
#         assert_equal(eval(1, divide, 2.0), 0.5)
#         with assert_raises(Exception):
#             (eval(1, divide, 0))
#
#     def test_divide_real_word_array(self):
#         assert_equal(eval(1, divide, [2, 3]), [1.0 / 2.0, 1.0 / 3.0])
#
#     def test_divide_real_real_array(self):
#         assert_equal(eval(1, divide, [2, 3]), [1.0/2.0, 1.0/3.0])
#
#     def test_divide_real_mixed_array(self):
#         assert_equal(eval(1, divide, [2, 3.0]), [1.0 / 2.0, 1.0 / 3.0])
#
#     def test_divide_word_array_word(self):
#         assert_equal(eval([2, 3], divide, 1), [2, 3])
#
#     def test_divide_word_array_real(self):
#         assert_equal(eval([2, 3], divide, 1.0), [2, 3])
#
#     def test_divide_word_array_word_array(self):
#         assert_equal(eval([2, 3], divide, [2, 3]), [1, 1])
#
#     def test_divide_word_array_real_array(self):
#         assert_equal(eval([2, 3], divide, [2, 3]), [1, 1])
#
#     def test_divide_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], divide, [2, 3.0]), [1, 1.0])
#
#     def test_divide_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], divide, 2), [1, 3.0 / 2.0])
#
#     def test_divide_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], divide, 2.0), [1, 3.0 / 2.0])
#
#     def test_divide_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], divide, [2, 3]), [1, 1.0])
#
#     def test_divide_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], divide, [2, 3]), [1, 1.0])
#
#     def test_divide_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], divide, [2, 3.0]), [1, 1.0])
#
# class NegateTests(TestCase):
#     def test_negate_word(self):
#         assert_equal(eval(1, negate), -1)
#
#     def test_negate_real(self):
#         assert_equal(eval(1, negate), -1.0)
#
#     def test_negate_word_array(self):
#         assert_equal(eval([2, 3], negate), [-2, -3])
#
#     def test_negate_real_array(self):
#         assert_equal(eval([2, 3], negate), [-2, -3])
#
#     def test_negate_mixed_array(self):
#         assert_equal(eval([2, 3.0], negate), [-2, -3])
#
#
# class ReciprocalTests(TestCase):
#     def test_reciprocal_word(self):
#         assert_equal(eval(2, reciprocal), 1.0 / 2.0)
#
#     def test_reciprocal_real(self):
#         assert_equal(eval(2, reciprocal), 1.0/2.0)
#
#     def test_reciprocal_word_array(self):
#         assert_equal(eval([2, 3], reciprocal), [1.0 / 2.0, 1.0 / 3.0])
#
#     def test_reciprocal_real_array(self):
#         assert_equal(eval([2, 3], reciprocal), [1.0/2.0, 1.0/3.0])
#
#     def test_reciprocal_mixed_array(self):
#         assert_equal(eval([2, 3.0], reciprocal), [1.0 / 2.0, 1.0 / 3.0])
#
# class EnumerateTests(TestCase):
#     def test_enumerate(self):
#         assert_equal(eval(5, enumerate), [1, 2, 3, 4, 5])
#
# class ComplementationTests(TestCase):
#     def test_complementation_word(self):
#         assert_equal(eval(5, complementation), -4)
#
#     def test_complementation_real(self):
#         assert_equal(eval(5, complementation), -4)
#
#     def test_complementation_word_array(self):
#         assert_equal(eval([0, 1, 2], complementation), [1, 0, -1])
#
#     def test_complementation_real_array(self):
#         assert_equal(eval([0, 1, 2], complementation), [1, 0, -1])
#
#     def test_complementation_mixed_array(self):
#         assert_equal(eval([0, 1.0, 2], complementation), [1, 0.0, -1])
#
# class FloorTests(TestCase):
#     def test_floor_word(self):
#         assert_equal(eval(5, floor), 5)
#
#     def test_floor_real(self):
#         assert_equal(eval(5.5, floor), 5)
#
#     def test_floor_word_array(self):
#         assert_equal(eval([0, 1, 2], floor), [0, 1, 2])
#
#     def test_floor_real_array(self):
#         assert_equal(eval([0.1, 1.5, 2.9], floor), [0, 1, 2])
#
#     def test_floor_mixed_array(self):
#         assert_equal(eval([0, 1, 2], floor), [0, 1, 2])
#
# class ReverseTests(TestCase):
#     def test_reverse_word_array(self):
#         assert_equal(eval([0, 1, 2], reverse), [2, 1, 0])
#
#     def test_reverse_real_array(self):
#         assert_equal(eval([0, 1, 2], reverse), [2, 1, 0])
#
#     def test_reverse_mixed_array(self):
#         assert_equal(eval([0, 1, 2], reverse), [2, 1, 0])
#
# class FirstTests(TestCase):
#     def test_first_word_array(self):
#         assert_equal(eval([0, 1, 2], first), 0)
#
#     def test_first_real_array(self):
#         assert_equal(eval([0, 1, 2], first), 0.0)
#
#     def test_first_mixed_array(self):
#         assert_equal(eval([0, 1, 2], first), 0)
#
# class ShapeTests(TestCase):
#     def test_shape_word(self):
#         assert_equal(eval(5, shape), 0)
#
#     def test_shape_real(self):
#         assert_equal(eval(5.5, shape), 0)
#
#     def test_shape_word_array(self):
#         assert_equal(eval([0, 1, 2], shape), [3])
#
#     def test_shape_real_array(self):
#         assert_equal(eval([0.1, 1.5, 2.9], shape), [3])
#
#     def test_shape_mixed_array(self):
#         assert_equal(eval([0, 1, [1, 2, 3]], shape), [3])
#         assert_equal(eval([[0], [1], [0]], shape), [3, 1])
#
# class RankTests(TestCase):
#     def test_shape_word(self):
#         assert_equal(eval(5, shape, size), 0)
#
#     def test_shape_real(self):
#         assert_equal(eval(5.5, shape, size), 0)
#
#     def test_shape_word_array(self):
#         assert_equal(eval([0, 1, 2], shape, size), 1)
#
#     def test_shape_real_array(self):
#         assert_equal(eval([0.1, 1.5, 2.9], shape, size), 1)
#
#     def test_shape_mixed_array(self):
#         assert_equal(eval([0, 1, [1, 2, 3]], shape, size), 1)
#         assert_equal(eval([[0], [1], [0]], shape, size), 2)
#
# class EncloseTests(TestCase):
#     def test_enclose_word(self):
#         assert_equal(eval(5, enclose), [5])
#
#     def test_enclose_real(self):
#         assert_equal(eval(5.5, enclose), [5.5])
#
#     def test_enclose_word_array(self):
#         assert_equal(eval([0, 1, 2], enclose), [[0, 1, 2]])
#
#     def test_enclose_real_array(self):
#         assert_equal(eval([0, 1, 2], enclose), [[0, 1, 2]])
#
#     def test_enclose_mixed_array(self):
#         assert_equal(eval([0, 1, [1, 2, 3]], enclose), [[0, 1, [1, 2, 3]]])
#
# class UniqueTests(TestCase):
#     def test_unique_word_array(self):
#         assert_equal(eval([0, 1, 0, 2], unique), [0, 1, 2])
#
#     def test_unique_real_array(self):
#         assert_equal(eval([0, 1, 0, 2], unique), [0, 1, 2])
#
#     def test_unique_mixed_array(self):
#         assert_equal(eval([0, 1.0, 0, 2.0], unique), [0, 1.0, 2.0])
#
# class TakeTests(TestCase):
#     def test_take_word_array(self):
#         assert_equal(eval([0, 1, 0, 2], take, 2), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, -2), [0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, 0), [])
#         assert_equal(eval([0, 1, 0, 2], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
#         assert_equal(eval([0, 1, 0, 2], take, 6), [0, 1, 0, 2, 0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, -6), [0, 2, 0, 1, 0, 2])
#         assert_equal(eval([], take, 1), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, 0.0), [])
#         assert_equal(eval([0, 1, 0, 2], take, 0.5), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, 1.0), [0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, 2.0), [0, 1, 0, 2, 0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, -2.0), [0, 1, 0, 2, 0, 1, 0, 2])
#         assert_equal(eval([], take, 0.5), [])
#         assert_equal(eval([], take, 1.0), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [1]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [1, 2]), [[0], [0, 1]])
#         assert_equal(eval([], take, [1, 2]), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25, 0.5]), [[0], [0, 1]])
#         assert_equal(eval([], take, [1, 2]), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [1]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [1, 0.5]), [[0], [0, 1]])
#         assert_equal(eval([], take, [1, 2.0]), [])
#         assert_equal(eval([], take, [1, 2.0]), [])
#
#     def test_take_real_array(self):
#         assert_equal(eval([0, 1, 0, 2], take, 2), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, -2), [0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, 0), [])
#         assert_equal(eval([0, 1, 0, 2], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
#         assert_equal(eval([0, 1, 0, 2], take, 6), [0, 1, 0, 2, 0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, -6), [0, 2, 0, 1, 0, 2])
#         assert_equal(eval([], take, 1), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, 0.0), [])
#         assert_equal(eval([0, 1, 0, 2], take, 0.5), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], take, 1.0), [0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, 2.0), [0, 1, 0, 2, 0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], take, -2.0), [0, 1, 0, 2, 0, 1, 0, 2])
#         assert_equal(eval([], take, 0.5), [])
#         assert_equal(eval([], take, 1.0), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [1]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [1, 2]), [[0], [0, 1]])
#         assert_equal(eval([], take, [1, 2]), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25, 0.5]), [[0], [0, 1]])
#         assert_equal(eval([], take, [0.25, 0.5]), [])
#
#         assert_equal(eval([0, 1, 0, 2], take, []), [])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25]), [[0]])
#         assert_equal(eval([0, 1, 0, 2], take, [0.25, 0.5]), [[0], [0, 1]])
#         assert_equal(eval([], take, [0.25, 0.5]), [])
#
#         assert_equal(eval([], take, [1, 2.0]), [])
#
#     def test_take_mixed_array(self):
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 2), [0, 1.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, -2), [0, 2.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 0), [])
#         assert_equal(eval([0.0, 1.0, 0.0, 2.0], take, 9), [0, 1, 0, 2, 0, 1, 0, 2, 0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 6), [0, 1, 0, 2, 0, 1.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, -6), [0, 2, 0, 1, 0, 2.0])
#         assert_equal(eval([], take, 1), [])
#
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 0.0), [])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 0.5), [0, 1.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 1.0), [0, 1.0, 0, 2.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, 2.0), [0, 1, 0, 2, 0, 1, 0, 2.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, -2.0), [0, 1, 0, 2, 0, 1, 0, 2.0])
#         assert_equal(eval([], take, 0.5), [])
#         assert_equal(eval([], take, 1.0), [])
#
#         assert_equal(eval([0, 1.0, 0, 2.0], take, []), [])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, [1]), [[0]])
#         assert_equal(eval([0, 1.0, 0, 2.0], take, [1, 2]), [[0], [0, 1.0]])
#         assert_equal(eval([], take, [1, 2]), [])
#         assert_equal(eval([], take, [1, 2.0]), [])
#
# class DropTests(TestCase):
#     def test_drop_word_array(self):
#         assert_equal(eval([0, 1, 0, 2], drop, 2), [0, 2])
#         assert_equal(eval([0, 1, 0, 2], drop, -2), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], drop, 0), [0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], drop, 100), [])
#         assert_equal(eval([], drop, 100), [])
#         assert_equal(eval([0, 1, 0, 2], drop, -100), [])
#         assert_equal(eval([], drop, -100), [])
#
#     def test_drop_real_array(self):
#         assert_equal(eval([0, 1, 0, 2], drop, 2), [0, 2])
#         assert_equal(eval([0, 1, 0, 2], drop, -2), [0, 1])
#         assert_equal(eval([0, 1, 0, 2], drop, 0), [0, 1, 0, 2])
#         assert_equal(eval([0, 1, 0, 2], drop, 100), [])
#         assert_equal(eval([], drop, 100), [])
#         assert_equal(eval([0, 1, 0, 2], drop, -100), [])
#         assert_equal(eval([], drop, -100), [])
#
#     def test_drop_mixed_array(self):
#         assert_equal(eval([0, 1.0, 0, 2.0], drop, 2), [0, 2.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], drop, -2), [0, 1.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], drop, 0), [0, 1.0, 0, 2.0])
#         assert_equal(eval([0, 1.0, 0, 2.0], drop, 100), [])
#         assert_equal(eval([], drop, 100), [])
#         assert_equal(eval([0, 1.0, 0, 2.0], drop, -100), [])
#         assert_equal(eval([], drop, -100), [])
#
#     def test_drop_errors(self):
#         with assert_raises(Exception):
#             (eval(1, drop, -1))
#
#         with assert_raises(Exception):
#             (eval(1, drop, 1.0))
#
#         with assert_raises(Exception):
#             (eval(1, drop, -1))
#
#         with assert_raises(Exception):
#             (eval(1, drop, 1.0))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], drop, 1.0))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], drop, 1.0))
#
#         with assert_raises(Exception):
#             (eval([1, 2.0, 3], drop, 1.0))
#
# class JoinTests(TestCase):
#     def test_join_word_word(self):
#         assert_equal(eval(1, join, 2), [1, 2])
#
#     def test_join_word_real(self):
#         assert_equal(eval(1, join, 2.0), [1, 2.0])
#
#     def test_join_word_word_array(self):
#         assert_equal(eval(1, join, [2, 3]), [1, 2, 3])
#
#     def test_join_word_real_array(self):
#         assert_equal(eval(1, join, [2, 3]), [1, 2, 3])
#
#     def test_join_word_mixed_array(self):
#         assert_equal(eval(1, join, [2, 3.0]), [1, 2, 3])
#
#     def test_join_real_word(self):
#         assert_equal(eval(1, join, -1), [1, -1])
#
#     def test_join_real_real(self):
#         assert_equal(eval(1, join, 2.0), [1, 2])
#
#     def test_join_real_word_array(self):
#         assert_equal(eval(1, join, [2, 3]), [1, 2, 3])
#
#     def test_join_real_real_array(self):
#         assert_equal(eval(1, join, [2, 3]), [1, 2, 3])
#
#     def test_join_real_mixed_array(self):
#         assert_equal(eval(1, join, [2, 3.0]), [1, 2, 3])
#
#     def test_join_word_array_word(self):
#         assert_equal(eval([2, 3], join, 1), [2, 3, 1])
#
#     def test_join_word_array_real(self):
#         assert_equal(eval([2, 3], join, 1.0), [2, 3, 1])
#
#     def test_join_word_array_word_array(self):
#         assert_equal(eval([2, 3], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_word_array_real_array(self):
#         assert_equal(eval([2, 3], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], join, [2, 3.0]), [2, 3, 2, 3])
#
#     def test_join_real_array_word(self):
#         assert_equal(eval([2, 3], join, 1), [2, 3, 1])
#
#     def test_join_real_array_real(self):
#         assert_equal(eval([2, 3], join, 1.0), [2, 3, 1])
#
#     def test_join_real_array_word_array(self):
#         assert_equal(eval([2, 3], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_real_array_real_array(self):
#         assert_equal(eval([2, 3], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], join, [2, 3.0]), [2, 3, 2, 3])
#
#     def test_join_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], join, 2), [2, 3.0, 2])
#
#     def test_join_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], join, 2.0), [2, 3, 2.0])
#
#     def test_join_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], join, [2, 3]), [2, 3, 2, 3])
#
#     def test_join_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], join, [2, 3.0]), [2, 3, 2, 3])
#
# class RotateTests(TestCase):
#     def test_rotate_word_word_array(self):
#         assert_equal(eval(1, rotate, [0, 1, 2]), [1, 2, 0])
#         assert_equal(eval(-1, rotate, [0, 1, 2]), [2, 0, 1])
#         assert_equal(eval(1, rotate, []), [])
#         assert_equal(eval(0, rotate, [0, 1, 2]), [0, 1, 2])
#
#         assert_equal(eval(1, rotate, [0, 1, 2]), [1, 2, 0])
#         assert_equal(eval(-1, rotate, [0, 1, 2]), [2, 0, 1])
#         assert_equal(eval(1, rotate, []), [])
#         assert_equal(eval(0, rotate, [0, 1, 2]), [0, 1, 2])
#
#         assert_equal(eval(1, rotate, [0, 1, 2]), [1, 2, 0])
#         assert_equal(eval(-1, rotate, [0, 1, 2]), [2, 0, 1])
#         assert_equal(eval(1, rotate, []), [])
#         assert_equal(eval(0, rotate, [0, 1, 2]), [0, 1, 2])
#
#         with assert_raises(Exception):
#             (eval(1, rotate, 1))
#
#     def test_rotate_word_array(self):
#         assert_equal(eval([0, 1, 2], rotate, 1), [1, 2, 0])
#         assert_equal(eval([0, 1, 2], rotate, 4), [1, 2, 0])
#         assert_equal(eval([0, 1, 2], rotate, -1), [2, 0, 1])
#         assert_equal(eval([0, 1, 2], rotate, -4), [2, 0, 1])
#         assert_equal(eval([], rotate, 1), [])
#         assert_equal(eval([0, 1, 2], rotate, 0), [0, 1, 2])
#
#     def test_rotate_real_array(self):
#         assert_equal(eval([0, 1, 2], rotate, 1), [1, 2, 0])
#         assert_equal(eval([0, 1, 2], rotate, 4), [1, 2, 0])
#         assert_equal(eval([0, 1, 2], rotate, -1), [2, 0, 1])
#         assert_equal(eval([0, 1, 2], rotate, -4), [2, 0, 1])
#         assert_equal(eval([], rotate, 1), [])
#         assert_equal(eval([0, 1, 2], rotate, 0), [0, 1, 2])
#
#     def test_rotate_mixed_array(self):
#         assert_equal(eval([0, 1, [1, 2, 3]], rotate, 1), [1, [1, 2, 3], 0])
#         assert_equal(eval([0, 1, [1, 2, 3]], rotate, 4), [1, [1, 2, 3], 0])
#         assert_equal(eval([0, 1, [1, 2, 3]], rotate, -1), [[1, 2, 3], 0, 1.0])
#         assert_equal(eval([0, 1, [1, 2, 3]], rotate, -4), [[1, 2, 3], 0, 1.0])
#         assert_equal(eval([], rotate, -1), [])
#         assert_equal(eval([0, 1, [1, 2, 3]], rotate, 0), [0, 1, [1, 2, 3]])
#
#     def test_rotate_errors(self):
#         with assert_raises(Exception):
#             (eval(test_error(), rotate, [1, 2, 3]))
#
#         with assert_raises(Exception):
#             (eval(test_error(), rotate, [1, 2, 3]))
#
#         with assert_raises(Exception):
#             (eval(test_error(), rotate, [1, 2.0, 3]))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, 1.0))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, 1.0))
#         with assert_raises(Exception):
#             (eval([1, 2, [3, 4, 5]], rotate, 1.0))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, test_error()))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, [3, 4, 5]], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, test_error()))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, [3, 4, 5]], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, test_error()))
#
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, test_error()))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, [3, 4, 5]], rotate, [1]))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], rotate, [1]))
#
# class SplitTests(TestCase):
#     def test_split_word_word_array(self):
#         assert_equal(eval(1, split, [2, 3]), [[2], [3]])
#
#     def test_split_word_real_array(self):
#         assert_equal(eval(1, split, [2, 3]), [[2], [3]])
#
#     def test_split_word_mixed_array(self):
#         assert_equal(eval(1, split, [2, 3.0]), [[2], [3.0]])
#
#     def test_split_real_word_array(self):
#         assert_equal(eval(0.5, split, [2, 3]), [[2], [3]])
#
#     def test_split_real_real_array(self):
#         assert_equal(eval(0.5, split, [2, 3]), [[2], [3]])
#
#     def test_split_real_mixed_array(self):
#         assert_equal(eval(0.5, split, [2, 3.0]), [[2], [3.0]])
#
#     def test_split_word_array_word(self):
#         assert_equal(eval([2, 3], split, 1), [[2], [3]])
#         with assert_raises(Exception):
#             eval([2, 3], split, -1)
#
#     def test_split_word_array_real(self):
#         assert_equal(eval([2, 3], split, 0.5), [[2], [3]])
#         assert_equal(eval([1], split, 0.0), [])
#
#     def test_split_word_array_word_array(self):
#         assert_equal(eval([2, 3, 4], split, [1, 1]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_word_array_real_array(self):
#         assert_equal(eval([2, 3, 4], split, [0.5, 0.5]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_word_array_mixed_array(self):
#         assert_equal(eval([2, 3, 4], split, [1, 0.5]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_real_array_word(self):
#         assert_equal(eval([2.0, 3.0], split, 1), [[2.0], [3.0]])
#
#     def test_split_real_array_real(self):
#         assert_equal(eval([2, 3], split, 0.5), [[2], [3]])
#         with assert_raises(Exception):
#             eval([2, 3], split, 0)
#         with assert_raises(Exception):
#             eval([1], split, 0)
#
#     def test_split_real_array_word_array(self):
#         assert_equal(eval([2, 3, 4], split, [1, 1]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_real_array_real_array(self):
#         assert_equal(eval([2, 3, 4], split, [0.5, 0.5]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_real_array_mixed_array(self):
#         assert_equal(eval([2, 3, 4], split, [1, 0.5]), [[2], [3], [4]])
#         with assert_raises(Exception):
#             eval([2, 3, 4], split, [])
#
#     def test_split_mixed_array_word(self):
#         assert_equal(eval([2, 3.0, 4], split, 1), [[2], [3.0], [4]])
#
#     def test_split_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], split, 0.5), [[2], [3.0]])
#         assert_equal(eval([1], split, 0.0), [])
#
#     def test_split_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0, 1], split, [1, 2]), [[2], [3.0, 1]])
#         with assert_raises(Exception):
#             eval([2, 3.0, 1], split, [])
#
#     def test_split_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0, 1], split, [0.5, 0.5]), [[2], [3.0], [1]])
#         with assert_raises(Exception):
#             eval([2, 3.0, 1], split, [])
#
#     def test_split_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0, 1], split, [1, 0.5]), [[2], [3.0], [1]])
#         with assert_raises(Exception):
#             eval([2, 3.0, 1], split, []), [[2], [3.0], [1]]
#
#     def test_split_errors(self):
#         with assert_raises(Exception):
#             (eval(1, split, 4))
#         with assert_raises(Exception):
#             (eval(1, split, 4))
#
#         with assert_raises(Exception):
#             (eval(1, split, 4))
#         with assert_raises(Exception):
#             (eval(1, split, 4))
#
#         with assert_raises(Exception):
#             (eval([], split, 4))
#         with assert_raises(Exception):
#             (eval([1], split, 0))
#         with assert_raises(Exception):
#             (eval([1], split, -1))
#         with assert_raises(Exception):
#             (eval([1], split, 2.0))
#
#         with assert_raises(Exception):
#             (eval([], split, 4))
#         with assert_raises(Exception):
#             (eval([1], split, 0))
#         with assert_raises(Exception):
#             (eval([1], split, -1))
#
#         with assert_raises(Exception):
#             (eval([], split, 4))
#         with assert_raises(Exception):
#             (eval([1], split, 0))
#         with assert_raises(Exception):
#             (eval([1], split, -1))
#
# class FindTests(TestCase):
#     def test_find_word_word(self):
#         with assert_raises(Exception):
#             (eval(2, find, 1))
#
#     def test_find_word_real(self):
#         with assert_raises(Exception):
#             (eval(2, find, 1))
#
#     def test_find_word_word_array(self):
#         assert_equal(eval(2, find, [1, 2, 3]), [0, 1, 0])
#
#     def test_find_word_real_array(self):
#         assert_equal(eval(2, find, [1, 2, 3]), [0, 1, 0])
#
#     def test_find_word_mixed_array(self):
#         assert_equal(eval(2, find, [1, 2, 3]), [0, 1, 0])
#
#     def test_find_real_word_array(self):
#         assert_equal(eval(2, find, [1, 2, 3]), [0, 1, 0])
#
#     def test_find_real_real_array(self):
#         assert_equal(eval(2, find, [1, 2, 3]), [0, 1, 0])
#
#     def test_find_real_mixed_array(self):
#         assert_equal(eval(3, find, [1, 2, 3]), [0, 0, 1])
#
#     def test_find_word_array_word(self):
#         assert_equal(eval([1, 2, 3], find, 2), [0, 1, 0])
#
#     def test_find_word_array_real(self):
#         assert_equal(eval([1, 2, 3], find, 2.0), [0, 1, 0])
#
#     def test_find_word_array_word_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_word_array_real_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_word_array_mixed_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_real_array_word(self):
#         assert_equal(eval([1, 2, 3], find, 2), [0, 1, 0])
#
#     def test_find_real_array_real(self):
#         assert_equal(eval([1, 2, 3], find, 2.0), [0, 1, 0])
#
#     def test_find_real_array_word_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_real_array_real_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_real_array_mixed_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_mixed_array_word(self):
#         assert_equal(eval([1, 2, 3], find, 2), [0, 1, 0])
#
#     def test_find_mixed_array_real(self):
#         assert_equal(eval([1.0, 2.0, 3.0], find, 2.0), [0, 1, 0])
#
#     def test_find_mixed_array_word_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3]), [0, 1, 0])
#
#     def test_find_mixed_array_real_array(self):
#         assert_equal(eval([1.0, 2.0, 3.0], find, [2, 3]), [0, 1, 0])
#
#     def test_find_mixed_array_mixed_array(self):
#         assert_equal(eval([1, 2, 3], find, [2, 3.0]), [0, 1, 0])
#
# class RemainderTests(TestCase):
#     def test_remainder_word_word(self):
#         assert_equal(eval(10, remainder, 2), 0)
#
#     def test_remainder_word_word_array(self):
#         assert_equal(eval(10, remainder, [2, 3]), [0, 1])
#
#     def test_remainder_word_mixed_array(self):
#         assert_equal(eval(10, remainder, [2, 3]), [0, 1])
#
#     def test_remainder_word_array_word(self):
#         assert_equal(eval([10, 9], remainder, 2), [0, 1])
#
#     def test_remainder_word_array_word_array(self):
#         assert_equal(eval([10, 9], remainder, [2, 3]), [[0, 1], [1, 0]])
#
#     def test_remainder_word_array_mixed_array(self):
#         assert_equal(eval([10, 9], remainder, [2, 3]), [[0, 1], [1, 0]])
#
#     def test_remainder_mixed_array_word(self):
#         assert_equal(eval([10, 9], remainder, 2), [0, 1])
#
#     def test_remainder_mixed_array_word_array(self):
#         assert_equal(eval([10, 9], remainder, [2, 3]), [[0, 1], [1, 0]])
#
#     def test_remainder_mixed_array_mixed_array(self):
#         assert_equal(eval([10, 9], remainder, [2, 3]), [[0, 1], [1, 0]])
#
#     def test_remainder_errors(self):
#         with assert_raises(Exception):
#             (eval(10, remainder, [2.0, 3.0]))
#         with assert_raises(Exception):
#             (eval(10, remainder, [2, 3.0]))
#         with assert_raises(Exception):
#             (eval([10], remainder, [2.0, 3.0]))
#         with assert_raises(Exception):
#             (eval([10], remainder, [2, 3.0]))
#         with assert_raises(Exception):
#             (eval(10.0, remainder, [2, 3]))
#
# class MatchTests(TestCase):
#     def test_match_word_word(self):
#         assert_equal(eval(10, match, 10), 1)
#
#     def test_match_word_real(self):
#         assert_equal(eval(10, match, 10), 1)
#
#     def test_match_word_word_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_word_real_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_word_mixed_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_real_word(self):
#         assert_equal(eval(10, match, 10), 1)
#
#     def test_match_real_real(self):
#         assert_equal(eval(10, match, 10), 1)
#
#     def test_match_real_word_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_real_real_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_real_mixed_array(self):
#         assert_equal(eval(10, match, [2, 3]), 0)
#
#     def test_match_word_array_word(self):
#         assert_equal(eval([1, 2, 3], match, 2), 0)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#
#     def test_match_word_array_real(self):
#         assert_equal(eval([2, 3], match, 2.0), 0)
#
#     def test_match_word_array_word_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#
#     def test_match_word_array_real_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#
#     def test_match_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#
#     def test_match_real_array_word(self):
#         assert_equal(eval([1, 2, 3], match, 2), 0)
#
#     def test_match_real_array_real(self):
#         assert_equal(eval([1, 2, 3], match, 2.0), 0)
#
#     def test_match_real_array_word_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#         assert_equal(eval([2, 3], match, [4, 5]), 0)
#
#     def test_match_real_array_real_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#
#     def test_match_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], match, [2, 3]), 1)
#
#     def test_match_mixed_array_word(self):
#         assert_equal(eval([1, 2.0, 3], match, 2), 0)
#
#     def test_match_mixed_array_word_array(self):
#         assert_equal(eval([1, 2.0, 3], match, [1, 2, 3]), 1)
#
#     def test_match_mixed_array_mixed_array(self):
#         assert_equal(eval([1, 2.0, 3], match, [1, 2, 3]), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, []), 1)
#         assert_equal(eval([], match, [1]), 0)
#         assert_equal(eval([1], match, []), 0)
#
# class MaxTests(TestCase):
#     def test_max_word_word(self):
#         assert_equal(eval(1, max, 2), 2)
#
#     def test_max_word_real(self):
#         assert_equal(eval(1, max, 2.0), 2.0)
#
#     def test_max_word_word_array(self):
#         assert_equal(eval(1, max, [2, 3]), [2, 3])
#
#     def test_max_word_real_array(self):
#         assert_equal(eval(1, max, [2, 3]), [2, 3])
#
#     def test_max_word_mixed_array(self):
#         assert_equal(eval(1, max, [2, 3.0]), [2, 3.0])
#
#     def test_max_real_word(self):
#         assert_equal(eval(1, max, -1), 1.0)
#
#     def test_max_real_real(self):
#         assert_equal(eval(1, max, 2.0), 2.0)
#
#     def test_max_real_word_array(self):
#         assert_equal(eval(1, max, [2, 3]), [2, 3])
#
#     def test_max_real_real_array(self):
#         assert_equal(eval(1, max, [2, 3]), [2, 3])
#
#     def test_max_real_mixed_array(self):
#         assert_equal(eval(1, max, [2, 3.0]), [2, 3])
#
#     def test_max_word_array_word(self):
#         assert_equal(eval([2, 3], max, -1), [2, 3])
#
#     def test_max_word_array_real(self):
#         assert_equal(eval([2, 3], max, 1.0), [2, 3])
#
#     def test_max_word_array_word_array(self):
#         assert_equal(eval([2, 3], max, [2, 3]), [3, 3])
#
#     def test_max_word_array_real_array(self):
#         assert_equal(eval([2, 3], max, [2, 3]), [3, 3])
#
#     def test_max_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], max, [2, 3.0]), [3, 3])
#
#     def test_max_real_array_word(self):
#         assert_equal(eval([2, 3], max, -1), [2, 3])
#
#     def test_max_real_array_real(self):
#         assert_equal(eval([2, 3], max, 1.0), [2, 3])
#
#     def test_max_real_array_word_array(self):
#         assert_equal(eval([2, 3], max, [2, 3]), [3, 3])
#
#     def test_max_real_array_real_array(self):
#         assert_equal(eval([2, 3], max, [2, 3]), [3, 3])
#
#     def test_max_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], max, [2, 3.0]), [3, 3])
#
#     def test_max_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], max, 3), [3, 3.0])
#
#     def test_max_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], max, 1.0), [2, 3.0])
#
#     def test_max_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], max, [2, 3]), [3, 3.0])
#
#     def test_max_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], max, [2, 3]), [3, 3])
#
#     def test_max_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], max, [2, 3.0]), [3, 3])
#
# class MinTests(TestCase):
#     def test_min_word_word(self):
#         assert_equal(eval(1, min, 2), 1)
#         assert_equal(eval(4, min, -1), -1)
#
#     def test_min_word_real(self):
#         assert_equal(eval(1, min, 2.0), 1.0)
#         assert_equal(eval(2, min, 1.0), 1.0)
#
#     def test_min_word_word_array(self):
#         assert_equal(eval(1, min, [2, 3]), [1, 1])
#         assert_equal(eval(4, min, [2, 3]), [2, 3])
#
#     def test_min_word_real_array(self):
#         assert_equal(eval(1, min, [2, 3]), [1, 1])
#         assert_equal(eval(4, min, [2, 3]), [2, 3])
#
#     def test_min_word_mixed_array(self):
#         assert_equal(eval(1, min, [2, 3.0]), [1, 1.0])
#         assert_equal(eval(4, min, [2, 3.0]), [2, 3.0])
#
#     def test_min_real_word(self):
#         assert_equal(eval(1, min, -1), -1.0)
#         assert_equal(eval(1, min, 4), 1.0)
#
#     def test_min_real_real(self):
#         assert_equal(eval(1, min, 2.0), 1.0)
#         assert_equal(eval(2, min, 1.0), 1.0)
#
#     def test_min_real_word_array(self):
#         assert_equal(eval(1, min, [2, 3]), [1, 1])
#         assert_equal(eval(4, min, [2, 3]), [2, 3])
#
#     def test_min_real_real_array(self):
#         assert_equal(eval(1, min, [2, 3]), [1, 1])
#         assert_equal(eval(4, min, [2, 3]), [2, 3])
#
#     def test_min_real_mixed_array(self):
#         assert_equal(eval(1, min, [2, 3.0]), [1, 1.0])
#         assert_equal(eval(4, min, [2, 3.0]), [2, 3])
#
#     def test_min_word_array_word(self):
#         assert_equal(eval([2, 3], min, -1), [-1, -1])
#         assert_equal(eval([2, 3], min, 4), [2, 3])
#
#     def test_min_word_array_real(self):
#         assert_equal(eval([2, 3], min, 1.0), [1, 1])
#         assert_equal(eval([2, 3], min, 4), [2, 3])
#
#     def test_min_word_array_word_array(self):
#         assert_equal(eval([2, 3], min, [1, 1]), [1, 1])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#
#     def test_min_word_array_real_array(self):
#         assert_equal(eval([2, 3], min, [1, 1]), [1, 1])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#
#     def test_min_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], min, [1, 1.0]), [1, 1.0])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#
#     def test_min_real_array_word(self):
#         assert_equal(eval([2.0, 3.0], min, -1), [-1.0, -1.0])
#         assert_equal(eval([2.0, 3.0], min, 4), [2.0, 3.0])
#
#     def test_min_real_array_real(self):
#         assert_equal(eval([2, 3], min, 1.0), [1, 1])
#         assert_equal(eval([2, 3], min, 4), [2, 3])
#
#     def test_min_real_array_word_array(self):
#         assert_equal(eval([2, 3], min, [1, 1]), [1, 1])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#          (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [2, 3]))
#
#     def test_min_real_array_real_array(self):
#         assert_equal(eval([2, 3], min, [1, 1]), [1, 1])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [2, 3]))
#
#     def test_min_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], min, [1, 1.0]), [1, 1.0])
#         assert_equal(eval([2, 3], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [2, 3]))
#
#     def test_min_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], min, -1), [-1, -1.0])
#         assert_equal(eval([2, 3.0], min, 4), [2, 3.0])
#
#     def test_min_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], min, 1.0), [1, 1.0])
#         assert_equal(eval([2, 3.0], min, 4), [2, 3])
#
#     def test_min_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], min, [1, 1]), [1, 1.0])
#         assert_equal(eval([2, 3.0], min, [4, 4]), [2, 3.0])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#
#     def test_min_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], min, [1, 1]), [1, 1.0])
#         assert_equal(eval([2, 3.0], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#
#     def test_min_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], min, [1, 1.0]), [1, 1.0])
#         assert_equal(eval([2, 3.0], min, [4, 4]), [2, 3])
#
#         with assert_raises(Exception):
#             (eval([2, 3], min, [4, 4, 4]))
#         with assert_raises(Exception):
#             (eval([2, 3], min, []))
#         with assert_raises(Exception):
#             (eval([], min, [4, 4, 4]))
#
# class LessTests(TestCase):
#     def test_less_word_word(self):
#         assert_equal(eval(1, less, 2), 1)
#
#     def test_less_word_real(self):
#         assert_equal(eval(1, less, 2.0), 1)
#
#     def test_less_word_word_array(self):
#         assert_equal(eval(1, less, [2, 3]), 1)
#
#     def test_less_word_real_array(self):
#         assert_equal(eval(1, less, [2, 3]), 1)
#
#     def test_less_word_mixed_array(self):
#         assert_equal(eval(1, less, [2, 3.0]), 1)
#
#     def test_less_real_word(self):
#         assert_equal(eval(1, less, -1), 0)
#
#     def test_less_real_real(self):
#         assert_equal(eval(1, less, 2.0), 1)
#
#     def test_less_real_word_array(self):
#         assert_equal(eval(1, less, [2, 3]), 1)
#
#     def test_less_real_real_array(self):
#         assert_equal(eval(1, less, [2, 3]), 1)
#     def test_less_real_mixed_array(self):
#         assert_equal(eval(1, less, [2, 3.0]), 1)
#
#     def test_less_word_array_word(self):
#         assert_equal(eval([2, 3], less, -1), [0, 0])
#
#     def test_less_word_array_real(self):
#         assert_equal(eval([2, 3], less, 1.0), [0, 0])
#
#     def test_less_word_array_word_array(self):
#         assert_equal(eval([2, 3], less, [2, 3]), [0, 0])
#
#     def test_less_word_array_real_array(self):
#         assert_equal(eval([2, 3], less, [2, 3]), [0, 0])
#
#     def test_less_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], less, [2, 3.0]), [0, 0])
#
#     def test_less_real_array_word(self):
#         assert_equal(eval([2, 3], less, -1), [0, 0])
#
#     def test_less_real_array_real(self):
#         assert_equal(eval([2, 3], less, 1.0), [0, 0])
#
#     def test_less_real_array_word_array(self):
#         assert_equal(eval([2, 3], less, [2, 3]), [0, 0])
#
#     def test_less_real_array_real_array(self):
#         assert_equal(eval([2, 3], less, [2, 3]), [0, 0])
#
#     def test_less_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], less, [2, 3.0]), [0, 0])
#
#     def test_less_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], less, 3), [1, 0])
#
#     def test_less_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], less, 1.0), [0, 0])
#
#     def test_less_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], less, [2, 3]), [0, 0])
#
#     def test_less_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], less, [2, 3]), [0, 0])
#
#     def test_less_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], less, [2, 2.0]), [0, 0])
#
# class MoreTests(TestCase):
#     def test_more_word_word(self):
#         assert_equal(eval(1, more, 2), 0)
#
#     def test_more_word_real(self):
#         assert_equal(eval(1, more, 2.0), 0)
#
#     def test_more_word_word_array(self):
#         assert_equal(eval(1, more, [2, 3]), 0)
#
#     def test_more_word_real_array(self):
#         assert_equal(eval(1, more, [2, 3]), 0)
#
#     def test_more_word_mixed_array(self):
#         assert_equal(eval(1, more, [2, 3.0]), 0)
#
#     def test_more_real_word(self):
#         assert_equal(eval(1, more, -1), 1)
#
#     def test_more_real_real(self):
#         assert_equal(eval(1, more, 2.0), 0)
#
#     def test_more_real_word_array(self):
#         assert_equal(eval(1, more, [2, 3]), 0)
#
#     def test_more_real_real_array(self):
#         assert_equal(eval(1, more, [2, 3]), 0)
#
#     def test_more_real_mixed_array(self):
#         assert_equal(eval(1, more, [2, 3.0]), 0)
#
#     def test_more_word_array_word(self):
#         assert_equal(eval([2, 3], more, -1), [1, 1])
#
#     def test_more_word_array_real(self):
#         assert_equal(eval([2, 3], more, 1.0), [1, 1])
#
#     def test_more_word_array_word_array(self):
#         assert_equal(eval([2, 3], more, [2, 3]), [0, 0])
#
#     def test_more_word_array_real_array(self):
#         assert_equal(eval([2, 3], more, [2, 3]), [0, 0])
#
#     def test_more_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], more, [2, 3.0]), [0, 0])
#
#     def test_more_real_array_word(self):
#         assert_equal(eval([2, 3], more, -1), [1, 1])
#
#     def test_more_real_array_real(self):
#         assert_equal(eval([2, 3], more, 1.0), [1, 1])
#
#     def test_more_real_array_word_array(self):
#         assert_equal(eval([2, 3], more, [2, 3]), [0, 0])
#
#     def test_more_real_array_real_array(self):
#         assert_equal(eval([2, 3], more, [2, 3]), [0, 0])
#
#     def test_more_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], more, [2, 3.0]), [0, 0])
#
#     def test_more_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], more, 3), [0, 0])
#
#     def test_more_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], more, 1.0), [1, 1])
#
#     def test_more_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], more, [2, 3]), [0, 0])
#
#     def test_more_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], more, [2, 3]), [0, 0])
#
#     def test_more_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], more, [2, 2.0]), [0, 1])
#
# class EqualTests(TestCase):
#     def test_equal_word_word(self):
#         assert_equal(eval(1, equal, 2), 0)
#
#     def test_equal_word_real(self):
#         assert_equal(eval(1, equal, 2.0), 0)
#
#     def test_equal_word_word_array(self):
#         assert_equal(eval(1, equal, [2, 3]), 0)
#
#     def test_equal_word_real_array(self):
#         assert_equal(eval(1, equal, [2, 3]), 0)
#
#     def test_equal_word_mixed_array(self):
#         assert_equal(eval(1, equal, [2, 3.0]), 0)
#
#     def test_equal_real_word(self):
#         assert_equal(eval(1, equal, -1), 0)
#
#     def test_equal_real_real(self):
#         assert_equal(eval(1, equal, 2.0), 0)
#
#     def test_equal_real_word_array(self):
#         assert_equal(eval(1, equal, [2, 3]), 0)
#
#     def test_equal_real_real_array(self):
#         assert_equal(eval(1, equal, [2, 3]), 0)
#     def test_equal_real_mixed_array(self):
#         assert_equal(eval(1, equal, [2, 3.0]), 0)
#
#     def test_equal_word_array_word(self):
#         assert_equal(eval([2, 3], equal, -1), [0, 0])
#
#     def test_equal_word_array_real(self):
#         assert_equal(eval([2, 3], equal, 1.0), [0, 0])
#
#     def test_equal_word_array_word_array(self):
#         assert_equal(eval([2, 3], equal, [2, 3]), [1, 1])
#
#     def test_equal_word_array_real_array(self):
#         assert_equal(eval([2, 3], equal, [2, 3]), [1, 1])
#
#     def test_equal_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], equal, [2, 3.0]), [1, 1])
#
#     def test_equal_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], equal, 3), [0, 1])
#
#     def test_equal_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], equal, 1.0), [0, 0])
#
#     def test_equal_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], equal, [2, 3]), [0, 0])
#
#     def test_equal_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], equal, [2, 3]), [0, 0])
#
#     def test_equal_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], equal, [2, 2.0]), [1, 0])
#
# class IndexTests(TestCase):
#     def test_index_word_word_array(self):
#         assert_equal(eval(1, index, [2, 3]), 2)
#
#     def test_index_word_real_array(self):
#         assert_equal(eval(1, index, [2, 3]), 2.0)
#
#     def test_index_word_mixed_array(self):
#         assert_equal(eval(1, index, [2, 3.0]), 2)
#
#     def test_index_real_word_array(self):
#         assert_equal(eval(0.5, index, [2, 3]), 2)
#
#     def test_index_real_real_array(self):
#         assert_equal(eval(0.5, index, [2, 3]), 2.0)
#
#     def test_index_real_mixed_array(self):
#         assert_equal(eval(0.5, index, [2, 3.0]), 2)
#
#     def test_index_word_array_word(self):
#         with assert_raises(Exception):
#             eval([2, 3], index, -1)
#
#     def test_index_word_array_real(self):
#         assert_equal(eval([2, 3], index, 0.5), 2)
#
#     def test_index_word_array_word_array(self):
#         assert_equal(eval([2, 3], index, [1, 2]), [2, 3])
#
#     def test_index_word_array_real_array(self):
#         assert_equal(eval([2, 3], index, [0.5, 1.0]), [2, 3])
#
#     def test_index_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], index, [1, 1.0]), [2, 3])
#
#     def test_index_real_array_word(self):
#         with assert_raises(Exception):
#             eval([2, 3], index, -1)
#
#     def test_index_real_array_real(self):
#         assert_equal(eval([2, 3], index, 0.5), 2.0)
#
#     def test_index_real_array_word_array(self):
#         assert_equal(eval([2, 3], index, [1, 2]), [2, 3])
#
#     def test_index_real_array_real_array(self):
#         assert_equal(eval([2, 3], index, [0.5, 1.0]), [2, 3])
#
#     def test_index_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], index, [1, 1.0]), [2, 3])
#
#     def test_index_mixed_array_word(self):
#         with assert_raises(Exception):
#             eval([2, 3.0], index, -1)
#
#     def test_index_mixed_array_real(self):
#         assert_equal(eval([2, 3.0], index, 0.5), 2)
#
#     def test_index_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], index, [1, 2]), [2, 3.0])
#
#     def test_index_mixed_array_real_array(self):
#         assert_equal(eval([2, 3.0], index, [0.5, 1.0]), [2, 3.0])
#
#     def test_index_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], index, [1, 1.0]), [2, 3.0])
#
# class CutTests(TestCase):
#     def test_cut_word_word_array(self):
#         assert_equal(eval(1, cut, [2, 3]), [3])
#
#     def test_cut_word_real_array(self):
#         assert_equal(eval(1, cut, [2, 3]), [3])
#
#     def test_cut_word_mixed_array(self):
#         assert_equal(eval(1, cut, [2, 3.0]), [3.0])
#
#     def test_cut_word_array_word(self):
#         with assert_raises(Exception):
#             eval([2, 3], cut, -1)
#
#     def test_cut_word_array_word_array(self):
#         assert_equal(eval([2, 3], cut, [1, 2]), [[], [2], [3]])
#         assert_equal(eval([2, 3], cut, []), [[2, 3]])
#         with assert_raises(Exception):
#             eval([], cut, [1, 2])
#
#     def test_cut_word_array_real_array(self):
#         assert_equal(eval([2, 3], cut, [0.5, 1.0]), [[2], [3], []])
#         assert_equal(eval([2, 3], cut, []), [[2, 3]])
#
#     def test_cut_word_array_mixed_array(self):
#         assert_equal(eval([2, 3], cut, [1, 2]), [[], [2], [3]])
#         assert_equal(eval([2, 3], cut, []), [[2, 3]])
#
#     def test_cut_real_array_word(self):
#         assert_equal(eval([2.0, 3.0], cut, 1), [[], [2.0, 3.0]])
#
#     def test_cut_real_array_word_array(self):
#         assert_equal(eval([2, 3], cut, [1, 2]), [[], [2], [3]])
#         assert_equal(eval([2, 3], cut, []), [[2, 3]])
#
#     def test_cut_real_array_mixed_array(self):
#         assert_equal(eval([2, 3], cut, [1, 2]), [[], [2], [3]])
#
#     def test_cut_mixed_array_word(self):
#         assert_equal(eval([2, 3.0], cut, 1), [[], [2, 3.0]])
#
#     def test_cut_mixed_array_word_array(self):
#         assert_equal(eval([2, 3.0], cut, [1, 2]), [[], [2], [3.0]])
#         assert_equal(eval([2, 3.0], cut, []), [[2, 3.0]])
#
#     def test_cut_mixed_array_mixed_array(self):
#         assert_equal(eval([2, 3.0], cut, [1, 2]), [[], [2], [3.0]])
#
#     def test_cut_errors(self):
#         with assert_raises(Exception):
#             (eval([1, 2, 3], cut, 1.0))
#
# class GradeUpTests(TestCase):
#     def test_gradeUp_word_array(self):
#         assert_equal(eval([0, 1, 0, 2], gradeUp), [1, 3, 2, 4])
#
#     def test_gradeUp_real_array(self):
#         assert_equal(eval([0, 1, 0, 2], gradeUp), [1, 3, 2, 4])
#
#     def test_gradeUp_mixed_array(self):
#         assert_equal(eval([0, 1.0, 0, 2.0], gradeUp), [1, 3, 2, 4])
#
# class GradeDownTests(TestCase):
#     def test_gradeDown_word_array(self):
#         assert_equal(eval([0, 1, 0, 2], gradeDown), [4, 2, 3, 1])
#
#     def test_gradeDown_real_array(self):
#         assert_equal(eval([0, 1, 0, 2], gradeDown), [4, 2, 3, 1])
#
#     def test_gradeDown_mixed_array(self):
#         assert_equal(eval([0, 1.0, 0, 2.0], gradeDown), [4, 2, 3, 1])
#
# class TransposeTests(TestCase):
#     def test_transpose_mixed_array(self):
#         assert_equal(eval([[1, 2], [3, 4]], transpose), [[1, 3], [2, 4]])
#
# class AdverbTests(TestCase):
#     def test_each(self):
#         assert_equal(eval(1, each, negate), -1)
#         assert_equal(eval(1, each, negate), -1.0)
#         assert_equal(eval([1, 2, 3], each, negate), [-1, -2, -3])
#         assert_equal(eval([1, 2, 3], each, negate), [-1.0, -2.0, -3.0])
#         assert_equal(eval([1, 2, 3], each, negate), [-1, -2, -3])
#
#     def test_each2(self):
#         assert_equal(eval(1, each2, plus, 1), 2)
#         assert_equal(eval(1, each2, plus, 1.0), 2.0)
#         assert_equal(eval([1, 2, 3], each2, plus, 4), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], each2, plus, 4.0), [5.0, 6.0, 7.0])
#         assert_equal(eval([1, 2, 3], each2, plus, [4, 5, 6]), [5, 7, 9])
#         assert_equal(eval([1, 2, 3], each2, plus, [4, 5.0, 6]), [5, 7.0, 9])
#
#         assert_equal(eval([1.0, 2.0, 3.0], each2, plus, 4), [5, 6, 7])
#         assert_equal(eval([1.0, 2.0, 3.0], each2, plus, 4.0), [5.0, 6.0, 7.0])
#         assert_equal(eval([1, 2.0, 3], each2, plus, [4, 5, 6]), [5, 7.0, 9])
#         assert_equal(eval([1, 2.0, 3], each2, plus, [4, 5, 6]), [5, 7.0, 9])
#
#     def test_eachLeft(self):
#         assert_equal(eval(1, eachLeft, plus, 4), 5)
#         assert_equal(eval(1, eachLeft, plus, 1.0), 2.0)
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5, 6, 7])
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5, 6, 7])
#
#         assert_equal(eval(1, eachLeft, plus, 4), 5.0)
#         assert_equal(eval(1, eachLeft, plus, 4.0), 5.0)
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachLeft, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#
#         assert_equal(eval([1, 2, 3], eachLeft, plus, 4), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], eachLeft, plus, 4.0), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], eachLeft, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
#
#         assert_equal(eval([1, 2.0, 3], eachLeft, plus, 4), [5, 6.0, 7])
#         assert_equal(eval([1, 2.0, 3], eachLeft, plus, 4), [5.0, 6.0, 7.0])
#         assert_equal(eval([1, 2.0, 3], eachLeft, plus, [4, 5, 6]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])
#
#     def test_eachRight(self):
#         assert_equal(eval(1, eachRight, plus, 4), 5)
#         assert_equal(eval(1, eachRight, plus, 4.0), 5.0)
#         assert_equal(eval(1, eachRight, plus, [4, 5, 6]), [5, 6, 7])
#         assert_equal(eval(1, eachRight, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachRight, plus, [4, 5.0, 6]), [5, 6.0, 7])
#
#         assert_equal(eval(1, eachRight, plus, 4), 5.0)
#         assert_equal(eval(1, eachRight, plus, 4.0), 5.0)
#         assert_equal(eval(1, eachRight, plus, [4, 5, 6]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachRight, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, eachRight, plus, [4, 5.0, 6]), [5.0, 6.0, 7.0])
#
#         assert_equal(eval([1, 2, 3], eachRight, plus, 4), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], eachRight, plus, 4.0), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5.0, 6]), [[5, 6, 7], [6.0, 7.0, 8.0], [7, 8, 9]])
#
#         assert_equal(eval([1, 2, 3], eachRight, plus, 4), [5, 6, 7])
#         assert_equal(eval([1, 2, 3], eachRight, plus, 4), [5.0, 6.0, 7.0])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5, 6]), [[5, 6, 7], [6, 7, 8], [7, 8, 9]])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
#         assert_equal(eval([1, 2, 3], eachRight, plus, [4, 5.0, 6]), [[5, 6, 7], [6.0, 7.0, 8.0], [7, 8, 9]])
#
#         assert_equal(eval([1, 2.0, 3], eachRight, plus, 4), [5, 6.0, 7])
#         assert_equal(eval([1, 2.0, 3], eachRight, plus, 4.0), [5.0, 6.0, 7.0])
#         assert_equal(eval([1, 2.0, 3], eachRight, plus, [4, 5, 6]), [[5, 6.0, 7], [6, 7.0, 8], [7, 8.0, 9]])
#         assert_equal(eval([1, 2.0, 3], eachRight, plus, [4.0, 5.0, 6.0]), [[5.0, 6.0, 7.0], [6.0, 7.0, 8.0], [7.0, 8.0, 9.0]])
#         assert_equal(eval([1, 2.0, 3], eachRight, plus, [4, 5.0, 6]), [[5, 6.0, 7], [6.0, 7.0, 8.0], [7, 8.0, 9]])
#
#     def test_eachPair(self):
#         assert_equal(eval([4, 5, 6], eachPair, plus), [9, 11])
#         assert_equal(eval([4.0, 5.0, 6.0], eachPair, plus), [9.0, 11.0])
#         assert_equal(eval([4, 5.0, 6], eachPair, plus), [9.0, 11.0])
#
#     def test_over(self):
#         assert_equal(eval(4, over, plus), 4)
#         assert_equal(eval(4, over, plus), 4.0)
#
#         assert_equal(eval([], over, plus), [])
#         assert_equal(eval([4], over, plus), [4])
#         assert_equal(eval([4, 5, 6], over, plus), 15)
#
#         assert_equal(eval([], over, plus), [])
#         assert_equal(eval([4], over, plus), [4])
#         assert_equal(eval([4, 5, 6], over, plus), 15.0)
#
#         assert_equal(eval([], over, plus), [])
#         assert_equal(eval([4], over, plus), [4])
#         assert_equal(eval([4, 5, 6], over, plus), 15)
#
#     def test_overNeutral(self):
#         assert_equal(eval(1, overNeutral, plus, 1), 2)
#         assert_equal(eval(1, overNeutral, plus, 1.0), 2.0)
#         assert_equal(eval(1, overNeutral, plus, [4, 5, 6]), [5, 6, 7])
#         assert_equal(eval(1, overNeutral, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, overNeutral, plus, [4, 5.0, 6]), [5, 6.0, 7])
#
#         assert_equal(eval(1, overNeutral, plus, 1), 2.0)
#         assert_equal(eval(1, overNeutral, plus, 1.0), 2.0)
#         assert_equal(eval(1, overNeutral, plus, [4, 5, 6]), [5, 6, 7])
#         assert_equal(eval(1, overNeutral, plus, [4.0, 5.0, 6.0]), [5.0, 6.0, 7.0])
#         assert_equal(eval(1, overNeutral, plus, [4, 5.0, 6]), [5.0, 6.0, 7.0])
#
#         assert_equal(eval([1, 2], overNeutral, plus, 1), 4)
#         assert_equal(eval([1, 2], overNeutral, plus, 1.0), 4.0)
#         assert_equal(eval([1, 2], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
#         assert_equal(eval([1, 2], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
#         assert_equal(eval([1, 2], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])
#         with assert_raises(Exception):
#             (eval([], overNeutral, plus, 1))
#
#         assert_equal(eval([1, 2], overNeutral, plus, 1), 4.0)
#         assert_equal(eval([1, 2], overNeutral, plus, 1.0), 4.0)
#         assert_equal(eval([1, 2], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
#         assert_equal(eval([1, 2], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
#         assert_equal(eval([1, 2], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])
#         with assert_raises(Exception):
#             (eval([], overNeutral, plus, 1))
#
#         assert_equal(eval([1, 2.0], overNeutral, plus, 1), 4.0)
#         assert_equal(eval([1, 2.0], overNeutral, plus, 4.0), 7.0)
#         assert_equal(eval([1, 2.0], overNeutral, plus, [4, 5, 6]), [7, 8, 9])
#         assert_equal(eval([1, 2.0], overNeutral, plus, [4.0, 5.0, 6.0]), [7.0, 8.0, 9.0])
#         assert_equal(eval([1, 2.0], overNeutral, plus, [4, 5.0, 6]), [7, 8.0, 9])
#         with assert_raises(Exception):
#             (eval([], overNeutral, plus, 1))
#
#     def test_converge(self):
#         assert_equal(eval([1, 2, 3], converge, shape), [1])
#
#     def test_whileOne(self):
#         assert_equal(eval(0, whileOne, atom, enclose), [0])
#
#     def test_iterate(self):
#         assert_equal(eval([1, 2, 3], iterate, shape, 2), [1])
#         assert_equal(eval([1, 2, 3], iterate, shape, 2), [1])
#         assert_equal(eval([1, 2.0, 3], iterate, shape, 2), [1])
#
#         with assert_raises(Exception):
#             (eval(2, iterate, shape, [1, 2, 3]))
#         with assert_raises(Exception):
#             (eval(-2, iterate, shape, [1, 2, 3]))
#         with assert_raises(Exception):
#             (eval(2, iterate, shape, [1, 2, 3]))
#
#     def test_scanOver(self):
#         assert_equal(eval(1, scanOver, shape), [1])
#
#         assert_equal(eval([1, 2, 3], scanOver, plus), [1, 3, 6])
#         assert_equal(eval([], scanOver, plus), [])
#
#         assert_equal(eval([1, 2, 3], scanOver, plus), [1.0, 3.0, 6.0])
#         assert_equal(eval([], scanOver, plus), [])
#
#         assert_equal(eval([1, 2.0, 3], scanOver, plus), [1, 3.0, 6.0])
#         assert_equal(eval([], scanOver, plus), [])
#
#     def test_scanOverNeutral(self):
#         assert_equal(eval(1, scanOverNeutral, plus, 1), [1, 2])
#         assert_equal(eval([1, 2, 3], scanOverNeutral, plus, 1), [1, 2, 4, 7])
#         assert_equal(eval([1, 2, 3], scanOverNeutral, plus, 1), [1, 2.0, 4.0, 7.0])
#         assert_equal(eval([1, 2.0, 3], scanOverNeutral, plus, 1), [1, 2, 4.0, 7.0])
#
#     def test_scanConverging(self):
#         assert_equal(eval([1, 2, 3], scanConverging, shape), [[1, 2, 3], [3], [1]])
#         assert_equal(eval([1, 2, 3], scanConverging, shape), [[1, 2, 3], [3], [1]])
#         assert_equal(eval([1, 2.0, 3], scanConverging, shape),[[1, 2.0, 3], [3], [1]])
#
#     def test_scanWhileOne(self):
#         assert_equal(eval(0, scanWhileOne, atom, enclose), [0])
#
#     def test_scanIterating(self):
#         assert_equal(eval([1, 2, 3], scanIterating, shape, 2), [[1, 2, 3], [3], [1]])
#         with assert_raises(Exception):
#             (eval([1, 2, 3], scanIterating, shape, -2))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], scanIterating, shape, 1.0))
#
#         assert_equal(eval([1, 2, 3], scanIterating, shape, 2), [[1, 2, 3], [3], [1]])
#         with assert_raises(Exception):
#             (eval([1, 2, 3], scanIterating, shape, -2))
#         with assert_raises(Exception):
#             (eval([1, 2, 3], scanIterating, shape, 1.0))
#
#         assert_equal(eval([1, 2.0, 3], scanIterating, shape, 2), [[1, 2.0, 3], [3], [1]])
#         with assert_raises(Exception):
#             (eval([1, 2.0, 3], scanIterating, shape, -2))
#         with assert_raises(Exception):
#             (eval([1, 2.0, 3], scanIterating, shape, 1.0))
#
#     def test_apply(self):
#         assert_equal(eval(1, applyMonad, negate), -1)
#         assert_equal(eval(1, applyDyad, plus, 1), 2)
#         assert_equal(eval(1, applyMonad, F(i, negate)), -1)
#         assert_equal(eval(1, applyMonad, F(i, plus, 1)), 2)
#         assert_equal(eval((1, plus, 1), applyMonad, negate), -2)
#         assert_equal(eval((1, plus, 1), applyMonad, (i, plus, 1)), 3)

if __name__ == "__main__":
    # Run tests when executed
    from testify import run

    run()
