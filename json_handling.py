from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# Return JSON response
@app.route('/api/status', methods=['GET'])
def get_status():
    status_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ECM Document Engine"
    }
    # jsonify() converts Python dict to JSON response
    return jsonify(status_data)

# Receive JSON data
@app.route('/api/document', methods=['POST'])
def create_document_metadata():
    # Get JSON data from request
    data = request.json
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    
    document = {
        "id": str(uuid.uuid4()),
        "title": data.get("title", "Untitled Document"),
        "created_at": datetime.now().isoformat(),
        "author": data.get("author", "Unknown"),
        "tags": data.get("tags", [])
    }
    
    return jsonify({
        "message": "Document metadata created",
        "document": document
    }), 201  # 201 = Created

if __name__ == '__main__':
    app.run(debug=True, port=8080)