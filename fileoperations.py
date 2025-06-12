import os
import json
import uuid
from datetime import datetime

def practice_file_operations():
    
    # Make a directory, won't throw an error if it exists already
    os.makedirs("test_storage", exist_ok=True)
    
    # Write a file
    test_content = "This is a test document"
    filename = f"doc_{uuid.uuid4()}.txt"
    filepath = os.path.join("test_storage", filename)
    
    with open(filepath, 'w') as f:
        f.write(test_content)
        
    # Read the file back
    with open(filepath, 'r') as f:
        content = f.read()
        print(f"Read content: {content}")
        
    # Get file info
    file_size = os.path.getsize(filepath)
    print(f"File size: {file_size} bytes")

practice_file_operations()

def practice_json_operations():
    # Create a document in key value format
    document = {
        "id": str(uuid.uuid4()),
        "title": "Practice Document",
        "created_at": datetime.now().isoformat(),
        "tags": ["practice", "learning"],
        "metadata": {
            "author": "Johnny",
            "department": "ECM"
        }
    }
    # Save document dict above as JSON
    with open("document_metadata.json", 'w') as f:
        json.dump(document, f, indent=2)
    # Load from JSON to be used as a variable later
    with open("document_metadata.json", 'r') as f:
        loaded_doc = json.load(f)
        print(f"Loaded: {loaded_doc['title']}")
        
practice_json_operations()