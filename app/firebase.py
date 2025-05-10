import os
import firebase_admin
from firebase_admin import credentials, firestore

# Ruta relativa dentro del directorio `app/`
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()
