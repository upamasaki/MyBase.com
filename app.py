from flask import Flask, render_template
from flask import *
from flask import request

import sys
import os

from module import firebase_request

# fire base 
from firebase_admin import db

# ファイル名をチェックする関数
from werkzeug.utils import secure_filename

# cloudinary
import cloudinary
import cloudinary.uploader
cloudinary.config(
  cloud_name = "aichi-prefectural-university",
  api_key = "884251713832499",
  api_secret = "gVicsVp9HqJhu_Yxf7xxKDGjVTQ"
)

from pprint import pprint

UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

pprint(sys.path)

message = {}
message['page_title'] = 'item-list'


@app.route('/', methods=['GET'])
def index():
  item_dict = {}
  item_dict['users_ref'] = db.reference('/items')

  pprint(item_dict['users_ref'].get())
  message['firebase_get'] = item_dict['users_ref'].get()
  message['page_title'] = 'item-list'

  return render_template('index.html', message=message)

@app.route('/Item_list', methods=['GET'])
def Item_list():

  item_dict = {}
  item_dict['users_ref'] = db.reference('/items')

  pprint(item_dict['users_ref'].get())
  message['firebase_get'] = item_dict['users_ref'].get()
  pprint(message['firebase_get'])
  message['page_title'] = 'item-list'
  return render_template('index.html', message=message)

@app.route('/Exhibition')
def Exhibition():
  message['page_title'] = 'Exhibition'
  return render_template('Exhibition.html', message=message)

@app.route('/RentPage', methods=["GET", "POST"])
def RentPage():
  message['page_title'] = 'RentPage'
  return render_template('RentPage.html', message=message)



@app.route('/IconsPage')
def IconsPage():
  message['page_title'] = 'IconsPage'
  return render_template('IconsPage.html', message=message)

@app.route('/DeliveryPage', methods=["GET", "POST"])
def DeliveryPage():
  message['page_title'] = 'DeliveryPage'
  return render_template('DeliveryPage.html', message=message)

@app.route('/PayPage', methods=["GET", "POST"])
def PayPage():
  message['page_title'] = 'PayPage'
  return render_template('PayPage.html', message=message)

@app.route('/PayCfmPage', methods=["GET", "POST"])
def PayCfmPage():
  message['page_title'] = 'PayCfmPage'
  return render_template('PayCfmPage.html', message=message)

@app.route('/PayCfmPageResult', methods=["GET", "POST"])
def PayCfmPageResult():
  message['page_title'] = 'PayCfmPageResult'
  return render_template('PayCfmPageResult.html', message=message)

@app.route('/ProfilePage', methods=["GET", "POST"])
def ProfilePage():
  message['page_title'] = 'ProfilePage'
  return render_template('ProfilePage.html', message=message)

@app.route('/FavoritePage', methods=["GET", "POST"])
def FavoritePage():
  message['page_title'] = 'FavoritePage'
  return render_template('FavoritePage.html', message=message)

@app.route('/OwnItemPage', methods=["GET", "POST"])
def OwnItemPage():
  message['page_title'] = 'OwnItemPage'
  return render_template('OwnItemPage.html', message=message)

@app.route('/ContactUsPage', methods=["GET", "POST"])
def ContactUsPage():
  message['page_title'] = 'ContactUsPage'
  return render_template('ContactUsPage.html', message=message)

@app.route('/PointPage', methods=["GET", "POST"])
def PointPage():
  message['page_title'] = 'PointPage'
  return render_template('PointPage.html', message=message)

@app.route('/DraftsPage', methods=["GET", "POST"])
def DraftsPage():
  message['page_title'] = 'DraftsPage'
  return render_template('DraftsPage.html', message=message)

@app.route("/login_manager", methods=["POST"])  #追加
def login_manager():
  # ===================================================
  # page init
  message['page_title'] = 'Exhibition'

  # ===================================================
  # debug 
  print("request.form")
  print(request.form) 
  print("request.files")
  print(request.files)


  # ===================================================
  # item image loading
  if 'file' not in request.files:
    print('ファイルがありません')
    return render_template('Exhibition.html', message=message)
  
  # データの取り出し
  file = request.files['file']
  
  # ファイル名がなかった時の処理
  if file.filename == '':
    print('ファイルがありません')
    return render_template('Exhibition.html', message=message)
  
  # ファイルのチェック
  if file and allwed_file(file.filename):
    # 危険な文字を削除（サニタイズ処理）
    filename = secure_filename(file.filename)
    # ファイルの保存
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    # アップロード後のページに転送

    # cloudinary regist
    res = cloudinary.uploader.upload(file=img_path, public_id=filename)
    pprint(res)

    message['item_img_url'] = res['secure_url']

  # ===================================================
  # item databse writing
  item_dict = {}
  item_dict['users_ref'] = db.reference('/items')
  item_dict['user_name'] = request.form['user_name']
  item_dict['item_name'] = request.form['item_name']
  item_dict['item_usage'] = request.form['item_usage']
  item_dict['item_img_url'] = res['secure_url']

  firebase_request.insert_item(item_dict)

  pprint(item_dict['users_ref'].get())

  return render_template('Exhibition.html', message=message)

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':

  app.run(host='0.0.0.0', port=5000, debug=True)
