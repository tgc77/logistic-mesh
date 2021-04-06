from flask import render_template, flash, redirect, url_for, abort
import json
from sqlalchemy import exc
from sqlite3 import IntegrityError as sqlite3IntegrityError
from wtforms.validators import ValidationError

from app import bp, db
from app.forms import UploadMapForm, FindBestRouteForm
from app.models import LogisticMeshMap
from app.logistic_mesh.best_route import get_best_route
from app.utils import validate_map_inputs


@bp.route('/')
@bp.route('/index')
def index():
    return redirect(url_for('app.list_maps'))


@bp.route('/upload_map', methods=['GET', 'POST'])
def upload_map():
    form = UploadMapForm()
    if form.validate_on_submit():
        logistic_map = LogisticMeshMap()
        logistic_map.mapname = form.mapname.data
        log_map = [s.rstrip().split() for s in form.routes.data.split('\n')]

        if not validate_map_inputs(log_map):
            abort(400, "Invalid Map! Values must be in the format:"
                  "<br />A B 12<br />C D 20<br />B D 10")

        logistic_map.routes = json.dumps(log_map)
        db.session.add(logistic_map)

        try:
            db.session.commit()
        except AssertionError:
            db.session.rollback()
            abort(409, "Oops! AssertionError, you may have input with invalid values!")
        except (exc.IntegrityError, sqlite3IntegrityError):
            db.session.rollback()
            abort(409, "Oops! This mapname already exists in the database! "
                  "Choose another one!")
        except Exception:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

        flash('Map uploaded successfully!', 'info')
        return redirect(url_for('app.list_maps'))
    return render_template('upload_map.html.j2', title='Upload Map', form=form)


@bp.route('/list_maps')
def list_maps():
    logistic_maps = LogisticMeshMap.query.all()

    if len(logistic_maps) > 0:
        return render_template('list_maps.html.j2', title='Map List', logistic_maps=logistic_maps)
    else:
        return render_template('index.html.j2', title='Home App')


@bp.route('/find_best_route', methods=['GET', 'POST'])
def find_best_route():
    form = FindBestRouteForm()

    maps_name = db.session.query(LogisticMeshMap.mapname).all()
    form.mapname.choices = [name[0] for name in maps_name]

    if form.validate_on_submit():
        lm_map = LogisticMeshMap.query.filter_by(
            mapname=form.mapname.data).first_or_404()

        origin = form.origin.data.upper()
        target = form.destiny.data.upper()
        best_path, distance = ([], 0.0)
        try:
            best_path, distance = get_best_route(json.loads(lm_map.routes),
                                                 origin=origin, target=target)
        except ValidationError as err:
            abort(400, err)

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
