from app import app
from flask import render_template, redirect, url_for, request
from forms import ZipcodeForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ZipcodeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            return redirect(url_for('results', zipcode = form.zipcode.data))
        else:
            return render_template('index.html', form = form, wrong = True)
    return render_template('index.html', form = form)

@app.route('/results')
def results():
    zipcode = request.args.get('zipcode')
    return render_template('results.html', zipcode = zipcode)
