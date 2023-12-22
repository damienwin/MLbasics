from flask import Flask, request, send_from_directory, render_template
import plotly.express as px
import numpy as np



app = Flask(__name__)

sections = {
    'linear_regression': ['page1', 'page2', 'page3']
}

def get_result():
    # make data
    x = np.linspace(0, 10, 100)
    
    # graph lines and points on figure
    fig = px.line(x=x, y=(0.5 * x + 2), labels={'x': 'x-axis', 'y': 'y-axis'})
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

if __name__ == '__main__':
    app.run(debug=True, port=8000)