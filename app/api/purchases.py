from flask import request, jsonify, current_app
from http import HTTPStatus
from . import api_bp
from app.services import purchase_service

# --- CRUD Endpoints ---
# Este módulo actúa como el "Controller" en una arquitectura MVC.
# Su responsabilidad es manejar la petición HTTP, validar entrada básica
# y delegar la lógica de negocio a la capa de servicios.

@api_bp.route('/purchases', methods=['POST'])
def create_purchase():
    """
    Crea una nueva orden de compra.
    Payload esperado: { "user_id": "...", "items": [...] }
    """
    # Logging: Es vital para la observabilidad en producción.
    current_app.logger.info("Solicitud recibida: Crear Compra")
    
    # Obtener JSON del cuerpo de la petición.
    # request.get_json() retorna None si el mimetype no es application/json o está vacío.
    data = request.get_json()
    
    if not data:
        current_app.logger.warning("Error: Payload JSON faltante")
        return jsonify({'error': 'Payload JSON requerido'}), HTTPStatus.BAD_REQUEST

    user_id = data.get('user_id')
    items = data.get('items')

    # Validación de entrada (Input Validation):
    # Filtramos datos malformados antes de tocar la lógica de negocio.
    if not user_id or not items or not isinstance(items, list):
        current_app.logger.warning(f"Error: Datos inválidos recibidos: {data}")
        return jsonify({'error': 'Faltan campos requeridos: user_id, items (lista)'}), HTTPStatus.BAD_REQUEST

    try:
        # Llamada al Servicio (Business Logic Layer):
        # Desacopla la lógica HTTP de la lógica de dominio.
        purchase = purchase_service.create_purchase(user_id, items)
        current_app.logger.info(f"Éxito: Compra creada {purchase.id} para usuario {user_id}")
        # Retornamos 201 (Created) y el recurso creado.
        return jsonify(purchase.to_dict()), HTTPStatus.CREATED

    except ValueError as ve:
        # Errores de Dominio: Si el servicio levanta un ValueError (ej. regla de negocio violada),
        # lo traducimos a un 400 Bad Request para el cliente.
        current_app.logger.warning(f"Error de validación de negocio: {ve}")
        return jsonify({'error': str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        # Errores Inesperados: Capturamos cualquier otra excepción para evitar que el servidor se caiga (Crash),
        # retornando un 500 genérico y ocultando detalles sensibles al cliente.
        current_app.logger.error(f"Error interno creando compra: {e}", exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), HTTPStatus.INTERNAL_SERVER_ERROR

@api_bp.route('/purchases', methods=['GET'])
def get_all_purchases():
    """
    Obtiene el listado de todas las compras.
    """
    current_app.logger.info("Solicitud recibida: Listar Compras")
    try:
        # Verificación de implementación (Feature Flagging implícito):
        # Útil durante el desarrollo iterativo para no romper endpoints incompletos.
        if hasattr(purchase_service, 'get_all_purchases'):
            purchases = purchase_service.get_all_purchases()
            # Serialización: Convertimos objetos de dominio a diccionarios/JSON.
            return jsonify([p.to_dict() for p in purchases]), HTTPStatus.OK
        else:
            # 501 Not Implemented: El servidor reconoce el método pero no puede cumplirlo.
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
            # 404 Not Found: Estándar cuando el recurso específico no existe.
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