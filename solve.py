# an Operation is a tuple:
#    (Exp, operator, Exp)

# an Exp is one of:
#   Fraction
#   Number
#   Term
#   Rational Expression

# a Fraction is a tuple
# a Term is a tuple
# a Rational Expression is a tuple

# Operation -> Exp
# `solve` evaluates an operation potentially consisting of various data.
#  data can be in the form of fractions, numbers, rational expressions, and monomials
def solve(operation):
    (l, op, r) = operation
    if isfraction(l) and isfraction(r):
        return solve_fraction(l, op, r)
    if isinstance(l, int) and isinstance(r, int):
        return solve_number(l, op, r)
    if isratexp(l) and isratexp(r):
        return solve-fraction(l, op, r)
    if isterm(l) and isterm(r):
        return solve_term(l, op, r)
    raise ValueError("Solve can't handle this: " + str(operation))

# fraction(or rat-expr) symbol fraction(or rat-expr) -> fraction(or rat-expr)
# this procedure evaluates fractions - adds, multiplies, and subtracts fractions or rational expressions
def solve_fraction(rat1, operator, rat2):
    (numer1, op, denom1 ) = rat1
    (numer2, opx, denom2) = rat2
    if operator == '+':
        return add(mul(numer1, denom2), mul(numer2, denom1)), '/', mul(denom1,denom2)
    if operator == '-':
        return sub(mul(numer1, denom2), mul(numer2, denom1)), '/', mul(denom1,denom2)
    if operator == '*':
        return mul(numer1,numer2), '/', mul(denom1,denom2)
    else:
        return 0

# number symbol number -> number
# adds, multiplies, and subtracts numbers 
def solve_number(num1, operator, num2):
    if operator == '+':
        return num1 + num2
    if operator == '-':
        return num1 - num2
    if operator == '*':
        return num1 * num2
    else:
        return 0
    
# monomial symbol monomial -> monomial
def solve_term(term1, op, term2):
    if op == '+':
        return add(term1, term2)
    if op == '-':
        return sub(term1, term2)
    if op == '*':
        return mul(term1, term2)
    else:
        return 0

# Exp -> bool
# checks if a given Exp is a fraction;
# if yes, then it evaluates to True; otherwise, it's false.
def isfraction(exp):
    if isinstance(exp, tuple) and len(exp) == 3:
        (l, op, r) = exp
        return len(exp) == 3 and op == '/'
    else:
        return False
# Exp -> bool
# checks if a given Exp is a rational-expression
# given: isratexp(((2,'*','x') '/', (2,'*','x')));
# expect: True
def isratexp(exp):
    if isinstance(exp, tuple):
        (l, op, r) = exp
        return isinstance(exp, tuple) and isterm(l) and isterm(r) and op == '/'
    else:
        return False
# Exp -> bool
# this function determines if the given Exp is a monomial
def isterm(exp):
    if isinstance(exp, tuple) and len(exp) == 3:
        (l, op, v) = exp
        return isinstance(exp, tuple) and isinstance(l, int) and op == '*' and v == 'x'
    else:
        return False

# Exp Exp -> Exp
# adds different types of Exps - it adds fractions,
# rational expressions, terms, and ints.
def add(exp1, exp2):
    if isinstance(exp1, int) and isinstance(exp2, int):
        return exp1 + exp2
    if isfraction(exp1) and isfraction(exp2):
        (numer, op, denom) = exp1
        (numer2, opx, denom2) = exp2
        return (numer * denom2) + (numer2 * denom), '/', (denom * denom2)
    if isterm(exp1):
        (const, p, var) = exp1
        (const2, p2, var2) = exp2
        if var == var2:
            return const+const2, p, var
    if len(exp1) == 5 and len(exp2) == 5:
        (l_operand, op, r_operand, expt, num) = exp1
        (left_operand, opx, right_operand, exptx, num2) = exp2
        if r_operand == right_operand:
            return l_operand+left_operand, op, r_operand, expt, num
        if r_operand != right_operand:
            return exp1, '+', exp2
    else:
        return 0

# Exp Exp -> Exp
# substracts different types of Exps - it subtracts
# fractions, ints, terms, and rational-expressions
def sub(exp1, exp2):
    if isinstance(exp1, int) and isinstance(exp2, int):
        return exp1 - exp2
    if isfraction(exp1) and isfraction(exp2):
        (numer, op, denom) = exp1
        (numer2, opx, denom2) = exp2
        return (numer * denom2) - (numer2 * denom), '/', (denom * denom2)
    if isterm(exp1):
        (const, p, var) = exp1
        (const2, p2, var2) = exp2
        if var == var2:
            return const-const2, p, var
    if len(exp1) == 5 and len(exp2) == 5:
        (l_operand, op, r_operand, expt, num) = exp1
        (left_operand, opx, right_operand, exptx, num2) = exp2
        if r_operand == right_operand:
            return l_operand-left_operand, op, r_operand, expt, num
        if r_operand != right_operand:
            return exp1, '-', exp2
    else:
        return 0

# Exp Exp -> Exp
# multiplies different types of Exps
def mul(exp1, exp2):
    if isinstance(exp1, int) and isinstance(exp2, int):
        return exp1 * exp2
    if isfraction(exp1):
        (numer, op, denom) = exp1
        (numer2, opx, denom2) = exp2
        return numer * numer2, '/', denom * denom2
    if isterm(exp1):
        (l_operand, op, r_operand) = exp1
        (left_operand, op, right_operand) = exp2
        if r_operand == right_operand:
            return l_operand*left_operand, op, r_operand, '**', 2
        else:
            return 0

# tests
def tests():
    # ints
    num1 = 2
    num2 = 3
    exp = num1, '+', num2
    assert solve(exp) == 5

    # fractions
    frac1 = 2, '/', 3
    exp2 = frac1, '+', frac1
    assert solve(exp2) == (12, '/', 9)

    # terms ie monomials
    t1 = 2, '*', 'x'
    t2 = 4, '*', 'x'
    exp3 = t1, '+', t1
    exp4 = t2, '-', t1
    exp5 = t2, '*', t1
    assert solve(exp3) == (4, '*', 'x')
    assert solve(exp4) == (2, '*', 'x')
    assert solve(exp5) == (8, '*', 'x', '**', 2)

    # rational-expressions
    t3 = 1, '*', 'x'
    rat1 = t1, '/', t1
    rat2 = t2, '/', t2
    rat3 = t3, '/', t3
    exp6 = rat1, '*', rat1
    exp7 = rat1, '+', rat1
    exp8 = rat2, '-', rat3
    assert solve(exp6) == ((4, '*', 'x', '**', 2), '/', (4, '*', 'x', '**', 2))
    assert solve(exp7) == ((8, '*', 'x', '**', 2), '/', (4, '*', 'x', '**', 2))

    return 'All Tests passed!'

print tests()
