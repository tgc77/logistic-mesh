from flask import render_template
from app import bp, db


@bp.errorhandler(400)
def abort_error(error):
    return render_template('400.html.j2', error=error), 400


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html.j2'), 404


@bp.errorhandler(409)
def conflict_error(error):
    return render_template('409.html.j2', error=error), 409


@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html.j2'), 500
