import os
from dotenv import load_dotenv
import json

# Add OpenAI import
import openai


def get_embedding(query):
    # Call OpenAI API to get the embeddings.
    response = openai.Embedding.create(
        input=query,
        # Your deployment name
        engine="OpenAISearch" 
    )
    embeddings = response['data'][0]['embedding']
    print(embeddings)

    return embeddings

 #   else:
 #     raise Exception(f"Failed to get embedding. Status code: {response.status_code}")


def main():   
    try: 
        # Get configuration settings 
        load_dotenv()
       # azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
       # azure_oai_key = os.getenv("AZURE_OAI_KEY")
       # azure_oai_model = os.getenv("AZURE_OAI_MODEL")
      
        # Set OpenAI configuration settings
        openai.api_type = "azure"
        openai.api_base = "https://cloudsa.openai.azure.com/"
        openai.api_version = "2023-03-15-preview"
        openai.api_key = "7b82e680d0be4c0ab072acb2b5b0ff61"
        # Load the JSON dataset
        with open('.venv/OpenAIdatabase.OpenAIcollection.json', 'r') as json_file:
            entity_data = json.load(json_file)
            for entity in entity_data:
                entity_name = entity['entity_name']
                print("entity_name: " + entity_name + "\n")


        # Placeholder for the embeddings
                entity_name_embeddings = get_embedding(entity_name)
        
                entity['entity_name_embeddings'] = entity_name_embeddings

            #print("Summary: " + entity_name_embeddings + "\n")
        
        with open('.venv/OpenAIdatabase.OpenAIcollection.json', 'w') as json_file:

            json.dump(entity_data, json_file, indent=4)
                 
    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()  
  