from src import *
from models import *
from flask import jsonify, request, Blueprint


makanan = Blueprint('makanan', __name__,
                    url_prefix= '/api/makanan')


##### ----------------------- MAKANAN ----------------------- #####

@makanan.get('/all')
#@jwt_required()
def get_all_makanan():

    #current_user_id = get_jwt_identity()

    # default pagination parameter
    page = request.args.get('page', 1, type= int)
    per_page = request.args.get('per_page', 5, type= int)

    all_makanan = Makanan.query.paginate(page = page, per_page = per_page)
    makanan_dict = []
    for makanan in all_makanan.items:
        data = {
            'id' : makanan.id_makanan,
            'nama' : makanan.nama_makanan ,
            'harga' : makanan.harga,
            'kategori' : makanan.kategori_id#,
            #'user_req' : current_user_id
        }
        makanan_dict.append(data)

    if makanan_dict != []:

        meta = {
            'page' : all_makanan.page,
            'pages' : all_makanan.pages,
            'total_count' : all_makanan.total,
            'prev_page' : all_makanan.prev_num,
            'next_page' : all_makanan.next_num,
            'has_prev' : all_makanan.has_prev,
            'has_next' : all_makanan.has_next
        }

        json_return = jsonify({
            'data' : makanan_dict,
            'meta' : meta
        }), HTTP_200_OK
    else:
        json_return = jsonify({'msg': 'data makanan kosong'}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@makanan.get('/<int:id>')
def get_makanan(id):
    makanan = Makanan.query.filter_by(id_makanan = id).first()
    if makanan:
        json_return = jsonify({
            'id': makanan.id_makanan,
            'nama': makanan.nama_makanan,
            'harga': makanan.harga,
            'kategori': makanan.kategori_id
        }), HTTP_200_OK

    else:
        json_return = jsonify({
            'error': "makanan tidak ada!"
        }), HTTP_404_NOT_FOUND

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@makanan.post('/tambah_makanan')
def tambah_makanan():

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == "application/json":
        data = request.get_json()
        nama = data['nama_makanan']
        harga = data['harga']
        kategori_id = data['id_kategori']

        try:
            makanan_baru = Makanan(
                nama_makanan = nama,
                harga = harga,
                kategori_id = kategori_id
            )

            db.session.add(makanan_baru)
            db.session.commit()

            json_return = jsonify({
                'berhasil' : {
                    'id' : makanan_baru.id_makanan,
                    'nama_makanan' : nama,
                    'harga' : harga,
                    'kategori_id' : kategori_id
                }
            }), HTTP_201_CREATED

        except IntegrityError:
            json_return = jsonify({
                'error': f'Makanan : ({nama}), sudah ada di tabel!'
            }), HTTP_409_CONFLICT

    else:
        json_return = non_json_return(req_check)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return  json_return





@makanan.put('/edit/<int:id>')
@makanan.patch('/edit/<int:id>')
def edit_makanan(id):

    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':
        data = request.get_json()
        nama_baru = data['nama_baru']
        harga_baru = data['harga_baru']
        kategori_id = data['kategori_id']

        makanan_edit = Makanan.query.get(id)
        if makanan_edit:
            try:
                nama_lama = makanan_edit.nama_makanan

                makanan_edit.nama_makanan = nama_baru
                makanan_edit.harga = harga_baru
                makanan_edit.kategori_id = kategori_id

                db.session.commit()
                json_return = jsonify({
                    "berhasil" : {
                        'nama_baru' : nama_baru,
                        'harga_baru' : harga_baru,
                        'kategori_baru' : kategori_id
                    }
                }), HTTP_200_OK

            except IntegrityError:
                json_return = jsonify({
                    'error': f'Makanan : ({nama_baru}), sudah ada di tabel!'
                }), HTTP_409_CONFLICT

        else:
            json_return = jsonify({
                'error' : 'Info Makanan tidak ditemuukan!'
            }), HTTP_404_NOT_FOUND

    else:
        json_return = non_json_return(req_check)

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return





@makanan.delete('/hapus/<int:id>')
def hapus_makanan(id):
    makanan_hapus = Makanan.query.get(id)
    if makanan_hapus:
        db.session.delete(makanan_hapus)
        db.session.commit()

        json_return = jsonify({
            "berhasil" : f"Berhasil hapus makanan : {makanan_hapus.nama_makanan}"
        }), HTTP_200_OK
    else:
        json_return = jsonify({
            "error": f"Info Makanan tidak ditemukan"
        }), HTTP_404_NOT_FOUND

    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    return json_return

