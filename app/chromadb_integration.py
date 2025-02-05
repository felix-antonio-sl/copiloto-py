import os
import chromadb
from chromadb.config import Settings

# Directorio de persistencia para ChromaDB
persist_directory = "db/chroma"
os.makedirs(persist_directory, exist_ok=True)

# Inicializar el cliente de ChromaDB
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=persist_directory
))

# Obtener o crear la colección para conversaciones
collection = client.get_or_create_collection(name="conversations")


def add_message(conversation_id, user_message, bot_response):
    """Agrega un mensaje al vector store de ChromaDB.

    conversation_id: ID de la conversación.
    user_message: Mensaje enviado por el usuario.
    bot_response: Respuesta generada por el bot.

    Nota: Se utiliza un embedding dummy (vector de 768 dimensiones con ceros). En una implementación real, 
    se debe reemplazar por un modelo de embeddings que convierta el mensaje a un vector numérico.
    """
    # Crear un embedding dummy (vector de 768 dimensiones con ceros)
    dummy_embedding = [0.0] * 768
    
    # Preparar el documento que contiene el mensaje del usuario y la respuesta del bot
    document = f"User: {user_message}\nBot: {bot_response}"
    
    # Agregar el documento a la colección
    collection.add(
        ids=[str(conversation_id)],
        documents=[document],
        embeddings=[dummy_embedding],
        metadatas=[{'conversation_id': conversation_id}]
    ) 