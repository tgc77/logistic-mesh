from flask import render_template, flash, redirect, url_for
import json
from app import app, db
from app.forms import UploadMapForm, FindBestRouteForm
from app.models import LogisticMeshMap


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('list_maps'))
    # return render_template('index.html.j2')


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
        logistic_map = LogisticMeshMap()
        logistic_map.mapname = form.mapname.data
        log_map = [s.rstrip().split() for s in form.routes.data.split('\n')]
        logistic_map.routes = json.dumps(log_map)
        db.session.add(logistic_map)
        db.session.commit()
        flash('Map uploaded successfully!')
        return redirect(url_for('index'))
    return render_template('upload_map.html.j2', title='Upload Map', form=form)


@app.route('/list_maps')
def list_maps():
    logistic_maps = LogisticMeshMap.query.all()

    return render_template('list_maps.html.j2', title='Map List', logistic_maps=logistic_maps)


@app.route('/find_best_route')
def find_best_route():
    form = FindBestRouteForm()
    if form.validate_on_submit():
        logistic_map = LogisticMeshMap.query.filter_by(
            mapname=form.mapname).first_or_404()

    return render_template('show_best_route.html.j2', title='Best Route Result')


def process_best_route_request(routes):
    ...
