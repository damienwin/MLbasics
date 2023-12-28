from flask import Flask, request, send_from_directory, render_template, jsonify, render_template_string
import plotly.express as px
import numpy as np

app = Flask(__name__)

sections = {
    'linear_regression': ['page1', 'page2', 'page3']
}

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/repo')
def repo():
    return render_template('repo.html')

@app.route('/<category>/<page>')
def show_page(category, page):
    if category in sections:
        current_section = sections[category]
        if page in current_section:
            current_index = current_section.index(page)
            prev_page = current_section[current_index - 1] if current_index > 0 else None
            next_page = current_section[current_index + 1] if current_index < len(current_section) - 1 else None
            return render_template(f'{category}/{page}.html', category=category, page=page, prev_page=prev_page, next_page=next_page)
    return "Page not found", 404

@app.route('/linear_regression/page1')
def linearpage():
    python_result = get_result()
    
    category = 'linear_regression'
    page = 'page1'
    prev_page = sections[category][sections[category].index(page) - 1] if page in sections[category] and sections[category].index(page) > 0 else None
    next_page = sections[category][sections[category].index(page) + 1] if page in sections[category] and sections[category].index(page) < len(sections[category]) - 1 else None

    return render_template('linear_regression/page1.html', html_result=python_result, prev_page=prev_page, next_page=next_page)

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
        width=840, height=480
    )

    return fig

@app.route('/linear_regression/page2')
def linearpage2():
    res = initial_graph().to_html(full_html=False)

    return render_template('linear_regression/page2.html', initial_graph=res)

def add_line_func():
    fig = initial_graph()
    fig.add_scatter(x=initial_x, y=(25 * initial_x + 100), mode='lines', name="Prediction Line")
    return fig
    
@app.route('/linear_regression/page2/line', methods=['GET'])
def addline():
    fig = add_line_func()
    line_plot = fig.to_html(full_html=False)
    return render_template('linear_regression/page2.html', initial_graph=line_plot)


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


if __name__ == '__main__':
    app.run(debug=True, port=8000)