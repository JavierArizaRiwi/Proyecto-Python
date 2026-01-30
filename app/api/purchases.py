from flask import request, jsonify, current_app
from . import api_bp
from app.services import purchase_service

@api_bp.route('/purchases', methods=['POST'])
def create_purchase():
    """
    Crea una nueva orden de compra.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Payload JSON requerido'}), 400

    user_id = data.get('user_id')
    items = data.get('items')

    # Validación de entrada
    if not user_id or not items or not isinstance(items, list):
        return jsonify({'error': 'Faltan campos requeridos: user_id, items (lista)'}), 400

    try:
        purchase = purchase_service.create_purchase(user_id, items)
        
        current_app.logger.info(f"Compra creada exitosamente: {purchase.id} por usuario {user_id}")
        
        return jsonify(purchase.to_dict()), 201

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error interno creando compra: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/purchases/<purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    """
    Obtiene el detalle de una compra por ID.
    """
    purchase = purchase_service.get_purchase_by_id(purchase_id)
    
    if not purchase:
        current_app.logger.warning(f"Compra no encontrada: {purchase_id}")
        return jsonify({'error': 'Compra no encontrada'}), 404
        
    return jsonify(purchase.to_dict()), 200