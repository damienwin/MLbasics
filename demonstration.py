from flask import Blueprint, Flask, request, send_from_directory, render_template, jsonify, render_template_string, session
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

demonstration_bp = Blueprint('demonstration', __name__, url_prefix='/demonstration')

@demonstration_bp.route('/')
def demonstration():
    return render_template('demonstration.html')


@demonstration_bp.route('/plot', methods=['POST'])
def plot():
    slope = float(request.form['slope'])
    y_intercept = float(request.form['intercept'])

    session['slope'] = slope
    session['y_intercept'] = y_intercept

    initial_x = np.linspace(0, 10, 25)
    initial_y = slope * initial_x + np.random.randn(25) * .5 + y_intercept

    fig=go.Figure(
        data=[go.Scatter(x=initial_x, y=initial_y, mode="markers", marker=dict(color="blue", size=5), showlegend=False),
              go.Scatter(x=[None], y=[None], mode="markers", marker=dict(color='blue', size=5), name="Data Points                          ")],
        layout=go.Layout(
                xaxis=dict(range=[0,10], dtick=1, showgrid=True),
                yaxis=dict(range=[0,10], dtick=1, showgrid=True),
                title_text="User Generated Data",
                width=900, height=600
        )
    )

    fig.update_layout(
        template='simple_white',
    )

    graph = fig.to_html()
    return render_template('demonstration.html', plot=graph, generated=True)

@demonstration_bp.route('/animate', methods=['POST'])
def animate():
    animation_slope = session.get('slope')
    animation_intercept = session.get('y_intercept')

    # Check if both slope and y_intercept have non-empty values
    if animation_slope and animation_intercept:
        
        x_data = np.linspace(0, 10, 25)
        y_data = animation_slope * x_data + np.random.randn(25) * .5 + animation_intercept

        cost_steps, w_steps, b_steps = gdsteps(x_data, y_data, animation_slope, animation_intercept)

        fig = go.Figure(
            data=[go.Scatter(x=x_data, y=[0], mode="lines", line=dict(color="#00CED1", width=2), name=f"Current Function: 0.000x + 0.00 <br>Cost: {cost_steps[0]:.3f}"), # initial linear function
                go.Scatter(x=x_data, y=y_data, mode="markers", marker=dict(color="blue", size=5), name="Dataset Points")], # Add Data Points
            layout=go.Layout(
                xaxis=dict(range=[0,10], dtick=1, showgrid=True),
                yaxis=dict(range=[0,10], dtick=1, showgrid=True),
                title_text="Regressing to Line of Best Fit",
                width=900, height=600,
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                method="animate",
                                args=[None])])]),
            frames=[go.Frame(
                data=[go.Scatter(
                    x=np.arange(-1, 11, .1),
                    y=w_steps[i] * np.arange(-1, 11, .1) + b_steps[i],
                    mode="lines",
                    line=dict(color="#00CED1", width=2),
                    name=f"Current Function: {w_steps[i]:.3f}x + {b_steps[i]:.2f} <br>Cost: {cost_steps[i]:.3f}"  
                )] 
            )
            for i in range(len(w_steps))] # iterate through all steps
        )
        fig.update_layout(
            template="simple_white"
        )
        fig.update_xaxes(title_text="x-axis")
        fig.update_yaxes(title_text="y-axis")

        graph=fig.to_html()
        return render_template('demonstration.html', animation=graph, prev_page='page3')


def gdsteps(x_data, y_data, animation_slope, animation_intercept):
    # Initialize weight and bias
    w = 0
    b = 0   
    # Tailored learning rates
    lr_w = 0.005 * abs(animation_slope)
    lr_b = 0.0225 * animation_intercept
    # Iterations
    epochs=200
    # Arrays to store steps
    cost_steps = []
    w_steps = []
    b_steps = []

    for epoch in range(epochs):
        # Calculate predictions
        y_predictions = w * x_data + b
        w_steps.append(w)
        b_steps.append(b)

        # Calculate errors
        errors = y_predictions - y_data

        # Calculate and store cost
        cost = np.mean(errors**2)
        cost_steps.append(cost)

        # Calculate gradients using derivatives
        dw = (2/x_data.shape[0]) * np.sum(errors * x_data)
        db = (2/x_data.shape[0]) * np.sum(errors)

        # Update weight and bias
        w -= lr_w * dw
        b -= lr_b * db

        if epoch > 0 and abs(cost_steps[epoch - 1] - cost) < .0001:
            print(f'Converged at epoch {epoch}, Cost: {cost}')
            break

    return cost_steps, w_steps, b_steps
