import requests
import pymongo
import os
from dotenv import load_dotenv
import json
# Add OpenAI import
import openai
def get_embedding(query):
    # Call OpenAI API to get the embeddings.
    response = openai.Embedding.create(
        input=query,
        engine="OpenAISearch"
    )
    embeddings = response['data'][0]['embedding']
    return embeddings
    
def find_similar_documents(embedding):
    url = "mongodb+srv://myAtlasDBUser:myAtlasDBUser@myatlasclusteredu.8injg8q.mongodb.net/"  # Replace with your MongoDB url.
    try:
        client = pymongo.MongoClient(url)
        print("Connected to MongoDB")
        db = client["Reviews"]
        collection = db["wineReviews"]
        # Query for similar documents.
        documents = list(
            collection.aggregate(
                [
                    {
                        "$search": {
                            "index": "entity_name_vector_index",
                            "knnBeta": {
                                "vector": embedding,
                                "path": "entity_name_embeddings",
                                "k": 1,
                            },
                        }
                    },
                    {"$project": {"_id": 0, "entity_name": 1, "event_sentiment": 1, "signal_sentiment": 1}},
                ]
            )
        )
        return documents
    finally:
        client.close()

def main():
    # Configure OpenAI
    load_dotenv()
    #azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
    #azure_oai_key = os.getenv("AZURE_OAI_KEY")
    #azure_oai_model = os.getenv("AZURE_OAI_MODEL")
        
    # Set OpenAI configuration settings
    openai.api_type = "azure"
    openai.api_base = "https://cloudsa.openai.azure.com/"
    openai.api_version = "2023-03-15-preview"
    openai.api_key = "7b82e680d0be4c0ab072acb2b5b0ff61"  # Replace with your OpenAI API key
    
    query = "JPMorgan"  # Replace with your query.
    
    try:
        embedding = get_embedding(query)
        documents = find_similar_documents(embedding)
        for document in documents:
            print(str(document) + "\n")
            print()
    except Exception as err:
        print(err)

if __name__ == '__main__': 
    main()
