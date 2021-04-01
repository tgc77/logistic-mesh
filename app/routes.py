from flask import render_template, flash, redirect, url_for
import json

from app import app, db
from app.forms import UploadMapForm, FindBestRouteForm
from app.models import LogisticMeshMap
from app.logistic_mesh.best_route import get_best_route


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('list_maps'))
    # return render_template('index.html.j2')


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


@app.route('/find_best_route', methods=['GET', 'POST'])
def find_best_route():
    form = FindBestRouteForm()

    maps_name = db.session.query(LogisticMeshMap.mapname).all()
    form.mapname.choices = [name[0] for name in maps_name]

    if form.validate_on_submit():
        lm_map = LogisticMeshMap.query.filter_by(
            mapname=form.mapname.data).first_or_404()

        data = get_best_route(json.loads(lm_map.routes))
        result = dict()
        result['mapname'] = lm_map.mapname
        result['best_route'] = data[0]
        result['cost'] = data[1]

        return render_template('show_best_route.html.j2', title='Best Route Result', result=result)
    return render_template('find_best_route.html.j2', title='Find Best Route', form=form)
