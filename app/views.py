from app import app
from twitter import *
from flask import render_template, redirect, url_for, request
from forms import ZipcodeForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = ZipcodeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            searchObject = Search(form.zipcode.data, form.search.data)
            searchObject.populateTweets()
            templateObject = {'lat':searchObject.lat, 'long':searchObject.long, 'radius':searchObject.radius,\
                'sentiment':searchObject.sentiment, 'popularHashtags':searchObject.popularHashtags, 'showcase':searchObject.showcase}
            return render_template('results.html', zipcode = form.zipcode.data, search = form.search.data, templateObject = templateObject)
        else:
            return render_template('index.html', form = form, wrong = True)
    return render_template('index.html', form = form)

@app.route('/results')
def results():
    zipcode = request.args.get('zipcode')
    search = request.args.get('search')
    templateObject = request.args.get('templateObject')
    return render_template('results.html', zipcode = zipcode, search = search, templateObject = templateObject)
