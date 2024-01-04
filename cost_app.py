from flask import Blueprint, Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

cost_bp = Blueprint('cost', __name__, url_prefix='/cost')

@cost_bp.route('/page1')
def costpage1():
    # Create figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            visible=True,  # Set to visible initially
            line=dict(color="#00CED1", width=2),  # Adjust line properties as needed
            x=np.arange(0, 10, 0.01),
            y=np.arange(0, 10, 0.01),
            showlegend=False
        )
    )

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
        active=24,
        currentvalue={"prefix": "Slope(w): "},
        pad={"t": 50},
        steps=weight_steps,
        tickwidth=.5,
        len=.5,
        x=0
    )

    yint_steps = []
    for i, bval in enumerate(np.arange(0, 8, .25)):
        y_values = [weight * np.arange(0, 10, 0.01) + bval for weight in np.arange(-5, 5, 0.25)]
        step = dict(
            method="restyle",
            args=[{"y": y_values}],
            label=f"{bval}"
        )
        yint_steps.append(step)

    yint_slider = dict(
        active=0,
        currentvalue={"prefix": "Y-Intercept(b): "},
        pad={"t": 50},
        steps=yint_steps,
        tickwidth=.5,
        len=.5,
        x=0.5
    )

    static_shapes = [
        dict(
            type='circle',
            xref='x',
            yref='y',
            x0=1.9, y0=2.85,
            x1=2.1, y1=3.15,
            fillcolor='red',
            line=dict(color='red'),
            opacity=1,
            visible=True
        ),
        dict(
            type='circle',
            xref='x',
            yref='y',
            x0=3.9, y0=3.35,
            x1=4.1, y1=3.65,
            fillcolor='red',
            line=dict(color='red'),
            opacity=1,
            visible=True
        ),
        dict(
            type='circle',
            xref='x',
            yref='y',
            x0=5.9, y0=3.85,
            x1=6.1, y1=4.15,
            fillcolor='red',
            line=dict(color='red'),
            opacity=1,
            visible=True
        ),
        dict(
            type='circle',
            xref='x',
            yref='y',
            x0=7.9, y0=4.35,
            x1=8.1, y1=4.65,
            fillcolor='red',
            line=dict(color='red'),
            opacity=1,
            visible=True
    )]
    
    sliders = [weight_slider, yint_slider]

    fig.update_layout(
        title="<b>Updatable Linear Function (y = wx + b)</b>",
        template='simple_white',
        sliders=sliders,
        xaxis=dict(range=[0,10], dtick=1, showgrid=True),
        yaxis=dict(range=[0,8], dtick=1, showgrid=True),
        width=870, height=600,
        shapes=static_shapes,

    )


    graph = fig.to_html()
    return render_template('cost/page1.html', prev_page='page3', next_page='page2', graph=graph)



@cost_bp.route('/page2')
def costpage2():
    return render_template('cost/page2.html', prev_page='page1', next_page='page3')

@cost_bp.route('/page3')
def costpage3():
    return render_template('cost/page3.html', prev_page='page2', next_page='page4')