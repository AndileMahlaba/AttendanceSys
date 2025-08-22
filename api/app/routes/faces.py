from flask import Blueprint, request, jsonify

faces_bp = Blueprint('faces', __name__)

@faces_bp.route('/enroll', methods=['POST'])
def enroll_face():
    try:
        data = request.get_json()
        # Add face enrollment logic here
        return jsonify({'message': 'Face enrolled successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@faces_bp.route('/')
def get_faces():
    try:
        # Return empty array for now
        return jsonify({'faces': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
