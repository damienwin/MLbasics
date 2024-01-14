from flask import Blueprint, Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

gd_bp = Blueprint('gd', __name__, url_prefix='/gradient_descent')

@gd_bp.route('/page1')
def gdpage1():
    w_graph = w_cost_parabola()
    return render_template('gradient_descent/page1.html', prev_page='page2', next_page='page2', w_graph=w_graph)

@gd_bp.route('/page2')
def gdpage2():
    return render_template('gradient_descent/page2.html', prev_page='page1', next_page='page3')

@gd_bp.route('/page3')
def gdpage3():
    w_graph = gdsteps()
    line_graph = line_animation()
    return render_template('gradient_descent/page3.html', prev_page='page2', w_graph=w_graph, line_graph=line_graph)

# Generate random data with optimal line of y = 1.58x + 2.9
initial_x = np.linspace(0, 10, 25)
initial_y = .35 * initial_x + np.random.randn(25) * .6 + 2.9

def cost(w, b):
    # I use np.array vectorizing to make it more efficient and concise
    predicted_y = w * initial_x + b
    squared_diff = (predicted_y - initial_y) ** 2
    mse_cost = np.mean(squared_diff) / 2

    return mse_cost

w_values = np.linspace(-15, 15, 100)
w_cost_values = [cost(w, 2.9) for w in w_values]

def dx_cost(w, b):
    predicted_y = w * initial_x + b
    derivative = (predicted_y - initial_y) * initial_x # function when taking derivative of cost
    dx_mean = np.mean(derivative)

    return dx_mean

def w_cost_parabola():
    fig = px.line(x=w_values, y=w_cost_values, labels={'x': 'w', 'y': 'cost(w)'})
    
    # update layout
    fig.update_layout(
        title="Cost vs. w value",
        template='simple_white',
        xaxis=dict(range=[-15,15], dtick=3, showgrid=True),
        yaxis=dict(range=[0,2400], dtick=300, showgrid=True),
        width=600, height=600
    )

    graph = fig.to_html(full_html=False)
    return graph

b_values = np.linspace(-30, 40, 100)
b_cost_values = [cost(1.8, b) for b in b_values]

# create gradient descent steps for w
w_steps = []
w = -15
learning_rate = .003 # adjust to change size of steps
w_step = 1
i = 0
while abs(w_step) > .001 and i < 150:
    w_steps.append(w)
    derivative = dx_cost(w, 2.9)
    w_step = learning_rate * derivative
    w = w - w_step
    i += 1 


def gdsteps():
    fig = go.Figure(
        data=[go.Scatter(x=w_values, y=w_cost_values, mode="lines", line=dict(color="#00CED1", width=2), showlegend=False),
              go.Scatter(x=w_values, y=w_cost_values, mode="lines", line=dict(color="#00CED1", width=2), name="Cost vs. w value")],
        layout=go.Layout(
            xaxis=dict(range=[-15,15], dtick=3, showgrid=True),
            yaxis=dict(range=[0,4000], dtick=500, showgrid=True),
            title_text="Gradient Descent Steps",
            width=750, height=600,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                            method="animate",
                            args=[None])])]),
        frames=[go.Frame(
            data=[go.Scatter(
                x=[w],
                y=[cost(w, 2.9)],
                mode="markers",
                marker=dict(color="red", size=10),
                name=f"Current w = {w:.3f}<br>Cost = {cost(w, 2.9):.2f}",
                showlegend=True
            )])

            for w in w_steps]
    )

    graph = fig.to_html()
    return graph

def line_animation():
    x_values = np.linspace(0, 10, 100)
    fig = go.Figure(
        data=[go.Scatter(x=x_values, y=-10 * x_values + 2.9, mode="lines", line=dict(color="#00CED1", width=2))] + # initial linear function
            [go.Scatter(
                x=[x, x], 
                y=[y, w * x + 2.9], 
                mode='lines+markers', 
                line=dict(color="red", width=2, dash='dot'),
                showlegend=False
            )
            for x, y in zip(initial_x, initial_y)] + # loop through all points and add cost line for each
            [go.Scatter(x=initial_x, y=initial_y, mode="markers", marker=dict(color="red", size=10), name="Dataset Points"), # Add Data Points
             go.Scatter(x=[None], y=[None], mode='lines', line=dict(color='red', width=2, dash='dot'), name='Cost Lines')], # Add Cost to Legend
        layout=go.Layout(
            xaxis=dict(range=[0,10], dtick=1, showgrid=True),
            yaxis=dict(range=[0,10], dtick=1, showgrid=True),
            title_text="Plotted w value and Data Points",
            width=700, height=600,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="Play",
                            method="animate",
                            args=[None])])]),
        frames=[go.Frame(
            data=[go.Scatter(
                x=np.arange(0, 10, .1),
                y=w * np.arange(0, 10, .1) + 2.9,
                mode="lines",
                line=dict(color="#00CED1", width=2),
                name=f"{w:.3f}x + 2.9"  
            )] +  # adjust line for each w
            [go.Scatter(
                x=[x, x],
                y=[y, w * x + 2.9],
                mode='lines',
                line=dict(color="red", width=2, dash='dot')
            )
            for x, y in zip(initial_x, initial_y)] # adjust cost line for each w
        )
        for w in w_steps]
    )

    graph = fig.to_html()
    return graph

def b_cost_parabola():
    fig = px.line(x=b_values, y=b_cost_values, labels={'x': 'b', 'y': 'cost(w)'})
    
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


