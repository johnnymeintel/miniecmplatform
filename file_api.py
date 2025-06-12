# file_api.py - Combining Flask with file operations
from flask import Flask, request, jsonify
import os
import uuid
import json
from datetime import datetime

app = Flask(__name__)

# Configure storage directory
STORAGE_DIR = "api_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/api/documents', methods=['POST'])
def create_document():
    """Create a document"""
    
    # Get data from request
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Content required"}), 400
    
    # Generate unique document ID
    doc_id = str(uuid.uuid4())
    filename = f"doc_{doc_id}.txt"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    # Create document metadata
    document_metadata = {
        "id": doc_id,
        "title": data.get("title", "Untitled Document"),
        "filename": filename,
        "created_at": datetime.now().isoformat(),
        "author": data.get("author", "API User"),
        "tags": data.get("tags", [])
    }
    
    try:
        # Write file content
        with open(filepath, 'w') as f:
            f.write(data['content'])
        
        # Get file size
        file_size = os.path.getsize(filepath)
        document_metadata['file_size'] = file_size
        
        # Save metadata as JSON
        metadata_file = os.path.join(STORAGE_DIR, f"meta_{doc_id}.json")
        with open(metadata_file, 'w') as f:
            json.dump(document_metadata, f, indent=2)
        
        return jsonify({
            "message": "Document created successfully",
            "document": document_metadata
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    documents = []
    
    # Look for all metadata files
    for filename in os.listdir(STORAGE_DIR):
        if filename.startswith('meta_') and filename.endswith('.json'):
            filepath = os.path.join(STORAGE_DIR, filename)
            with open(filepath, 'r') as f:
                document = json.load(f)
                documents.append(document)
    
    return jsonify({
        "documents": documents,
        "count": len(documents)
    })

@app.route('/api/documents/<doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get specific document content"""
    
    # Find the document file
    filename = f"doc_{doc_id}.txt"
    filepath = os.path.join(STORAGE_DIR, filename)
    
    if not os.path.exists(filepath):
        return jsonify({"error": "Document not found"}), 404
    
    # Read content
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Get metadata
    metadata_file = os.path.join(STORAGE_DIR, f"meta_{doc_id}.json")
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    return jsonify({
        "document": metadata,
        "content": content
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)