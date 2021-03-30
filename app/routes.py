from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import UploadMapForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.j2')


"""
A B 10
B D 15
A C 20
C D 30
B E 50
D E 30
"""


@app.route('/upload_map', methods=['GET', 'POST'])
def upload_map():
    form = UploadMapForm()
    if form.validate_on_submit():
        flash('Map uploaded successfully!')
        return redirect(url_for('index'))
    return render_template('upload_map.html.j2', title='Upload Map', form=form)
