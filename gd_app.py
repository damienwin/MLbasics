from flask import Blueprint, Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

gd_bp = Blueprint('gd', __name__, url_prefix='/gradient_descent')

@gd_bp.route('/page1')
def gdpage1():
    return render_template('gradient_descent/page1.html', prev_page='page2', next_page='page2')

@gd_bp.route('/page2')
def gdpage2():
    w_graph = w_cost_parabola()
    b_graph = b_cost_parabola()
    return render_template('gradient_descent/page2.html', prev_page='page1', next_page='page3', w_graph=w_graph, b_graph=b_graph)

# Generate random data with optimal line of y = 1.58x + 4.7
initial_x = np.linspace(0, 10, 25)
initial_y = 1.8 * initial_x + 4.7

def cost(w, b):
    # I use np.array vectorizing to make it more efficient and concise
    predicted_y = w * initial_x + b
    squared_diff = (predicted_y - initial_y) ** 2
    mse_cost = np.mean(squared_diff) / 2

    return mse_cost

w_values = np.linspace(-10, 14, 100)
w_cost_values = [cost(w, 4.7) for w in w_values]

def w_cost_parabola():
    fig = px.line(x=w_values, y=w_cost_values, labels={'x': 'w', 'y': 'cost'})
    
    # update layout
    fig.update_layout(
        title="Cost vs. w value",
        template='simple_white',
        xaxis=dict(range=[-10,14], dtick=2, showgrid=True),
        yaxis=dict(range=[0,2400], dtick=300, showgrid=True),
        width=600, height=600
    )

    graph = fig.to_html(full_html=False)
    return graph

b_values = np.linspace(-30, 40, 100)
b_cost_values = [cost(1.8, b) for b in b_values]

def b_cost_parabola():
    fig = px.line(x=b_values, y=b_cost_values, labels={'x': 'w', 'y': 'cost'})
    
    # update layout
    fig.update_layout(
        title="Cost vs. b value",
        template='simple_white',
        xaxis=dict(range=[-30,40], dtick=10, showgrid=True),
        yaxis=dict(range=[0,600], dtick=100, showgrid=True),
        width=600, height=600
    )

    graph = fig.to_html(full_html=False)
    return graph


