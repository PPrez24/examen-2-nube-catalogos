from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Configuración de la base de datos
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
