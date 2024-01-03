from flask import Blueprint, Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

cost_bp = Blueprint('cost', __name__, url_prefix='/cost')

@cost_bp.route('/page1')
def costpage1():
    # Create figure
    fig = go.Figure()

    # Add traces, one for each slider step
    for weight in np.arange(-5, 5, 0.25):
        fig.add_trace(
            go.Scatter(
                visible=False,
                line=dict(color="#00CED1", width=2),
                x=np.arange(0, 10, 0.01),
                y=weight * np.arange(0, 10, 0.01) 
            )
        )

    # Make 1st trace visible
    fig.data[10].visible = True

    # Create and add slider
    weight_steps = []
    for i, wval in enumerate(np.arange(-5, 5, 0.25)):
        step = dict(
            method="update",
            args=[{"visible": [i == j for j in range(len(fig.data))]}],
            label=f"{wval}"
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        weight_steps.append(step)

    weight_slider = dict(
        active=30,
        currentvalue={"prefix": "Slope(w): "},
        pad={"t": 50},
        steps=weight_steps,
        tickwidth=.5,
        len=.5,
        x=.5
    )

    yint_steps = []
    for i, bval in enumerate(np.arange(0, 8, .25)):
        y_values = [weight * np.arange(0, 10, 0.01) + bval for weight in np.arange(-5, 5, 0.25)]
        step = dict(
            method="restyle",  # Use "restyle" method to update traces
            args=["y", y_values],  # Update y-values based on the selected y-intercept
            label=f"{bval}",
        )
        yint_steps.append(step)

    yint_slider = dict(
        active=5,
        currentvalue={"prefix": "Y-Intercept(b): "},
        pad={"t": 50},
        steps=yint_steps,
        tickwidth=.5,
        len=.5,
        x=0
    )
    
    sliders = [weight_slider, yint_slider]
    
    fig.update_layout(
        title="Updatable Linear Function",
        template='simple_white',
        sliders=sliders,
        xaxis=dict(range=[0,10], dtick=1, showgrid=True),
        yaxis=dict(range=[0,8], dtick=1, showgrid=True),
        width=900, height=600
    )
    
    graph = fig.to_html()
    return render_template('cost/page1.html', prev_page='page3', next_page='page2', graph=graph)

@cost_bp.route('/page2')
def costpage2():
    return render_template('cost/page2.html', prev_page='page1', next_page='page3')

@cost_bp.route('/page3')
def costpage3():
    return render_template('cost/page3.html', prev_page='page2', next_page='page4')