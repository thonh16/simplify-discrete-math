import re
import traceback
from functools import reduce
from pprint import pprint

from flask import Flask, render_template, request
from sympy import And, Implies, Nor, Not, Or, Symbol, init_printing
from sympy.printing.mathml import mathml, print_mathml

from logic.expression.logic_simplify import logic_simplify_expr_string

if __name__ == "__main__":
    app = Flask(__name__)

    fns = [
        lambda text: re.sub(r'\=\>', '→', text),
        lambda text: re.sub(r'([^\~\s\|\&\(\)])', r'<span class="variable">\1</span>', text),
        lambda text: re.sub(r'([\(\)])', r'<span class="bracket"> \1 </span>', text),
        lambda text: re.sub(r'\→', '<span class="operator">→</span>', text),
        lambda text: re.sub(r'\~', '<span class="variable">¬</span>', text),
        lambda text: re.sub(r'\|', '<span class="operator">∨</span>', text),
        lambda text: re.sub(r'\&', '<span class="operator">∧</span>', text),
    ]
    def fn(text):

        if type(text) == Implies:
            print ("1", len(text.args), text.args)
            return f"({fn(text.args[0])} => {fn(text.args[1])})"

        if type(text) == And:
            print ("2", len(text.args), text.args)
            return f"({' & '.join([fn(arg) for arg in text.args])})"

        if type(text) == Or:
            print ("3", len(text.args), text.args)
            return f"({' | '.join([fn(arg) for arg in text.args])})"

        if type(text) == Nor:
            print ("4", len(text.args), text.args)
            return f"~({fn(text.args[0])} | {fn(text.args[1])})"

        if type(text) == Not:
            print ("5", len(text.args), text.args)
            return f"~{fn(text.args[0])}"
        
        if type(text) == Symbol:
            return f"{text}"

        print (type(text))
        return str(text)

    replace = lambda text: reduce(lambda a, b: b(a), fns, fn(text))


    @app.route('/')
    def indexExpression():
        args = request.args
        if "expression" in args:
            expression = args.get("expression")
            # expr_str_1 = '((p => q) & p) => q'
            # expr_str_1 = '(p | q) & ~(~p & q)'
            try:
                pprint(expression)
                _, rules, results = logic_simplify_expr_string(expression)
                steps = []
                for i, _ in enumerate(rules):
                    print (results[i])
                    steps.append([replace(results[i]), rules[i]])
                return render_template('expression/index.html', steps=steps, expression=expression, _expression=replace(expression))
            except Exception as ex:
                traceback(ex)
                return render_template('expression/index.html', error="Invalid expression") 
        
        return render_template('expression/index.html')
    

    @app.route('/graph')
    def indexGraph():
        args = request.args
        if "expression" in args:
            expression = args.get("expression")
            # expr_str_1 = '((p => q) & p) => q'
            # expr_str_1 = '(p | q) & ~(~p & q)'
            try:
                pprint(expression)
                _, rules, results = logic_simplify_expr_string(expression)
                steps = []
                for i, _ in enumerate(rules):
                    print (results[i])
                    steps.append([replace(results[i]), rules[i]])
                return render_template('graph/index.html', steps=steps, expression=expression, _expression=replace(expression))
            except Exception as ex:
                traceback(ex)
                return render_template('graph/index.html', error="Invalid expression") 
        
        return render_template('graph/index.html')
    
    app.run(debug=True, host="0.0.0.0", port=9999)
