# url_parameters.py - Handling different types of parameters
from flask import Flask, request, jsonify

app = Flask(__name__)

# URL path parameters
@app.route('/api/users/<user_id>')
def get_user(user_id):
    """URL parameter in the path"""
    return jsonify({
        "user_id": user_id,
        "message": f"Retrieved user {user_id}"
    })

# Query parameters  
@app.route('/api/search')
def search_documents():
    """Query parameters: /api/search?q=contract&limit=10"""
    query = request.args.get('q', '')          # Default to empty string
    limit = request.args.get('limit', 10, type=int)  # Default to 10, convert to int
    author = request.args.get('author')        # Optional parameter
    
    return jsonify({
        "query": query,
        "limit": limit, 
        "author": author,
        "message": f"Searching for '{query}' with limit {limit}"
    })

# Multiple URL segments
@app.route('/api/documents/<doc_id>/versions/<version_id>')
def get_document_version(doc_id, version_id):
    """Multiple path parameters"""
    return jsonify({
        "document_id": doc_id,
        "version_id": version_id,
        "message": f"Document {doc_id}, version {version_id}"
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)