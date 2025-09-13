from fastapi import APIRouter, HTTPException, status, Query
from db.client import get_database
from typing import Optional
from db.Model.model import Card

router = APIRouter(
    prefix="/api/v1/tarjeta",
    tags=["Card"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_cards(status_filter: Optional[str] = Query(None), telefono_filter: Optional[str] = Query(None)):
    # 1. Get the Firestore client through the get_database() function
    db = get_database()
    # 2. Reference the "tarjetas_lealtad" collection in Firestore
    card_ref = db.collection("tarjetas_lealtad")
    # 3. Apply filters if they exist
    if status_filter:
        card_ref = card_ref.where("status", "==", status_filter)
    if telefono_filter:
        card_ref = card_ref.where("telefono", "==", telefono_filter)
    # 4. Get a "stream()" - an iterator with all the documents from the collection.
    docs = card_ref.stream()
    # 5. Convert each document into a Python dictionary
    #    "doc.to_dict()" returns the document content in "dict" format
    tarjetas = [doc.to_dict() for doc in docs]
    # 6. If no cards are found in the collection, return a 404 error
    if not tarjetas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cards not found"
        )
    # 7. Return the list of found cards in JSON format
    return tarjetas

@router.get("/{doc_id}", status_code=status.HTTP_200_OK)
def get_card_by_document(doc_id: str):
    # 1. Get the Firestore client through the "get_database()" function
    db = get_database()
    # 2. Reference the "tarjetas_lealtad" collection in Firestore
    #    Search for a specific document using the ID received in the path
    card_ref = db.collection("tarjetas_lealtad").document(doc_id)
    # 3. Retrieve the document from Firestore
    docs = card_ref.get()
    # 4. Verify if the document actually exists
    if not docs.exists:
        # If it doesn't exist, raise an HTTP 404 (Not Found) exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    # 5. If it exists, return the document content in JSON format
    return docs.to_dict()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_document(card: Card):
    # 1. Get the Firestore client through the get_database() function
    db = get_database()
    # 2. Try to add the document to Firestore
    try:
        # Desemepaquetamos la tupla (time_stamp, document_reference)
        time_stamp, doc_ref = db.collection("tarjetas_lealtad").add(card.model_dump())
        return {
            "message": "Document created successfully",
            "id": doc_ref.id
        }
    # 2. If it fails, raise an HTTP 500 (Internal Server Error) exception
    except Exception as e:
        print(f"Error creating document {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creatind document"
        )

@router.put("/{doc_id}", status_code=status.HTTP_200_OK)
def update_document(doc_id: str, card: Card):
    # 1. Get the Firestore client through the get_database() function
    db = get_database()
    # 2. Reference the "tarjetas_lealtad" collection in Firestore
    doc_ref = db.collection("tarjetas_lealtad").document(doc_id)
    # 3. Verify if the document exists before updating
    if not doc_ref.get().exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    # 4. Execute the "set()" method to replace the document in the Firestore database
    #    It overwrites the document with the values provided in the dictionary
    doc_ref.set(card.model_dump())
    # 5. Get a snapshot of the updated document from Firestore
    updated_doc = doc_ref.get()
    # 6. Return the updated document in JSON format
    return updated_doc.to_dict()

@router.patch("/{doc_id}", status_code=status.HTTP_200_OK)
def update_partial_document(doc_id: str, card: Card):
    # 1. Get the Firestore client throught the get_database() function
    db = get_database()
    # 2. Create the reference to the collection name and the document
    doc_ref = db.collection("tarjetas_lealtad").document(doc_id)
    # 3. Get a snapshot of the document from Firestore to verify if it exists
    doc = doc_ref.get()
    # 4. Verify if the document snapshot exists in the database
    if not doc.exists:
        # If it doesn't exist, raise a 404 Not Found error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    # 5. Convert the "card" object from the "Card" model into a Python dictionary
    updated_data = card.model_dump(exclude_unset=True)
    # 6. Verify if the client sent data to update the document
    if not updated_data:
        # If no data was sent to update, return a 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar"
        )
    # 7. Execute the "update()" method to update the document in the Firestore database
    #    It updates the fields in the document with the values provided in the "updated_data" dictionary
    doc_ref.update(updated_data)
    # 8. Get the updated document from Firestore again
    updated_doc = doc_ref.get()
    # 9. Return the updated document in JSON format
    return updated_doc.to_dict()

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: str):
    # 1. Get the Firestore client with the get_database() method
    db = get_database()
    # 2. Reference the "tarjetas_lealtad" collection in Firestore
    doc_ref = db.collection("tarjetas_lealtad").document(doc_id)
    # 3. Verify if the document exists
    if not doc_ref.get().exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found"
        )
    # 4. Delete the document from Firestore
    doc_ref.delete()
    # 5. Do not return any value
    return None









