from flask import request, jsonify, current_app
from . import api_bp
from app.services import purchase_service

# --- CRUD Endpoints ---

@api_bp.route('/purchases', methods=['POST'])
def create_purchase():
    """
    Crea una nueva orden de compra.
    Payload esperado: { "user_id": "...", "items": [...] }
    """
    current_app.logger.info("Solicitud recibida: Crear Compra")
    data = request.get_json()
    
    if not data:
        current_app.logger.warning("Error: Payload JSON faltante")
        return jsonify({'error': 'Payload JSON requerido'}), 400

    user_id = data.get('user_id')
    items = data.get('items')

    # Validación básica de entrada
    if not user_id or not items or not isinstance(items, list):
        current_app.logger.warning(f"Error: Datos inválidos recibidos: {data}")
        return jsonify({'error': 'Faltan campos requeridos: user_id, items (lista)'}), 400

    try:
        purchase = purchase_service.create_purchase(user_id, items)
        current_app.logger.info(f"Éxito: Compra creada {purchase.id} para usuario {user_id}")
        return jsonify(purchase.to_dict()), 201

    except ValueError as ve:
        current_app.logger.warning(f"Error de validación de negocio: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error interno creando compra: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/purchases', methods=['GET'])
def get_all_purchases():
    """
    Obtiene el listado de todas las compras.
    """
    current_app.logger.info("Solicitud recibida: Listar Compras")
    try:
        # Verificamos si el servicio tiene el método implementado
        if hasattr(purchase_service, 'get_all_purchases'):
            purchases = purchase_service.get_all_purchases()
            return jsonify([p.to_dict() for p in purchases]), 200
        else:
            # Mock temporal si no existe el servicio
            return jsonify({'message': 'Endpoint listo, falta implementar purchase_service.get_all_purchases()'}), 501
    except Exception as e:
        current_app.logger.error(f"Error listando compras: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/purchases/<purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    """
    Obtiene el detalle de una compra por ID.
    """
    current_app.logger.info(f"Solicitud recibida: Obtener Compra {purchase_id}")
    try:
        purchase = purchase_service.get_purchase_by_id(purchase_id)
        
        if not purchase:
            current_app.logger.warning(f"Error: Compra no encontrada {purchase_id}")
            return jsonify({'error': 'Compra no encontrada'}), 404
            
        return jsonify(purchase.to_dict()), 200
    except Exception as e:
        current_app.logger.error(f"Error obteniendo compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/purchases/<purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    """
    Actualiza una compra existente.
    """
    current_app.logger.info(f"Solicitud recibida: Actualizar Compra {purchase_id}")
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Payload JSON requerido'}), 400

    try:
        if hasattr(purchase_service, 'update_purchase'):
            purchase = purchase_service.update_purchase(purchase_id, data)
            if not purchase:
                return jsonify({'error': 'Compra no encontrada'}), 404
            return jsonify(purchase.to_dict()), 200
        else:
            return jsonify({'message': 'Falta implementar purchase_service.update_purchase()'}), 501
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Error actualizando compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/purchases/<purchase_id>', methods=['DELETE'])
def delete_purchase(purchase_id):
    """
    Elimina una compra por ID.
    """
    current_app.logger.info(f"Solicitud recibida: Eliminar Compra {purchase_id}")
    try:
        if hasattr(purchase_service, 'delete_purchase'):
            success = purchase_service.delete_purchase(purchase_id)
            if not success:
                return jsonify({'error': 'Compra no encontrada'}), 404
            return jsonify({'message': 'Compra eliminada correctamente'}), 200
        else:
            return jsonify({'message': 'Falta implementar purchase_service.delete_purchase()'}), 501
    except Exception as e:
        current_app.logger.error(f"Error eliminando compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500