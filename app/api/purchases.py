from flask import request, jsonify, current_app
from http import HTTPStatus
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
        return jsonify({'error': 'Payload JSON requerido'}), HTTPStatus.BAD_REQUEST

    user_id = data.get('user_id')
    items = data.get('items')

    # Validación básica de entrada
    if not user_id or not items or not isinstance(items, list):
        current_app.logger.warning(f"Error: Datos inválidos recibidos: {data}")
        return jsonify({'error': 'Faltan campos requeridos: user_id, items (lista)'}), HTTPStatus.BAD_REQUEST

    try:
        purchase = purchase_service.create_purchase(user_id, items)
        current_app.logger.info(f"Éxito: Compra creada {purchase.id} para usuario {user_id}")
        return jsonify(purchase.to_dict()), HTTPStatus.CREATED

    except ValueError as ve:
        current_app.logger.warning(f"Error de validación de negocio: {ve}")
        return jsonify({'error': str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        current_app.logger.error(f"Error interno creando compra: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

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
            return jsonify([p.to_dict() for p in purchases]), HTTPStatus.OK
        else:
            # Mock temporal si no existe el servicio
            return jsonify({'message': 'Endpoint listo, falta implementar purchase_service.get_all_purchases()'}), HTTPStatus.NOT_IMPLEMENTED
    except Exception as e:
        current_app.logger.error(f"Error listando compras: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

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
            return jsonify({'error': 'Compra no encontrada'}), HTTPStatus.NOT_FOUND
            
        return jsonify(purchase.to_dict()), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(f"Error obteniendo compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

@api_bp.route('/purchases/<purchase_id>', methods=['PUT'])
def update_purchase(purchase_id):
    """
    Actualiza una compra existente.
    """
    current_app.logger.info(f"Solicitud recibida: Actualizar Compra {purchase_id}")
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Payload JSON requerido'}), HTTPStatus.BAD_REQUEST

    try:
        if hasattr(purchase_service, 'update_purchase'):
            purchase = purchase_service.update_purchase(purchase_id, data)
            if not purchase:
                return jsonify({'error': 'Compra no encontrada'}), HTTPStatus.NOT_FOUND
            return jsonify(purchase.to_dict()), HTTPStatus.OK
        else:
            return jsonify({'message': 'Falta implementar purchase_service.update_purchase()'}), HTTPStatus.NOT_IMPLEMENTED
    except ValueError as ve:
        return jsonify({'error': str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        current_app.logger.error(f"Error actualizando compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

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
                return jsonify({'error': 'Compra no encontrada'}), HTTPStatus.NOT_FOUND
            return jsonify({'message': 'Compra eliminada correctamente'}), HTTPStatus.OK
        else:
            return jsonify({'message': 'Falta implementar purchase_service.delete_purchase()'}), HTTPStatus.NOT_IMPLEMENTED
    except Exception as e:
        current_app.logger.error(f"Error eliminando compra {purchase_id}: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR