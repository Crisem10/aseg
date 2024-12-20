from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de conexión a MySQL
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='boletos_avion'
    )
    return connection

# Ruta principal: lista de boletos
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = '''
        SELECT boletos.id AS boleto_id, clientes.nombre, clientes.apellido, 
               vuelos.origen, vuelos.destino, vuelos.fecha_salida, vuelos.fecha_llegada, vuelos.precio, boletos.estado
        FROM boletos
        INNER JOIN clientes ON boletos.cliente_id = clientes.id
        INNER JOIN vuelos ON boletos.vuelo_id = vuelos.id
    '''
    cursor.execute(query)
    boletos = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', boletos=boletos)

# Ruta para agregar clientes
@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        telefono = request.form['telefono']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO clientes (nombre, apellido, correo, telefono)
            VALUES (%s, %s, %s, %s)
        ''', (nombre, apellido, correo, telefono))
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('index'))
    
    return render_template('agregar_cliente.html')

# Ruta para agregar vuelos
@app.route('/agregar_vuelo', methods=['GET', 'POST'])
def agregar_vuelo():
    if request.method == 'POST':
        origen = request.form['origen']
        destino = request.form['destino']
        fecha_salida = request.form['fecha_salida']
        fecha_llegada = request.form['fecha_llegada']
        precio = request.form['precio']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO vuelos (origen, destino, fecha_salida, fecha_llegada, precio)
            VALUES (%s, %s, %s, %s, %s)
        ''', (origen, destino, fecha_salida, fecha_llegada, precio))
        connection.commit()
        cursor.close()
        connection.close()
        
        return redirect(url_for('index'))
    
    return render_template('agregar_vuelo.html')

# Ruta para comprar boletos
@app.route('/comprar_boleto', methods=['GET', 'POST'])
def comprar_boleto():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Obtener clientes y vuelos para el formulario
    cursor.execute('SELECT id, CONCAT(nombre, " ", apellido) AS nombre_completo FROM clientes')
    clientes = cursor.fetchall()
    
    cursor.execute('SELECT id, CONCAT(origen, " -> ", destino) AS vuelo_info FROM vuelos')
    vuelos = cursor.fetchall()
    
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        vuelo_id = request.form['vuelo_id']
        
        cursor.execute('''
            INSERT INTO boletos (cliente_id, vuelo_id)
            VALUES (%s, %s)
        ''', (cliente_id, vuelo_id))
        connection.commit()
        
        cursor.close()
        connection.close()
        return redirect(url_for('index'))
    
    cursor.close()
    connection.close()
    return render_template('comprar_boleto.html', clientes=clientes, vuelos=vuelos)

if __name__ == '__main__':
    app.run(debug=True)
