import firebase_admin
from firebase_admin import credentials, firestore
import time

print("--- test firebase connection ---")

try:
    # 1. 初始化 Firebase Admin SDK
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase App init success")

    # 2. 尝试写入一条数据
    doc_ref = db.collection('test_connection').document('test_doc')
    print("prepare to send message...")

    # .set() 是一个会发起网络请求的操作，如果这里卡住，问题就复现了
    doc_ref.set({
        'message': 'Hello from test script!',
        'timestamp': firestore.SERVER_TIMESTAMP
    })

    print("data write success")

except Exception as e:
    print(f"error: {e}")

print("--- test end ---")