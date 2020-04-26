import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pprint
import sys

pprint.pprint(sys.path)

cred = credentials.Certificate('kangaroo-flask-v1-firebase-adminsdk-wircc-de33c01ffc.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://kangaroo-flask-v1.firebaseio.com',
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    }
})

users_ref = db.reference('/items')
def insert_sample():

    users_ref.set({
        'user001': {
            'date_of_birth': 'June 23, 1984',
            'full_name': 'Sazae Isono'
            },
        'user002': {
            'date_of_birth': 'December 9, 1995',
            'full_name': 'Tama Isono'
            }
        })

    # databaseにデータを追加する
    users_ref.child('user003').set({
        'date_of_birth': 'Aug 23, 1980',
        'full_name': 'Masuo Isono'
        })

    ##データを取得する
    print(users_ref.get())

def insert_item(item_dict):
    # databaseにデータを追加する
    item_dict['users_ref'].child(item_dict['item_name']).set({
        'user_name': item_dict['user_name'],
        'item_name': item_dict['item_name'],
        'item_usage': item_dict['item_usage']
        })
    


def select_sample():
    docs = users_ref.get()
    print(docs)
    for doc in docs:
        print(doc)


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