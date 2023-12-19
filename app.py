from flask import Flask, request, send_from_directory, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import mpld3

app = Flask(__name__)

sections = {
    'introduction': ['page1', 'page2', 'page3']
}

def get_result():
    fig, ax = plt.subplots()  # Create a figure and axes
    ax.set_title('Blank Graph')  # Set a title for the graph
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.grid()

    # Customize the graph as needed (e.g., labels, limits, styles)
    ax.set(xlim=(0, 8), xticks=np.arange(0, 9), 
           ylim=(0, 8), yticks=np.arange(0, 9))
    
    # Convert the Matplotlib figure to HTML
    blankgraph = mpld3.fig_to_html(fig)
    return blankgraph

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

@app.route('/introduction/page2')
def intropage2():
    python_result = get_result()
    
    category = 'introduction'
    page = 'page2'
    prev_page = sections[category][sections[category].index(page) - 1] if page in sections[category] and sections[category].index(page) > 0 else None
    next_page = sections[category][sections[category].index(page) + 1] if page in sections[category] and sections[category].index(page) < len(sections[category]) - 1 else None

    return render_template('introduction/page2.html', html_result=python_result, prev_page=prev_page, next_page=next_page)

if __name__ == '__main__':
    app.run(debug=True, port=8000)