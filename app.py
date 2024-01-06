import re
import traceback
from functools import reduce
from pprint import pprint

from flask import Flask, render_template, request, session
from sympy import And, Implies, Nor, Not, Or, Symbol, init_printing
from sympy.printing.mathml import mathml, print_mathml

from logic.expression.logic_simplify import logic_simplify_expr_string
from logic.graph.rule import create_digraph, visualize_graph, is_symmetric, is_reflexive, is_transitive, find_reflexive_closure, find_symmetric_closure, find_transitive_closure
from collections import OrderedDict


fns = [
    lambda text: re.sub(r'\s+', '', text),
    lambda text: re.sub(r'\=\>', '→', text),
    lambda text: re.sub(r'([^\~\s\|\&\(\)])', r'<span class="variable">\1</span>', text),
    lambda text: re.sub(r'([\(\)])', r'<span class="bracket"> \1 </span>', text),
    lambda text: re.sub(r'\→', '<span class="operator">→</span>', text),
    lambda text: re.sub(r'\~', '<span class="variable">~</span>', text),
    lambda text: re.sub(r'\|', '<span class="operator">∨</span>', text),
    lambda text: re.sub(r'\&', '<span class="operator">∧</span>', text),
    lambda text: re.sub(r'\+', '<span class="operator"> + </span>', text),
    lambda text: re.sub(r'\*', '<span class="operator"> * </span>', text),
]
replace = lambda text: reduce(lambda a, b: b(a), fns, fn(text))

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

def find_duality(expr):
    expr = expr.replace(' ', '')
    result = ''

    for char in expr:
        if char == '0':
            result += '1'
        elif char == '1':
            result += '0'
        elif char == '+':
            result += ') * ('
        elif char == '*':
            result += '+'
        else:
            result += char

    return f"({result})"

def simplify_boolean_expression(expression):
    # Remove all spaces from the expression
    expression = expression.replace(" ", "")

    # Define a regular expression pattern to match redundant parentheses
    pattern = re.compile(r'\((\w+)\)')

    # Replace redundant parentheses with the captured content
    simplified_expression = pattern.sub(r'\1', expression)

    return simplified_expression


if __name__ == "__main__":
    app = Flask(__name__)
    app.secret_key = 'u0dyD1wR1BLcYWa'

    @app.route('/rut-gon-bieu-thuc-logic')
    @app.route('/')
    def rut_gon_bieu_thuc_logic():
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
        template = 'expression/tim-gia-tri-bieu-thuc.html'
        args = request.args
        if "expression" in args:
            expression = args.get("expression")
            try:
                pprint(expression)
                expr = expression
                steps = []
                steps.append([expr, ''])

                i = 0
                while len(expr) > 1 and i < 100:
                    expr = re.sub('~0', '1', expr)
                    expr = re.sub('~1', '0', expr)
                    for e in re.findall(r'(\([^\(\)]+\))', expr):
                        expr = expr.replace(e, str(1 if eval(e) > 0 else 0))

                    if steps[-1][0] != expr:
                        steps.append([expr, ''])

                    if re.match(r'^[0|1|\+|*|\s]+$', expr):
                        expr = str(1 if eval(expr) > 0 else 0)
                        steps.append([expr, ''])

                    i += 1
                
                if steps[-1][0] != expr:
                    steps.append([str(1 if eval(expr) > 0 else 0), ''])

                print (steps)
                return render_template(template, steps=[[replace(s[0]), s[1]] for s in steps], expression=expression)
            except Exception as ex:
                traceback(ex)
                return render_template(template, error="Invalid expression") 
        
        return render_template(template)

    @app.route('/tim-doi-ngau-bieu-thuc')
    def tim_doi_ngau_bieu_thuc():
        template = 'expression/tim-doi-ngau-bieu-thuc.html'
        args = request.args
        if "expression" in args:
            expression = args.get("expression")
            try:
                pprint(expression)
                steps = []
                steps.append([expression, ''])
                dual_expression = find_duality(expression)
                output_expression = simplify_boolean_expression(dual_expression)
                steps.append([output_expression, ''])
                print ("#", steps)
                return render_template(template, steps=[[replace(s[0]), s[1]] for s in steps], expression=expression)
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
                    graph =create_digraph(num_edges, list_edge_name)
                    visualize_graph(graph, 'static/images/origin_image.png')
                    tinh_phan_xa = is_reflexive(graph)
                    tinh_doi_xung = is_symmetric(graph)
                    tinh_bac_cau = is_transitive(graph)

                    print("Bao đóng phản xạ:")
                    visualize_graph(find_reflexive_closure(graph),  'static/images/phan_xa.png')

                    print("Bao đóng đối xứng:")
                    visualize_graph(find_symmetric_closure(graph),  'static/images/doi_xung.png')

                    print("Bao đóng bắc cầu:")
                    visualize_graph(find_transitive_closure(graph),  'static/images/bac_cau.png')

                return render_template('graph/index.html', edges=edges, vertexes=vertexes, pos="Image", tinh_phan_xa=tinh_phan_xa, tinh_doi_xung=tinh_doi_xung, tinh_bac_cau=tinh_bac_cau)           
            except Exception as ex:
                traceback(ex)
                return render_template('graph/index.html', error="Invalid Input") 

    app.run(debug=True, host="0.0.0.0", port=9999)
