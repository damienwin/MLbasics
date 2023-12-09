from flask import Blueprint, render_template, redirect, url_for, request, jsonify

views = Blueprint(__name__, 'views')

sections = {
    'introduction': ['introduction_page', 'introduction_page2', 'introduction_page3']
}

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/repo')
def repo():
    return render_template('repo.html')

@views.route('/<category>/<page>')
def show_page(category, page):
    print(f"Category: {category}, Page: {page}")
    if category in sections:
        current_section = sections[category]
        print(f"Current Section: {current_section}")
        if page in current_section:
            current_index = current_section.index(page)
            prev_page = current_section[current_index - 1] if current_index > 0 else None
            next_page = current_section[current_index + 1] if current_index < len(current_section) - 1 else None
            print(f"Prev Page: {prev_page}, Next Page: {next_page}")
            return render_template(f'{category}/{category}_page.html', category=category, page=page, prev_page=prev_page, next_page=next_page)
    return "Page not found", 404