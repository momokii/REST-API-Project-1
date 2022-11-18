from src import *
from models import *
from flask import request, jsonify, Blueprint



user = Blueprint('user', __name__,
                 url_prefix= '/api/user')


base_path_docs = './docs/user'


##### ----------------------- USER ----------------------- #####



@user.post('/get_user')
@swag_from(f'{base_path_docs}/user.yaml')
def get_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:

            data = request.get_json()
            username = data['username']
            password = data['password']

            user = User.query.filter_by(username = username).first()
            if user:
                if user.check_password(password):
                    akun = {
                            'username': username,
                            'status_login': 'berhasil',
                            'token' : user.password_hash
                    }
                    json_return = jsonify(akun), HTTP_200_OK

                else:
                    json_return = jsonify(status_login = 'gagal'), HTTP_401_UNAUTHORIZED
            else:
                json_return = jsonify(status_login = 'gagal'), HTTP_401_UNAUTHORIZED

        except KeyError:
            json_return = non_json_requested()

    else:
        json_return = non_json_return(check_req)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return


@user.post('/tambah_user')
@swag_from(f'{base_path_docs}/user_tambah.yaml')
def tambah_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:
            data = request.get_json()
            tambah_akun = User(
                username=data['username'],
                password=data['password']
            )

            db.session.add(tambah_akun)
            db.session.commit()

            json_return = jsonify(berhasil=f'Berhasil tambahkan akun username : {data["username"]}'), HTTP_201_CREATED

        except IntegrityError:
            json_return = jsonify(error = f'username : ({data["username"]}) sudah ada'), HTTP_409_CONFLICT

        except KeyError:
            json_return = non_json_requested()

    else:
        json_return = non_json_return(check_req)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return



@user.post('/hapus_user')
@swag_from(f'{base_path_docs}/user_delete.yaml')
def hapus_user():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        try:
            data = request.get_json()
            username = data['username']
            password = data['password']

            user = User.query.filter_by(username=username).first()
            if user:
                if user.check_password(password):
                    db.session.delete(user)
                    db.session.commit()
                    json_return = jsonify(berhasil = f"Berhasil hapus akun dengan username {username}"), HTTP_200_OK

                else:
                    json_return = jsonify(error='username/pass salah, hapus gagal'), HTTP_401_UNAUTHORIZED
            else:
                json_return = jsonify(error='data tidak ditemukan, hapus gagal'), HTTP_401_UNAUTHORIZED

        except KeyError:
            json_return = non_json_requested()

    else:
        json_return = non_json_return(check_req)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return



### ----------------------------------------------------------------------- ###
### ---------------- TAMBAHAN CONTOH PAKE JWT/ TOKEN ---------------------- ###
### ----------------------------------------------------------------------- ###

@user.post('/get_user_jwt')
def get_user_jwt():
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



@user.get('/me')
@jwt_required()
def user_info():
    id_user = get_jwt_identity() # sudah bentuk id tadi dimasukan

    user = User.query.get(id_user)

    return jsonify({'user': user.username}), HTTP_202_ACCEPTED


@user.get('/token/refresh')
@jwt_required(refresh= True) # -> header tambahan, hanya terima refresh token
def refresh_user_token():
    id = get_jwt_identity()
    # buat access token
    access = create_access_token(id)

    return jsonify({'access' : access}), HTTP_200_OK

