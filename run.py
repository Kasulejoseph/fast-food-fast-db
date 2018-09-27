from app import app
from flask import jsonify
from app.api.views import routes
if __name__ == '__main__':
    app.run(debug=True)

@app.errorhandler(405)
def url_not_found(error):
    return jsonify({'error':'Requested method not allowed'}), 405

@app.errorhandler(400)
def invalid_input_error(error):
    return jsonify({'Bad request':'Invalid request'}), 400

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error':'Order not found, check the url'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': "500 error"}), 500