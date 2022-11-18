from src import *
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# --------------------------------------------------------------
# ---------------------- DB CONFIGURATION ----------------------
# --------------------------------------------------------------


class Kategori(db.Model):
    __tablename__ = "kategori"
    id_kategori = db.Column(db.Integer, primary_key = True)
    nama_kategori = db.Column(db.String(100), unique = True, nullable = False)


class Makanan(db.Model):
    __tablename = "makanan"
    id_makanan = db.Column(db.Integer, primary_key = True)
    nama_makanan = db.Column(db.String, nullable = False, unique = True)
    harga = db.Column(db.Integer, nullable = False)
    # dependencies
    kategori_id = db.Column(db.Integer, ForeignKey('kategori.id_kategori'))
    #kategori = relationship('Kategori', backref = 'makanan')


class User(db.Model):
    __tablename__ = 'akun'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable =  False, unique = True)
    password_hash = db.Column(db.String(500), nullable = False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password_plain):
        self.password_hash = generate_password_hash(password_plain, salt_length=8)

    def check_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        else:
            return False


db.create_all()
