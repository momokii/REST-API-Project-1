from src import *
from models import *
from flask import jsonify, request, Blueprint



kategori = Blueprint('kategori', __name__,
                     url_prefix='/api/kategori')

base_path_docs = "./docs/kategori"


##### ----------------------- KATEGORI ----------------------- #####

@kategori.get('/all')
@swag_from(f'{base_path_docs}/kategori.yaml')
def get_all_kategori():

    all_kategori = Kategori.query.all()
    kategori_dict = []
    for kategori in all_kategori:
        data = {
            'id' : kategori.id_kategori,
            'nama_kategori' : kategori.nama_kategori
        }
        kategori_dict.append(data)

    if kategori_dict != []:
        json_return = jsonify(kategori_dict), HTTP_200_OK
    else:
        json_return = jsonify({'msg' : 'data kategori kosong'}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@kategori.get('/<int:id>')
@swag_from(f'{base_path_docs}/kategori_get.yaml')
def get_kategori(id):

    kategori = Kategori.query.filter_by(id_kategori = id).first()
    if kategori:
        return_json = jsonify({
            "id": kategori.id_kategori,
            'nama_kategori': kategori.nama_kategori
        }), HTTP_200_OK

    else:
        return_json = jsonify({
            'error': "data kategori tidak ditemukan"
        }), HTTP_404_NOT_FOUND

    return_json[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return return_json





@kategori.post('/tambah')
@swag_from(f'{base_path_docs}/kategori_tambah.yaml')
def tambah_kategori():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        try:
            nama_kategori = request.get_json()['nama_kategori']
            kategori = Kategori(
                nama_kategori = nama_kategori
            )
            db.session.add(kategori)
            db.session.commit()

            json_return = jsonify({
                "berhasil" : {
                    'id_kategori' : kategori.id_kategori,
                    'nama_kategori' : nama_kategori
                }
            }), HTTP_201_CREATED

        except IntegrityError:
                json_return = jsonify({
                    "error": f"tambah kategori : ({nama_kategori}), kemungkinan kategori tersebut sudah ada"
                }), HTTP_409_CONFLICT

        except KeyError:
                json_return = non_json_requested()

    else:
        json_return = non_json_return(check_req)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@kategori.put('/edit/<int:id>')
@kategori.patch('/edit/<int:id>')
@swag_from(f'{base_path_docs}/kategori_edit.yaml')
def edit_kategori(id):

    request.access_control_request_headers
    check = request.headers.get('Content-Type')
    if check == 'application/json':

        kategori_edit = Kategori.query.get(id)
        if kategori_edit:

            try:
                data_edit = request.get_json()
                nama_baru = data_edit['nama']
                nama_lama = kategori_edit.nama_kategori

                kategori_edit.nama_kategori = nama_baru
                db.session.commit()

                json_return = jsonify({
                    "berhasil" : {
                        'nama_lama' : nama_lama,
                        'nama_baru' : nama_baru
                    }
                }), HTTP_200_OK

            except IntegrityError:
                json_return = jsonify({
                    'error' : f'nama baru : {nama_baru} sudah ada dalam tabel'
                }), HTTP_409_CONFLICT

            except KeyError:
                json_return = non_json_requested()

        else:
            json_return = jsonify({
                'error': 'id tidak ditemukan'
            }), HTTP_404_NOT_FOUND

    else:
        json_return = non_json_return(check)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@kategori.delete('/hapus/<int:id>')
@swag_from(f'{base_path_docs}/kategori_delete.yaml')
def hapus_kategori(id):

    kategori_hapus = Kategori.query.get(id)
    if kategori_hapus:
        db.session.delete(kategori_hapus)
        db.session.commit()
        json_return = jsonify({
            "Berhasil" : f"Berhasil hapus kategori : { kategori_hapus.nama_kategori }"
        }), HTTP_200_OK

    else:
        json_return = jsonify({
            'error' : 'id tidak ditemukan'
        }), HTTP_404_NOT_FOUND


    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return
