from flask import Flask, request, jsonify
import pymysql
import os
import requests  # Para realizar llamadas al módulo Notas de Venta

app = Flask(__name__)

# Configuración de la base de datos
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# URL del módulo Notas de Venta
NOTAS_VENTA_URL = "http://localhost:5001"

db = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    db=db_name
)

# CRUD de Clientes
@app.route('/clientes', methods=['POST'])
def crear_cliente():
    data = request.json
    if not data.get('Razon_Social') or not data.get('Correo_Electronico'):
        return jsonify({'error': 'Razon Social y Correo Electrónico son requeridos'}), 400
    cursor = db.cursor()
    consulta = """
        INSERT INTO Clientes (Razon_Social, Nombre_Comercial, Correo_Electronico)
        VALUES (%s, %s, %s)
    """
    cursor.execute(consulta, (data['Razon_Social'], data.get('Nombre_Comercial'), data['Correo_Electronico']))
    db.commit()
    return jsonify({'mensaje': 'Cliente creado exitosamente'}), 201

@app.route('/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    cursor = db.cursor(pymysql.cursors.DictCursor)
    consulta = "SELECT * FROM Clientes WHERE ID = %s"
    cursor.execute(consulta, (id,))
    cliente = cursor.fetchone()
    if cliente:
        return jsonify(cliente), 200
    return jsonify({'error': 'Cliente no encontrado'}), 404

@app.route('/clientes/<int:id>', methods=['PUT'])
def actualizar_cliente(id):
    data = request.json
    cursor = db.cursor()
    consulta = """
        UPDATE Clientes
        SET Razon_Social=%s, Nombre_Comercial=%s, Correo_Electronico=%s
        WHERE ID=%s
    """
    cursor.execute(consulta, (data['Razon_Social'], data['Nombre_Comercial'], data['Correo_Electronico'], id))
    db.commit()
    return jsonify({'mensaje': 'Cliente actualizado exitosamente'}), 200

@app.route('/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cursor = db.cursor()
    consulta = "DELETE FROM Clientes WHERE ID=%s"
    cursor.execute(consulta, (id,))
    db.commit()
    return jsonify({'mensaje': 'Cliente eliminado exitosamente'}), 200

# Nuevo endpoint: Crear cliente y nota de venta
@app.route('/clientes/crear_nota', methods=['POST'])
def crear_nota_cliente():
    data = request.json
    if not data.get('Razon_Social') or not data.get('Correo_Electronico'):
        return jsonify({'error': 'Razon Social y Correo Electrónico son requeridos'}), 400

    # Crear cliente en la base de datos
    cursor = db.cursor()
    consulta = """
        INSERT INTO Clientes (Razon_Social, Nombre_Comercial, Correo_Electronico)
        VALUES (%s, %s, %s)
    """
    cursor.execute(consulta, (data['Razon_Social'], data.get('Nombre_Comercial'), data['Correo_Electronico']))
    cliente_id = cursor.lastrowid
    db.commit()

    # Llamar al módulo Notas de Venta para crear una nota
    nota_payload = {
        "Cliente_ID": cliente_id,
        "Direccion_Facturacion": data.get('Direccion_Facturacion', 'Dirección no especificada'),
        "Direccion_Envio": data.get('Direccion_Envio', 'Dirección no especificada'),
        "Total_Nota": data.get('Total_Nota', 0),
        "Contenido": data.get('Contenido', []),
        "Correo_Electronico": data.get('Correo_Electronico')
    }

    try:
        response = requests.post(f"{NOTAS_VENTA_URL}/notas_venta", json=nota_payload)
        if response.status_code == 201:
            return jsonify({
                'mensaje': 'Cliente y Nota de Venta creados exitosamente',
                'cliente_id': cliente_id,
                'nota_respuesta': response.json()
            }), 201
        else:
            return jsonify({'error': 'Error al crear la nota de venta', 'detalle': response.json()}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
