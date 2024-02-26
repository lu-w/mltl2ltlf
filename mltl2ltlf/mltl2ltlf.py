#!/bin/python

import sys
from typing import Callable

import lark
import os

_MTL_LARK_FILE = os.path.join(os.path.dirname((os.path.realpath(__file__))), "mltl.lark")
with open(_MTL_LARK_FILE, "r") as f:
    _MTL_PARSER = lark.Lark(f.read(), maybe_placeholders=False)


class IntervalTransformer(lark.Transformer):
    def _get_interval_bounds(self, interval: lark.Tree):
        a, b = -1, -1
        interval_type = interval.children[0].data
        time_points = list(interval.find_data("time_point"))
        if interval_type == "full_interval":
            a = int(time_points[0].children[0])
            b = int(time_points[1].children[0])
        elif interval_type == "upper_including_bound_interval":
            a = 0
            b = int(time_points[0].children[0])
        elif interval_type == "upper_excluding_bound_interval":
            a = 0
            b = int(time_points[0].children[0]) - 1
        assert 0 <= a <= b
        return a, b

    def _bracket_formula(self, formula: lark.Tree):
        lp = lark.Token("LEFT_PAREN", "(")
        rp = lark.Token("RIGHT_PAREN", ")")
        return lark.Tree(data=lark.Token("RULE", "ltl_formula"), children=[lp, formula, rp])

    def _disjunction(self, a, b, c=None, bracket=True):
        b_disjunction_term = lark.Token("OR1_TERMINAL", "|")
        b_disjunction_ = lark.Tree(data=lark.Token("RULE", "or"), children=[b_disjunction_term])
        formula = lark.Tree(data=lark.Token("RULE", "disjunction_formula"), children=[a, b_disjunction_, b])
        if bracket:
            return self._bracket_formula(formula)
        else:
            return formula

    def _conjunction(self, a, b, c=None, bracket=True):
        b_conjunction_term = lark.Token("AND1_TERMINAL", "&")
        b_conjunction_ = lark.Tree(data=lark.Token("RULE", "and"), children=[b_conjunction_term])
        formula = lark.Tree(data=lark.Token("RULE", "conjunction_formula"), children=[a, b_conjunction_, b])
        if bracket:
            return self._bracket_formula(formula)
        else:
            return formula

    def _until_subformula(self, a, inner, b, bracket=True):
        con = self._conjunction(a, inner, bracket=True)
        return self._disjunction(b, con, bracket=bracket)

    def _weak_next(self, a=None, bracket=True):
        b_next_term = lark.Token("X_TERMINAL", "X")
        b_next_ = lark.Tree(data=lark.Token("RULE", "weak_next"), children=[b_next_term])
        if a is not None:
            c = [b_next_, a]
        else:
            c = [b_next_]
        tree = lark.Tree(data=lark.Token("RULE", "weak_next_formula"), children=c)
        if bracket:
            return self._bracket_formula(tree)
        else:
            return tree

    def _strong_next(self, a=None, bracket=True):
        b_next_term = lark.Token("XB_TERMINAL", "X[!]")
        b_next_ = lark.Tree(data=lark.Token("RULE", "next"), children=[b_next_term])
        if a is not None:
            c = [b_next_, a]
        else:
            c = [b_next_]
        tree = lark.Tree(data=lark.Token("RULE", "next_formula"), children=c)
        if bracket:
            return self._bracket_formula(tree)
        else:
            return tree

    def _construct_interval(self, s, operator_name: str, operator_fun: Callable):
        next_constructor = self._strong_next
        if operator_name in {"eventually_formula", "always_formula"}:
            operator = s[0]
            phi1 = inner = s[1]
            phi2 = None
            if operator_name == "always_formula":
                next_constructor = self._weak_next
        elif operator_name == "until_formula":
            operator = s[1]
            phi1 = s[0]
            phi2 = inner = s[2]
        else:
            raise ValueError("Unsupported LTL operator: " + str(operator_name))
        interval = list(operator.find_data("interval"))
        if len(interval) > 0:
            a, b = self._get_interval_bounds(interval[0])

            if b > a:
                b_next_f = next_constructor(inner)
                for i in range(b - a - 1):
                    b_operator_f = operator_fun(phi1, b_next_f, phi2)
                    b_next_f = next_constructor(b_operator_f)
                inner_part_f = operator_fun(phi1, b_next_f, phi2, bracket=(a > 0))
            else:
                inner_part_f = inner

            if a > 0:
                a_inner_next_f = next_constructor(bracket=a > 1)
                a_prev_next_f = a_inner_next_f
                for i in range(a - 1):
                    a_next_f = next_constructor(a_prev_next_f, bracket=(i < a - 2))
                    a_prev_next_f = a_next_f
                if a > 1:
                    a_inner_next_f.children[1].children.append(inner_part_f)
                else:
                    a_inner_next_f.children.append(inner_part_f)
                res = a_prev_next_f
            else:
                res = inner_part_f
            if (len(res.children) > 0 and (not hasattr(res.children[0], "data") or
                                           (res.children[0].data == "ltl_formula" and len(res.children[0].children) > 0
                                            and res.children[0].children[0] == lark.Token("LEFT_PAREN", "(")))):
                return res
            else:
                return self._bracket_formula(res)

        else:
            return lark.Tree(data=lark.Token("RULE", operator_name), children=s)

    def eventually_formula(self, s):
        return self._construct_interval(s, operator_name="eventually_formula", operator_fun=self._disjunction)

    def always_formula(self, s):
        return self._construct_interval(s, operator_name="always_formula", operator_fun=self._conjunction)

    def until_formula(self, s):
        return self._construct_interval(s, operator_name="until_formula", operator_fun=self._until_subformula)


def to_string(ltlf_formula: lark.Tree):
    res_string = ""
    formulas = [ltlf_formula]
    while len(formulas) > 0:
        cur_formula = formulas[0]
        formulas = formulas[1:]
        if isinstance(cur_formula, lark.Tree) and len(cur_formula.children) > 0:
            formulas = cur_formula.children + formulas
        elif isinstance(cur_formula, lark.Token):
            res_string += cur_formula.value
    return res_string


def mltl2ltlf(ltl_in: str):
    mltl_formula = _MTL_PARSER.parse(ltl_in)
    ltlf_formula = IntervalTransformer().transform(mltl_formula)
    ltlf_string = to_string(ltlf_formula)
    return ltlf_string


def main():
    if len(sys.argv) > 1:
        print(mltl2ltlf(sys.argv[1]))
        exit(0)
    elif len(sys.argv) > 0:
        print("Usage: call " + os.path.basename(sys.argv[0]) + " with the MLTL formula as its only input string.")
        exit(1)
    else:
        exit(1)


if __name__ == "__main__":
    main()
