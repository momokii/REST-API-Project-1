from src import *
from models import *
from makanan import *
from kategori import *
from user import *


### ---------------- GLOBAL ERROR HANDLER ------------------ ###
@app.errorhandler(HTTP_404_NOT_FOUND)
def handler_404(e):
    return jsonify({
        "error" : "404 Error/ Pages Doesnt Exist"
    }), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def handler_405(e):
    return jsonify({
        'error' : '405 Error/ Method digunakan salah!'
    }), HTTP_405_METHOD_NOT_ALLOWED



## ----------- BLUEPRINT REGISTER --------------- ##
app.register_blueprint(user)
app.register_blueprint(makanan)
app.register_blueprint(kategori)



if __name__ == "__main__":
    app.run(debug= True)