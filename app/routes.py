from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms import MessageForm

main_bp = Blueprint('main', __name__)

# Store messages in memory for simplicity - make it a global list
messages = []

@main_bp.route('/')
def index():
    return render_template('index.html', messages=messages)

@main_bp.route('/greet/<name>')
def greet(name):
    return render_template('index.html', greeting=f"Hello, {name}!", messages=messages)

@main_bp.route('/message', methods=['GET', 'POST'])
def message():
    form = MessageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_message = {
                'name': form.name.data,
                'message': form.message.data
            }
            messages.append(new_message)
            flash('Your message has been added!')
            return redirect(url_for('main.index'))
        else:
            flash('There was an error with your submission. Please check the form.')
    
    return render_template('form.html', form=form)

@main_bp.route('/health')
def health():
    return {'status': 'healthy'}, 200