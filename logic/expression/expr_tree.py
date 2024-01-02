from sympy import Implies, Not, Symbol, postorder_traversal
from sympy.logic.boolalg import BooleanFalse, BooleanFunction, BooleanTrue

from .parse import parse_expr


def k_degree(ex: BooleanFunction) -> int:
    args = [ag for ag in postorder_traversal(ex) if
            ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue]

    not_and_implies_count = ex.atoms(Not, Implies).__len__()

    args_count = args.__len__()

    removed_constant_list = [ag for ag in args if ag.func is Symbol]
    args_set_count = set(removed_constant_list).__len__()
    return args_count - args_set_count + not_and_implies_count


def height_of_expr(_ex: BooleanFunction) -> int:
    sub_ex = [ag for ag in _ex.args if
              ag.func is not Symbol and ag.func is not BooleanFalse and ag.func is not BooleanTrue]
    if sub_ex.__len__() == 0:
        return 1
    else:
        return max([height_of_expr(_ex) for _ex in sub_ex]) + 1


def length_of_expr(_ex) -> int:
    count = 0
    for ag in postorder_traversal(_ex):
        if ag.func is Symbol or ag.func is BooleanFalse or ag.func is BooleanTrue or ag.func is Not or ag.func is Implies:
            count += 1

    return count


def simple_degree(ex: BooleanFunction) -> int:
    implies_count = ex.atoms(Implies)
    constant_count = ex.atoms(BooleanTrue, BooleanFalse)
    return length_of_expr(ex) + height_of_expr(ex) + implies_count + constant_count


def simpler(ex_1: BooleanFunction, ex_2: BooleanFunction) -> bool:
    constant_count_1 = ex_1.atoms(BooleanTrue, BooleanFalse).__len__()
    constant_count_2 = ex_2.atoms(BooleanTrue, BooleanFalse).__len__()

    if length_of_expr(ex_1) > length_of_expr(ex_2):
        return False
    elif length_of_expr(ex_1) == length_of_expr(ex_2) and constant_count_1 > constant_count_2:
        return False
    elif height_of_expr(ex_1) > height_of_expr(ex_2):
        return False

    return True


def simpler_equal(ex_1: BooleanFunction, ex_2: BooleanFunction) -> bool:
    constant_count_1 = ex_1.atoms(BooleanTrue, BooleanFalse).__len__()
    constant_count_2 = ex_2.atoms(BooleanTrue, BooleanFalse).__len__()

    if length_of_expr(ex_1) != length_of_expr(ex_2):
        return False
    elif constant_count_1 != constant_count_2:
        return False
    elif height_of_expr(ex_1) != height_of_expr(ex_2):
        return False

    return True


def convert_to_not(_expr: BooleanFunction) -> BooleanFunction:
    if _expr.func is Not:
        return _expr.args[0]
    else:
        return Not(_expr)


def remove_double_not(_expr: BooleanFunction) -> BooleanFunction:
    if _expr.func is Not and _expr.args[0].func is Not:
        return _expr.args[0].args[0]
    else:
        return _expr


def revert_not(_expr: BooleanFunction) -> BooleanFunction:
    if _expr.func is Not:
        return _expr.args[0]
    else:
        return Not(_expr)


if __name__ == '__main__':
    _ex1 = parse_expr('(p & ~q) | (q & ~p)')
    _ex2 = parse_expr('(p | q) & (~p | ~q)')
    print(simpler_equal(_ex2, _ex1))
