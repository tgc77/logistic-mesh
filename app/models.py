from app import db


class LogisticMeshMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mapname = db.Column(db.String(64), index=True, unique=True)
    routes = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return 'f<LogisticMeshMap {self.mapname}>'
