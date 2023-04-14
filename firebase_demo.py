import asyncio

import firebase_admin
from firebase_admin import credentials, db, firestore_async

# config = {
#   "apiKey": "AIzaSyDzUhEfzSBYcRMKJKmXJe87bSRP5gsVCxg",
#   "authDomain": "getarounduvt.firebaseapp.com",
#   "projectId": "getarounduvt",
#   "storageBucket": "getarounduvt.appspot.com",
#   "messagingSenderId": "870420901218",
#   "appId": "1:870420901218:web:3880d98aa151a7572f503b"
# }


async def main():
    cred = credentials.Certificate('./serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://getarounduvt-default-rtdb.europe-west1.firebasedatabase.app'
    })

    # databaseURL
    # ref = db.reference('users')
    # print(ref.get())

    # Firestore
    firestore_db = firestore_async.client()
    ref = firestore_db.collection('users').stream()
    async for doc in ref:
        print(f"{doc.id} => {doc.to_dict()}")

if __name__ == '__main__':
    asyncio.run(main())
