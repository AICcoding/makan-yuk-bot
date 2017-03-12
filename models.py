from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pedagang(db.Model):
    __tablename__ = 'pedagang'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    alamat = db.Column(db.String(255))

    def __repr__(self):
        return '<Pedagang (%s, %s) >' % (self.nama, self.alamat)