from app import create_app, db
from app.models import LogisticMeshMap

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Function to enable testing from python shell interface

    Returns:
        [db, LogisticMeshMap]: Database object and model
    """
    return {'db': db, 'LogisticMeshMap': LogisticMeshMap}
