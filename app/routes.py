from flask import render_template, flash, redirect, url_for, abort
import json

from app import app, db
from app.forms import UploadMapForm, FindBestRouteForm
from app.models import LogisticMeshMap
from app.logistic_mesh.best_route import get_best_route
from app.utils import validate_map_inputs


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('list_maps'))


@app.route('/upload_map', methods=['GET', 'POST'])
def upload_map():
    form = UploadMapForm()
    if form.validate_on_submit():
        logistic_map = LogisticMeshMap()
        logistic_map.mapname = form.mapname.data
        log_map = [s.rstrip().split() for s in form.routes.data.split('\n')]

        if not validate_map_inputs(log_map):
            abort(400, "Invalid Map! Values must be in the format: A B 123")

        logistic_map.routes = json.dumps(log_map)
        db.session.add(logistic_map)
        db.session.commit()
        flash('Map uploaded successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('upload_map.html.j2', title='Upload Map', form=form)


@app.route('/list_maps')
def list_maps():
    logistic_maps = LogisticMeshMap.query.all()

    if len(logistic_maps) > 0:
        return render_template('list_maps.html.j2', title='Map List', logistic_maps=logistic_maps)
    else:
        return render_template('index.html.j2', title='Home App')


@app.route('/find_best_route', methods=['GET', 'POST'])
def find_best_route():
    form = FindBestRouteForm()

    maps_name = db.session.query(LogisticMeshMap.mapname).all()
    form.mapname.choices = [name[0] for name in maps_name]

    if form.validate_on_submit():
        lm_map = LogisticMeshMap.query.filter_by(
            mapname=form.mapname.data).first_or_404()

        origin = form.origin.data
        target = form.destiny.data
        best_path, distance = get_best_route(json.loads(lm_map.routes),
                                             origin=origin, target=target)

        result = dict()
        result['mapname'] = lm_map.mapname
        result['best_route'] = best_path
        result['cost'] = 0.0
        autonomy = float(form.truck_autonomy.data)
        liter_value = float(form.liter_fuel_value.data)
        if distance:
            result['cost'] = (distance / autonomy) * liter_value
            flash('Best route found successfully!', 'info')
        else:
            flash(f'Do not exist a route from {origin} to {target}!', 'info')

        return render_template('show_best_route.html.j2', title='Best Route Result', result=result)
    return render_template('find_best_route.html.j2', title='Find Best Route', form=form)
