from flask import Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np
from cost_app import cost_bp
from gd_app import gd_bp
from demonstration import demonstration_bp
from config import SECRET_KEY

app = Flask(__name__)
app.register_blueprint(cost_bp)
app.register_blueprint(gd_bp)
app.register_blueprint(demonstration_bp)
app.secret_key = SECRET_KEY

@app.route('/')
def home():
    return render_template('index.html')

def get_result():
    # make data
    x = np.linspace(0, 10, 100)
    y = .5 * x + 2
    
    # graph lines and points on figure
    fig = px.line(x=x, y=y, labels={'x': 'x-axis', 'y': 'y-axis'})
    fig.update_traces(showlegend=True, name ='w*x + b')
    fig.add_scatter(x=[0], y=[2], mode='markers', marker=dict(color='red', size=10), name='y-intercept (b)')
    
    # update layout
    fig.update_layout(
        title="Basic Linear Function",
        template='simple_white',
        xaxis=dict(range=[0,10], dtick=1, showgrid=True),
        yaxis=dict(range=[0,8], dtick=1, showgrid=True),
        width=600, height=400
    )

    graph = fig.to_html(full_html=False)
    return graph

@app.route('/linear_regression/page1')
def linearpage():
    python_result = get_result()
    return render_template('linear_regression/page1.html', html_result=python_result, next_page='page2')

initial_x = np.linspace(1, 8, 16)
initial_y = 25 * initial_x + np.random.randn(16) * 16 + 100

def initial_graph():
    fig = px.scatter(x=initial_x, y=initial_y, labels={'x': 'sq. feet in thousands', 'y': '$ price in thousands'})    
    fig.update_traces(showlegend=True, name ='Given Dataset                 ')

    fig.update_layout(
        title="Pricing vs. Square Feet of Houses",
        template='simple_white',
        xaxis=dict(range=[1, 8], dtick=1, showgrid=True),
        yaxis=dict(range=[100, 300], dtick=50, showgrid=True), 
        width=810, height=460
    )

    return fig

@app.route('/linear_regression/page2')
def linearpage2():
    res = initial_graph().to_html(full_html=False)
    return render_template('linear_regression/page2.html', initial_graph=res, prev_page='page1')

def add_line_func():
    fig = initial_graph()
    fig.add_scatter(x=initial_x, y=(25 * initial_x + 100), mode='lines', name="Prediction Line")
    return fig
    
@app.route('/linear_regression/page2/line', methods=['GET'])
def addline():
    fig = add_line_func()
    line_plot = fig.to_html(full_html=False)
    return render_template('linear_regression/page2.html', initial_graph=line_plot, prev_page='page1')


@app.route('/linear_regression/page2/line/rand-point', methods=['GET'])
def update_plot():
    randx = np.random.uniform(1.2, 7.8)
    randy = 25 * randx + 100  # Use the prediction line equation

    # Create or update the Plotly plot using the accumulated data
    fig = add_line_func()
    fig.add_scatter(
        x=[randx], 
        y=[randy], 
        mode='markers', 
        marker=dict(color='red', size=10), 
        name=f'Input: {int(randx*1000)} ft.<sup>2</sup><br>Predicted Price: ${int(randy) * 1000}'
    )

    # Convert the updated Plotly figure to HTML and return it to the HTML page
    plot_html = fig.to_html(full_html=False)
    return render_template('linear_regression/page2.html', initial_graph=plot_html, prev_page='page1', next_page='page3')

@app.route('/linear_regression/page3')
def linearpage3():
    return render_template('linear_regression/page3.html', prev_page='page2', next_page='page1')



if __name__ == '__main__':
    app.run(debug=True, port=8000)