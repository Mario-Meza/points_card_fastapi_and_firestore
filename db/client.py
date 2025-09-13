from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import firebase_admin
import os

load_dotenv()
ADMIN_CREDENTIALS = os.getenv("ADMIN_CREDENTIALS")

def close_firebase():
    """
    Permite limpiar las conexiones de la base de datos inicializadas.
    :return No retorna nada:
    """
    if firebase_admin._apps:
        firebase_admin.delete_app(firebase_admin.get_app())
        print("Firestore connection closed")

def get_database():
    """
    Inicializa Firebase y devuelve un cliente de Firestore.
    Solo se inicializa una vez por conexion.
    :return: firestore.client() - El cliente de Firestore para
    hacer operaciones CRUD en Firebase
    """
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(ADMIN_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            print("Database initialized")
    except Exception as e:
        print("The connection could not be established")

    return firestore.client()