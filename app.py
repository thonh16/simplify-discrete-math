import re
import traceback
from functools import reduce
from pprint import pprint

from flask import Flask, render_template, request, session
from sympy import And, Implies, Nor, Not, Or, Symbol, init_printing
from sympy.printing.mathml import mathml, print_mathml

from logic.expression.logic_simplify import logic_simplify_expr_string
from logic.graph.rule import create_digraph, visualize_graph
from collections import OrderedDict


if __name__ == "__main__":
    app = Flask(__name__)
    app.secret_key = 'u0dyD1wR1BLcYWa'

    @app.route('/rut-gon-bieu-thuc-logic')
    @app.route('/')
    def rut_gon_bieu_thuc_logic():
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
        
        template = 'expression/rut-gon-bieu-thuc-logic.html'
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
                return render_template(template, steps=steps, expression=expression, _expression=replace(expression))
            except Exception as ex:
                traceback(ex)
                return render_template(template, error="Invalid expression") 
        
        return render_template(template)
    

    @app.route('/tim-gia-tri-bieu-thuc')
    def tim_gia_tri_bieu_thuc():
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
        
        template = 'expression/tim-gia-tri-bieu-thuc.html'
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
                return render_template(template, steps=steps, expression=expression, _expression=replace(expression))
            except Exception as ex:
                traceback(ex)
                return render_template(template, error="Invalid expression") 
        
        return render_template(template)


    @app.route('/bai-toan-quan-he', methods=['GET', 'POST'])
    def graph_input():
        edges = []  # Initialize empty list to store edges
        vertexes = []

        if request.method == 'GET':
            return render_template('graph/index.html', edges=edges)
        else:
            try:
                args = request.form
                list_vertex_name = args.get("list_vertex_name")
                list_edge_name = args.get("list_edge_name")
                if list_vertex_name == "" or list_edge_name == "":
                    return render_template('graph/index.html', error="Invalid Input")
                else:
                    list_vertex_name = list_vertex_name.split(" ")
                    for vertex in list_vertex_name:
                        vertexes.append(vertex)


                    list_edge_name = list_edge_name.split(" ")
                    for edge in list_edge_name:
                        edges.append(edge)
                    num_edges = len(list_edge_name)
                    image_path = create_digraph(num_edges, list_edge_name)
                    print(image_path)
                return render_template('graph/index.html', edges=edges, button_text='Giải bài toán', vertexes=vertexes, pos="Image")           
            except Exception as ex:
                traceback(ex)
                return render_template('graph/index.html', error="Invalid Input") 

    app.run(debug=True, host="0.0.0.0")
