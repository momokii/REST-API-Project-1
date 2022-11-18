from src import *
from models import *
from flask import request, jsonify, Blueprint



user = Blueprint('user', __name__,
                 url_prefix= '/api/user')



##### ----------------------- USER ----------------------- #####



@user.post('/get_user')
def get_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username = username).first()
        if user:
            if user.check_password(password):

                refresh_token = create_refresh_token(user.id)
                access_token = create_access_token(user.id)

                akun = {
                        'username': username,
                        'status_login': 'berhasil',
                        'token_refresh' : refresh_token,
                        'token_access' : access_token
                }
                json_return = jsonify(akun), HTTP_200_OK

            else:
                json_return = jsonify(status_login = 'gagal'), HTTP_401_UNAUTHORIZED
        else:
            json_return = jsonify(status_login = 'gagal'), HTTP_401_UNAUTHORIZED

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@user.post('/tambah_user')
def tambah_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        data = request.get_json()
        tambah_akun = User(
            username = data['username'],
            password = data['password']
        )
        try:
            db.session.add(tambah_akun)
            db.session.commit()

        except IntegrityError:
            json_return = jsonify(Error = f'Gagal Tambah Akun, Username : {data["username"]} sudah ada'), HTTP_409_CONFLICT

        else:
            json_return = jsonify(Berhasil = f'Berhasil tambahkan akun username : {data["username"]}'), HTTP_201_CREATED

        finally:
            json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
            return json_return


@user.post('/hapus_user')
def hapus_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                db.session.delete(user)
                db.session.commit()
                json_return = jsonify(Berhasil = f"Berhasil hapus akun dengan username {username}")

            else:
                json_return = jsonify(Gagal='username/pass salah, hapus gagal')
        else:
            json_return = jsonify(Gagal='username/pass salah, hapus gagal')

    json_return.headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return



@user.get('/me')
@jwt_required()
def user_info():
    id_user = get_jwt_identity() # sudah bentuk id tadi dimasukan

    user = User.query.get(id_user)

    return jsonify({'user': user.username}), HTTP_202_ACCEPTED


@user.get('/token/refresh')
@jwt_required(refresh= True) # -> header tambahan
def refresh_user_token():
    id = get_jwt_identity()
    # buat access token
    access = create_access_token(id)

    return jsonify({'access' : access}), HTTP_200_OK

