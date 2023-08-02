import unittest

import lark

from mltl2ltlf import mltl2ltlf


class TestEventually(unittest.TestCase):
    def test_eventually_48(self):
        formula = "F_[4,8] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!](X[!](a|(X[!](a|(X[!](a|(X[!](a|(X[!]a))))))))))))"
        self.assertEqual(expected, actual)

    def test_eventually_03(self):
        formula = "F_[0,3] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a|(X[!](a|(X[!](a|(X[!]a))))))"
        self.assertEqual(expected, actual)

    def test_eventually_3(self):
        formula = "F_<=3 a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a|(X[!](a|(X[!](a|(X[!]a))))))"
        self.assertEqual(expected, actual)

    def test_eventually_2(self):
        formula = "F_<3 a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a|(X[!](a|(X[!]a))))"
        self.assertEqual(expected, actual)

    def test_eventually_33(self):
        formula = "F_[3,3] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!]a)))"
        self.assertEqual(expected, actual)

    def test_eventually_00(self):
        formula = "F_[0,0] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a)"
        self.assertEqual(expected, actual)

    def test_eventually_12(self):
        formula = "F_[1,2] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](a|(X[!]a)))"
        self.assertEqual(expected, actual)

    def test_eventually_no_interval(self):
        formula = "F a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        self.assertEqual(formula, actual)

    def test_eventually_invalid_bound(self):
        formula = "F_[2,1] a"
        with self.assertRaises(AssertionError) and self.assertRaises(lark.exceptions.VisitError):
            mltl2ltlf.mltl2ltlf(formula)

    def test_eventually_negative_bound(self):
        formula = "F_[-1,-2] a"
        with self.assertRaises(lark.exceptions.UnexpectedCharacters):
            mltl2ltlf.mltl2ltlf(formula)


class TestAlways(unittest.TestCase):
    def test_always_48(self):
        formula = "G_[4,8] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!](X[!](a&(X[!](a&(X[!](a&(X[!](a&(X[!]a))))))))))))"
        self.assertEqual(expected, actual)

    def test_always_03(self):
        formula = "G_[0,3] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a&(X[!](a&(X[!](a&(X[!]a))))))"
        self.assertEqual(expected, actual)

    def test_always_3(self):
        formula = "G_<=3 a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a&(X[!](a&(X[!](a&(X[!]a))))))"
        self.assertEqual(expected, actual)

    def test_always_2(self):
        formula = "G_<3 a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a&(X[!](a&(X[!]a))))"
        self.assertEqual(expected, actual)

    def test_always_33(self):
        formula = "G_[3,3] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!]a)))"
        self.assertEqual(expected, actual)

    def test_always_00(self):
        formula = "G_[0,0] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(a)"
        self.assertEqual(expected, actual)

    def test_always_12(self):
        formula = "G_[1,2] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](a&(X[!]a)))"
        self.assertEqual(expected, actual)

    def test_always_no_interval(self):
        formula = "G a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        self.assertEqual(formula, actual)

    def test_always_invalid_bound(self):
        formula = "G_[2,1] a"
        with self.assertRaises(AssertionError) and self.assertRaises(lark.exceptions.VisitError):
            mltl2ltlf.mltl2ltlf(formula)

    def test_always_negative_bound(self):
        formula = "G_[-1,-2] a"
        with self.assertRaises(lark.exceptions.UnexpectedCharacters):
            mltl2ltlf.mltl2ltlf(formula)


class TestUntil(unittest.TestCase):
    def test_until_48(self):
        formula = "a U_[4,8] b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!](X[!](b|(a&(X[!](b|(a&(X[!](b|(a&(X[!](b|(a&(X[!]b))))))))))))))))"
        self.assertEqual(expected, actual)

    def test_until_03(self):
        formula = "a U_[0,3] b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(b|(a&(X[!](b|(a&(X[!](b|(a&(X[!]b)))))))))"
        self.assertEqual(expected, actual)

    def test_until_3(self):
        formula = "a U_<=3 b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(b|(a&(X[!](b|(a&(X[!](b|(a&(X[!]b)))))))))"
        self.assertEqual(expected, actual)

    def test_until_2(self):
        formula = "a U_<3 b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(b|(a&(X[!](b|(a&(X[!]b))))))"
        self.assertEqual(expected, actual)

    def test_until_33(self):
        formula = "a U_[3,3] b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](X[!](X[!]b)))"
        self.assertEqual(expected, actual)

    def test_until_00(self):
        formula = "a U_[0,0] b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(b)"
        self.assertEqual(expected, actual)

    def test_until_12(self):
        formula = "a U_[1,2] b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](b|(a&(X[!]b))))"
        self.assertEqual(expected, actual)

    def test_until_no_interval(self):
        formula = "a U b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        self.assertEqual(formula, actual)

    def test_until_invalid_bound(self):
        formula = "a U_[2,1] b"
        with self.assertRaises(AssertionError) and self.assertRaises(lark.exceptions.VisitError):
            mltl2ltlf.mltl2ltlf(formula)

    def test_until_negative_bound(self):
        formula = "a U_[-1,-2] b"
        with self.assertRaises(lark.exceptions.UnexpectedCharacters):
            mltl2ltlf.mltl2ltlf(formula)


class TestMixingOperators(unittest.TestCase):

    def test_nested_operator(self):
        formula = "F G_[1,2] (a U (F b))"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "F(X[!]((a U(F b))&(X[!](a U(F b)))))"
        self.assertEqual(expected, actual)

    def test_simple_mixing_1(self):
        formula = "F G_[0,3] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "F(a&(X[!](a&(X[!](a&(X[!]a))))))"
        self.assertEqual(expected, actual)

    def test_simple_mixing_2(self):
        formula = "F_[0,1] G_[1,2] a"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "(X[!](a&(X[!]a)))|(X[!](X[!](a&(X[!]a))))"
        self.assertEqual(expected, actual)

    def test_complex_mixing(self):
        formula = "(F_[0,1] G_[1,2] a) U b"
        actual = mltl2ltlf.mltl2ltlf(formula)
        expected = "((X[!](a&(X[!]a)))|(X[!](X[!](a&(X[!]a)))))U b"
        self.assertEqual(expected, actual)
