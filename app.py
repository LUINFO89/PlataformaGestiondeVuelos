import functools
import os
from re import X

from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, current_app, g, make_response
from flask import render_template as render
#import utils
from db import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from formulario import Contactenos,formularioI,formularioC,formularioV,formularioU
import sqlite3
from message import mensajes

app = Flask( __name__ )
app.secret_key = os.urandom( 24 )


@app.route( '/' )
def index():
    if g.user:
        return redirect( url_for( 'send' ) )
    return render_template( 'login.html' )


@app.route( '/register', methods=('GET', 'POST') )
def register():
    if g.user:
        return redirect( url_for( 'send' ) )
    try:  
        if request.method == 'POST':
            name= request.form['nombre']
            username = request.form['username']
            password = request.form['password']
            email = request.form['correo']
            error = None
            db = get_db()
            db.executescript(
                "INSERT INTO usuario   (nombre, usuario,correo,contraseña) VALUES ('%s','%s','%s','%s')"%(name,username,email,generate_password_hash(password))
            )
            db.commit()
            return "usuario guardado exitosamente"
        return  render ('register.html') 
    except:
        return render_template( 'register.html' )


@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
        if g.user:
            return redirect( url_for( 'send' ) )
        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'login.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'login.html' )
    
            user = db.execute(
                'SELECT * FROM usuario WHERE usuario = ? AND contraseña = ?', (username, password)
            ).fetchone()

            if user is None:
                user = db.execute(
                    'SELECT * FROM usuario WHERE usuario = ?', (username,)
                ).fetchone()
                if user is None:
                    error = 'Usuario no existe'
                else:
                    #Validar contraseña hash            
                    store_password = user[4]
                    result = check_password_hash(store_password, password)
                    if result is False:
                        error = 'Contraseña inválida'
                    else:
                        session.clear()
                        session['user_id'] = user[0]
                        resp = make_response( redirect( url_for( 'send' ) ) )
                        resp.set_cookie( 'username', username )
                        return resp
                    flash( error )
            else:
                session.clear()
                session['user_id'] = user[0]
                return redirect( url_for( 'send' ) )
            flash( error )
            close_db()
        return render_template( 'login.html' )
    except Exception as e:
        print(e)
        return render_template( 'login.html' )


@app.route( '/contacto', methods=('GET', 'POST') )
def contacto():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )


def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'login' ) )

        return view( **kwargs )

    return wrapped_view


@app.route( '/downloadpdf', methods=('GET', 'POST') )
# @login_required
def downloadpdf():
    return send_file( "resources/doc.pdf", as_attachment=True )


@app.route( '/downloadimage', methods=('GET', 'POST') )
@login_required
def downloadimage():
    return send_file( "resources/image.png", as_attachment=True )


@app.route( '/send', methods=('GET', 'POST') )
@login_required
def send():
    if g.user:
        return render_template('send.html')

    
    
  


#----------------------------------------INICIO CRUD RESERVAS--------------------------------------#

@app.route('/reservas', methods=["GET", "POST"])
@login_required
def inicio():
    form = formularioI()
    return render_template('reservas.html', form = form)

#---------------------------------------RESERVAS CREAR--------------------------------------------#
@app.route('/reservas/guardar/', methods=["POST"])
def guardar():
        form = formularioI()#Instancia de la clase en formulario.py
        if request.method == "POST":
            docum = form.documento.data#Recupera datos
            nombr = form.nombre.data
            lugar = form.lugardesde.data
            hasta = form.hasta.data
            salida = form.salida.data
            regreso = form.regreso.data
            cantidad = form.cantidadpasajeros.data

            with sqlite3.connect("database.db") as conn:#Manejador de contexto ->conexion
                cur = conn.cursor()#manipula la db
                #se va a usar el PreparedStatement
                #Acciones
                cur.execute(
                    "INSERT INTO reserva (documento, nombre, lugardesde, hasta, salida, regreso, cantidad) VALUES (?,?,?,?,?,?,?)", 
                (docum, nombr, lugar, hasta, salida,regreso, cantidad)
                )
                conn.commit()#Confirmación de inserción de datos :)
                return "<script> alert('Reserva creada y guardada' ); </script>"
        return "No se pudo guardar T_T"    

'''@app.route('/vista', methods=["GET","POST"])
@login_required

def vista():
     return render ("reservas.html")'''

@app.route('/reservas/visualizar/', methods=["POST"])
def visualizar():
    form = formularioI()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:#conexion
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("SELECT * FROM reserva WHERE Documento = ?", [docum])
            row = cur.fetchone()
            if row is None:
                return "No se encontró el registro en la base de datos...... :'( "
            return render_template("vistaReserva.html", row = row)
    return "Error"

#-----------------------------------------------RESERVAS ELIMINAR ------------------------------------#
@app.route('/reservas/eliminar/', methods=["POST"])
def eliminar():
   
    form = formularioI()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("DELETE FROM reserva WHERE Documento = ?", [docum])
            if conn.total_changes > 0:
                return "<script> alert('Reserva BORRADA ' ); </script>"
            return render_template("reservas.html")
    return "Error"

#---------------------------------------RESERVAS ACTUALIZAR ----------------------------------------#

@app.route('/reservas/actualizar/', methods=["POST"])
def actualizar():
    
    form = formularioI()
    if request.method == "POST":
        docum = form.documento.data
        nombr = form.nombre.data
        lugar = form.lugardesde.data
        hasta = form.hasta.data
        salida = form.salida.data
        regreso = form.regreso.data
        cantidad = form.cantidadpasajeros.data
        idreserva = form.idreserva.data
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE  reserva SET nombre = ?, lugardesde = ?, hasta = ?, salida = ?,regreso = ?,cantidad = ?WHERE Documento = ?;",
             [docum, nombr, lugar, hasta, salida,regreso, cantidad]
             )
            conn.commit()#Confirmación de inserción de datos :)
            return "¡Datos actualizados exitosamente ^v^!"
    return "No se pudo actualizar T_T"



#---------------------------------------- COMENTARIOS
@app.route('/comentarios', methods=["GET", "POST"])
@login_required
def inicioC():
    form = formularioC()
    return render('comentarios.html', form = form)
#----------------------------------------CREAR CRUD COMENTARIOS ------------------------------------------------#
@app.route('/comentarios/guardar/', methods=["GET","POST"])
def guardarC():
        form = formularioC()#Instancia de la clase en formulario.py
        if request.method == "POST":#Recupera datos
            docum = form.documento.data# docu es vuelos
            nombre = form.nombre.data
            lugar = form.lugar.data
            mensaje = form.mensaje.data
            

            with sqlite3.connect("database.db") as conn:#Manejador de contexto ->conexion
                cur = conn.cursor()#manipula la db
                #se va a usar el PreparedStatement
                #Acciones
                cur.execute(
                    "INSERT INTO comentarios (ID, NOMBREVIAJERO, LUGARDEVUELO, MENSAJE) VALUES (?,?,?,?)", 
                (docum, nombre, lugar, mensaje)
                )
                conn.commit()#Confirmación de inserción de datos :)
                return "<h1>¡Comentario guardado exitosamente!</h1>"
        return "No se pudo guardar T_T"    

#----------------------------------------EDITAR CRUD COMENTARIOS ------------------------------------------------#
@app.route('/comentarios/actualizar/', methods=["POST"])
def actualizarC():
    
    form = formularioC()#Instancia de la clase en formulario.py
    if request.method == "POST":
        docum = form.documento.data# docu es vuelos
        nombre = form.nombre.data
        lugar = form.lugar.data
        mensaje = form.mensaje.data
        
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE comentarios SET NOMBREVIAJERO = ?, LUGARDEVUELO = ?, MENSAJE = ? WHERE ID = ?",
             [docum, nombre, lugar, mensaje]
             )
            conn.commit()#Confirmación de inserción de datos :)
            return "¡Datos actualizados exitosamente ^v^!"
    return "No se pudo actualizar T_T"
#----------------------------------------VISUALIZAR CRUD COMENTARIO ---------------------------------------------#
@app.route('/comentarios/eliminar/', methods=["POST"])
def eliminarC():
   
    form = formularioC()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("DELETE FROM comentarios WHERE ID = ?", [docum])
            if conn.total_changes > 0:
                return "Comentario  borrado ^v^"
            return render_template("comentarios.html")
    return "Error"

@app.route('/comentarios/visualizar/', methods=["POST"])
def visualizarC():
    form = formularioC()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:#conexion
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("SELECT * FROM comentarios WHERE ID = ?", [docum])
            row = cur.fetchone()
            if row is None:
                return "No se encontró el registro en la base de datos...... :'( "
            return render_template("vistacomentarios.html", row = row)
    return "Error"


#---------------------------------------- VUELOS

@app.route('/vuelos', methods=["GET", "POST"])
@login_required
def inicioV():
    form = formularioV()
    return render('vuelos.html', form = form)
#----------------------------------------CREAR CRUD VUELOS

@app.route('/vuelos/guardar/', methods=["GET","POST"])
def guardarv():
        form = formularioV()#Instancia de la clase en formulario.py
        if request.method == "POST":#Recupera datos
            docum = form.documento.data# docu es vuelos
            aerolinea = form.aerolinea.data
            hora = form.hora.data
            destino = form.destino.data
            horadestino = form.horadestino.data
            observacion = form.observacion.data
            piloto = form.piloto.data
            capacidad = form.capacidad.data

            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO vuelos (VUELO, AEROLINEA, HORA, DESTINO, HORADESTINO, OBSERVACION, PILOTO, CAPACIDAD) VALUES (?,?,?,?,?,?,?,?)", 
                (docum, aerolinea, hora, destino, horadestino,observacion, piloto,capacidad)
                )
                conn.commit()
                return "¡Datos de Vuelo guardados exitosamente!</h1>"
        return "No se pudo guardar T_T"    

#----------------------------------------VISUALIZAR CRUD VUELOS --------------------------------------------#
@app.route('/vuelos/visualizar/', methods=["POST"])
def visualizarV():
    form = formularioV()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:#conexion
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("SELECT * FROM vuelos WHERE VUELO = ?", [docum])
            row = cur.fetchone()
            if row is None:
                return "No se encontró el registro en la base de datos...... :'( "
            return render_template("vistaVuelos.html", row = row)
    return "Error"
#----------------------------------------EDITAR CRUD VUELOS ------------------------------------------------#
@app.route('/vuelo/actualizar/', methods=["POST"])
def actualizarV():
    
    form = formularioV()#Instancia de la clase en formulario.py
    if request.method == "POST":
        docum = form.documento.data# docu es vuelos
        aerolinea = form.aerolinea.data
        hora = form.hora.data
        destino = form.destino.data
        horadestino = form.horadestino.data
        observacion = form.observacion.data
        piloto = form.piloto.data
        capacidad = form.capacidad.data
        with sqlite3.connect("database.db") as conn:#Manejador de contexto ->conexion
            cur = conn.cursor()#manipula la db
            #se va a usar el PreparedStatement
            #Acciones
            cur.execute(
                "UPDATE vuelos SET AEROLINEA = ?, HORA = ?, DESTINO = ?, HORADESTINO = ?,OBSERVACION = ?,PILOTO = ?,CAPACIDAD = ? WHERE VUELO = ?;",
             [docum, aerolinea, hora, destino, horadestino, observacion, piloto,capacidad]
             )
            conn.commit()#Confirmación de inserción de datos :)
            return "¡Datos actualizados exitosamente ^v^!"
    return "No se pudo actualizar T_T"
#----------------------------------------BORRAR CRUD VUELOS ------------------------------------------------#
@app.route('/vuelos/eliminar/', methods=["POST"])
def eliminarV():
   
    form = formularioV()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("DELETE FROM vuelos WHERE VUELO = ?", [docum])
            if conn.total_changes > 0:
                return "Vuelo borrado ^v^"
            return render_template("vuelos.html")
    return "Error"


#-----------------------------------------FIN CRUD VUELOS-------------------------------------------------#





@app.route('/user', methods=["GET", "POST"])
@login_required
def inicioU():
    form = formularioU()
    return render('usuarios.html', form = form)
#----------------------------------------EDITAR USUSARIO  ---------------------------------------------#

@app.route('/usuarios/guardar/', methods=["GET","POST"])
def guardarU():
        form = formularioU()#Instancia de la clase en formulario.py
        if request.method == "POST":#Recupera datos
            docum = form.documento.data# docu es vuelos
            nombre = form.nombre.data
            usuario = form.usuario.data
            contraseña = form.contraseña.data
            correo = form.correo.data
            nacimiento = form.nacimiento.data
            telefono = form.telefono.data
            direccion = form.direccion.data
            rol = form.rol.data

            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO usuario (nombre, usuario, correo, contraseña,nacimiento,telefono,direccion,rol,documento) VALUES (?,?,?,?,?,?,?,?,?)", 
                (nombre,usuario,correo, generate_password_hash(contraseña),nacimiento,telefono,direccion,rol,docum)
                )
                conn.commit()
                return "<h1>Usuario Credado exitosamente!</h1>"
        return "No se pudo guardar T_T"   

#----------------------------------------VER USUSARIO  ---------------------------------------------#
@app.route('/usuarios/actualizar/', methods=["POST"])
def actualizarU():
    
    form = formularioU()#Instancia de la clase en formulario.py
    if request.method == "POST":
        docum = form.documento.data# docu es vuelos
        nombre = form.nombre.data
        usuario = form.usuario.data
        contraseña = form.contraseña.data
        correo = form.correo.data
        nacimiento = form.nacimiento.data
        telefono = form.telefono.data
        direccion = form.direccion.data
        rol = form.rol.data
        
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE usuario SET nombre = ?, usuario = ?, contraseña = ?,correo = ? ,nacimiento = ? ,telefono = ? ,direccion = ? ,rol = ?  WHERE documento = ?",
            (nombre,usuario,generate_password_hash(contraseña),correo,nacimiento,telefono,direccion,rol,docum)
             )
            conn.commit()#Confirmación de inserción de datos :)
            return "¡Datos actualizados exitosamente ^v^!"
    return "No se pudo actualizar T_T"
#------------------------------

@app.route('/usuarios/visualizar/', methods=["POST"])
def visualizarU():
    form = formularioU()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:#conexion
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE documento = ?", [docum])
            row = cur.fetchone()
            if row is None:
                return "No se encontró el registro en la base de datos...... :'( "
            return render_template("vistausuarios.html", row = row)
    return "Error"

#----------------------------------------BORRAR CRUD VUELOS ------------------------------------------------#
@app.route('/usuarios/eliminar/', methods=["POST"])
def eliminarU():
   
    form = formularioU()
    if request.method == "POST":
        docum = form.documento.data
        with sqlite3.connect("database.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()#manipula la db
            cur.execute("DELETE FROM usuario WHERE documento = ?", [docum])
            if conn.total_changes > 0:
                return "Usuario borrado ^v^"
            return render_template("usuarios.html")
    return "Error"

@app.before_request
def load_logged_in_user():
    user_id = session.get( 'user_id' )

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuario WHERE id = ?', (user_id,)
        ).fetchone()



@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'login' ) )


if __name__ == '__main__':
    app.run()
