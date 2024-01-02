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
                line=dict(color="#00CED1", width=6),
                name="w = " + str(weight),
                x=np.arange(0, 10, 0.01),
                y=weight * np.arange(0, 10, 0.01)
            )
        )

    # Make 10th trace visible
    fig.data[10].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        wval = i/4 - 5
        step = dict(
            method="update",
            args=[{"visible": [False] * len(fig.data)},
                  {"title": f"Weight of Function: {wval}"},  # Title
                  ]
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [dict(
        active=10,
        currentvalue={"prefix": "Weight: "},
        pad={"t": 50},
        steps=steps,
    )]

    fig.update_layout(sliders=sliders, 
                      xaxis = dict(range=[0, 10]), 
                      yaxis = dict(range=[0, 8])
                      )
    
    graph = fig.to_html()
    return render_template('cost/page1.html', prev_page='page3', next_page='page2', graph=graph)

@cost_bp.route('/page2')
def costpage2():
    return render_template('cost/page2.html', prev_page='page1', next_page='page3')

@cost_bp.route('/page3')
def costpage3():
    return render_template('cost/page3.html', prev_page='page2', next_page='page4')