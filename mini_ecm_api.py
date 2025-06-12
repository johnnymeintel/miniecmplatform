# mini_ecm_api.py - Complete mini ECM platform
from flask import Flask, request, jsonify, send_file
import os
import uuid
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
STORAGE_DIR = "ecm_storage"
METADATA_DIR = "ecm_metadata"
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# Health check endpoint
@app.route('/health')
def health_check():
    """Platform health check"""
    return jsonify({
        "status": "healthy",
        "service": "Mini ECM Platform",
        "timestamp": datetime.now().isoformat()
    })

# Create document
@app.route('/api/documents', methods=['POST'])
def upload_document():
    """Upload document with metadata"""
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Secure filename
        original_filename = secure_filename(file.filename)
        file_extension = os.path.splitext(original_filename)[1]
        safe_filename = f"{doc_id}{file_extension}"
        
        # Save file
        filepath = os.path.join(STORAGE_DIR, safe_filename)
        file.save(filepath)
        
        # Create metadata
        metadata = {
            "id": doc_id,
            "title": request.form.get('title', original_filename),
            "original_filename": original_filename,
            "safe_filename": safe_filename,
            "file_size": os.path.getsize(filepath),
            "created_at": datetime.now().isoformat(),
            "author": request.form.get('author', 'API User'),
            "tags": request.form.get('tags', '').split(',') if request.form.get('tags') else []
        }
        
        # Save metadata
        metadata_file = os.path.join(METADATA_DIR, f"{doc_id}.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return jsonify({
            "message": "Document uploaded successfully",
            "document": metadata
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# List documents
@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents with optional search"""
    
    search_query = request.args.get('q', '').lower()
    documents = []
    
    # Load all metadata files
    for filename in os.listdir(METADATA_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(METADATA_DIR, filename), 'r') as f:
                doc_metadata = json.load(f)
                
                # Simple search filter
                if search_query:
                    title_match = search_query in doc_metadata['title'].lower()
                    author_match = search_query in doc_metadata['author'].lower()
                    if not (title_match or author_match):
                        continue
                
                documents.append(doc_metadata)
    
    # Sort by creation date (newest first)
    documents.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify({
        "documents": documents,
        "count": len(documents),
        "search_query": search_query
    })

# Download document
@app.route('/api/documents/<doc_id>/download')
def download_document(doc_id):
    """Download document file"""
    
    # Get metadata
    metadata_file = os.path.join(METADATA_DIR, f"{doc_id}.json")
    if not os.path.exists(metadata_file):
        return jsonify({"error": "Document not found"}), 404
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Get file
    filepath = os.path.join(STORAGE_DIR, metadata['safe_filename'])
    if not os.path.exists(filepath):
        return jsonify({"error": "Document file not found"}), 404
    
    return send_file(
        filepath,
        as_attachment=True,
        download_name=metadata['original_filename']
    )

@app.route('/api/documents/<doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document and its metadata"""
    
    # Paths to the content and metadata files
    metadata_file_path = os.path.join(METADATA_DIR, f"{doc_id}.json")
    
    # Check if metadata exists first
    if not os.path.exists(metadata_file_path):
        return jsonify({"error": "Document not found"}), 404

    try:
        # Load metadata to get the safe_filename
        with open(metadata_file_path, 'r') as f:
            metadata = json.load(f)
        
        content_file_path = os.path.join(STORAGE_DIR, metadata['safe_filename'])

        # Delete the content file if it exists
        if os.path.exists(content_file_path):
            os.remove(content_file_path)
        else:
            # Optionally log if content file is missing but metadata exists
            print(f"Warning: Content file {content_file_path} not found for metadata {doc_id}. Proceeding with metadata deletion.")

        # Delete the metadata file
        os.remove(metadata_file_path)
        
        return jsonify({
            "message": f"Document {doc_id} and its metadata deleted successfully"
        }), 200 # 200 OK or 204 No Content are typical for successful DELETE

    except OSError as e:
        # Catch OS-level errors like permission denied or file in use
        return jsonify({"error": f"Failed to delete files: {str(e)}"}), 500
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error during deletion: {e}")
        return jsonify({"error": "Internal server error during deletion"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)