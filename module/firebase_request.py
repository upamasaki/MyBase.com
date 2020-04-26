import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import pprint
import sys
import os


sys.path.append(os.path.dirname(__file__))
cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), 'kangaroo-flask-v1-firebase-adminsdk-wircc-de33c01ffc.json'))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kangaroo-flask-v1.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

def insert_item(item_dict):
    # databaseにデータを追加する
    item_dict['users_ref'].child(item_dict['item_name']).set({
        'user_name': item_dict['user_name'],
        'item_name': item_dict['item_name'],
        'item_usage': item_dict['item_usage'],
        'item_img_url': item_dict['item_img_url']
        })

if __name__ == "__main__":

    ##databaseに初期データを追加する

    item_dict = {}
    item_dict['users_ref'] = db.reference('/items')
    item_dict['user_name'] = 'tani'
    item_dict['item_name'] = 'Cat_handkerchief'
    item_dict['item_usage'] = 'Its a cat handkerchief'

    item_dict['user_name'] = 'tani'
    item_dict['item_name'] = 'Dog_handkerchief'
    item_dict['item_usage'] = 'Its a dog handkerchief'
    insert_item(item_dict)

    item_dict['user_name'] = 'tani'
    item_dict['item_name'] = 'Bird_handkerchief'
    item_dict['item_usage'] = 'Its a bird handkerchief'
    insert_item(item_dict)

    item_dict['user_name'] = 'tani'
    item_dict['item_name'] = 'rabbit_handkerchief'
    item_dict['item_usage'] = 'Its a rabbit handkerchief'
    insert_item(item_dict)

    pprint.pprint(item_dict['users_ref'].get())
    #select_sample()
