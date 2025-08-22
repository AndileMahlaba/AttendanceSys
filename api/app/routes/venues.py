from flask import Blueprint, request, jsonify
from ..models import Venue

venues_bp = Blueprint('venues', __name__)

@venues_bp.route('/', methods=['GET'])
def get_venues():
    try:
        venues = Venue.get_all()
        return jsonify({'venues': venues})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@venues_bp.route('/', methods=['POST'])
def create_venue():
    try:
        data = request.get_json()
        # Add venue creation logic here
        return jsonify({'message': 'Venue created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
