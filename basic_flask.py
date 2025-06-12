from flask import Flask, request

app = Flask(__name__)

@app.route('/api/test', methods=['GET'])
def hello_world():
    return "Hello, ECM Platform Engineering"

# GET request - read data
@app.route('/api/test', methods=['GET'])
def get_test():
    return {"message": "GET request - Reading data", "method": "GET"}

@app.route('/api/test', methods=['PUT']) 
def put_test():
    return {"message": "PUT request - Updating data", "method": "PUT"}

# POST request - create new data
@app.route('/api/test', methods=['POST'])
def post_test():
    return {"message": "POST request - Creating data", "method": "POST"}

# DELETE request - remove data
@app.route('/api/test', methods=['DELETE'])
def delete_test():
    return {"message": "DELETE request - Deleting data", "method": "DELETE"}

if __name__ == '__main__':
    app.run(debug=True, port=8080)