import random
import math
from mandel import mandelbrot


def is_number(s):
    """Checks if a string can be evaluated as a float
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


OPERATORS = {  # Function and number of operands for each operator or function
    "+": (lambda x, y: min([max([x + y, -1.00]), 1.00]), 2),
    "-": (lambda x, y: min([max([x - y, -1.00]), 1.00]), 2),
    "*": (lambda x, y: x * y, 2),
    # "/": (lambda x, y: x / y, 2), # Proper division
    "/": (lambda x, y: x / (y + .001*(y == 0)), 2),  # Divide by zero error workaround
    # "sqrt": (lambda x: math.sqrt(x), 1),  # Proper square root
    "sqrt": (lambda x: math.sqrt(abs(x)), 1),  # Square root of negative number workaround
    # "sin": (math.sin, 1),
    # "cos": (math.cos, 1),
    # "tan": (math.tan, 1)
    "pi_*_sin": (lambda x: math.sin(math.pi*x), 1),
    "pi_*_cos": (lambda x: math.cos(math.pi*x), 1),
    "pi_*_tan": (lambda x: math.tan(math.pi*x), 1),
    "mandelbrot": (mandelbrot, 2)
    # ".5_pi_/_%": (lambda x: x % (.5 / math.pi), 1)
}


def rpn(expr, variables=None):
    """Evaluate an expression given in Reverse Polish Notation/postfix
    expr -- Expression to be evaluated
    variables -- Dictionary of any variables in expr and corresponding values; 
    """
    if expr == '':
        return -1
    if variables is None:
        variables = []

    stack = []
    tokens = expr.split(' ')

    while tokens:
        token = tokens.pop(0)  # Take leftmost token
        if token == '':  # Skip empty tokens
            continue
        elif token in OPERATORS:
            current_op = OPERATORS[token][0]
            num_operands = OPERATORS[token][1]
            operands = []
            for i in range(num_operands):
                operands.append(stack.pop())
            operator_output = current_op(*operands)
            stack.append(operator_output)
        elif token in variables:
            stack.append(variables[token])
        elif is_number(token):
            stack.append(float(token))

        else:
            raise ValueError("Token is not a number, variable, or an operator: {}".format(token))
            # raise ValueError(f"Token is not a number, variable, or an operator: {token}")

    if len(stack) == 1:
        return stack[0]
    else:
        raise ValueError("Expression has invalid number of operands or operators")


def random_rpn_expr(p_nest=.9, resolution_variables=('x', 'y')):
    """ Recursively generate random functions in postfix notation
    p_nest -- probability from 0 to 1.0 of continuing to wrap function; Higher probability results in more complex final
    expression
    resolution_variables -- When expression stops nesting, it resolves to x or y assumed for image/complex
    function creation
    """
    n = random.random()
    if n < p_nest:
        # Continue nesting functions
        op = random.choice(list(OPERATORS))
        num_operands = OPERATORS[op][1]

        if num_operands == 1:
            return "{} {}".format(random_rpn_expr(p_nest), op)
            # return f"{random_rpn_expr(p_nest)} {op}"
        elif num_operands == 2:
            return "{} {} {}".format(random_rpn_expr(p_nest ** 2), random_rpn_expr(p_nest ** 2), op)
            # return f"{random_rpn_expr(p_nest ** 2)} {random_rpn_expr(p_nest ** 2)} {op}"

    else:
        # Resolve to a variable
        return random.choice(resolution_variables)


def rpn_batch_test(num_tests):
    for i in range(num_tests):
        variables = {
            "x": int(random.random() * 10 + 1),
            "y": int(random.random() * 10 + 1)
        }
        s = random_rpn_expr()
        print("x = {}, y = {}\n expr: {}".format(variables['x'], variables['y'], s))
        evaluated = rpn(s, variables)
        print("result: {}".format(evaluated))
