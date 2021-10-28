from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField,TextAreaField,TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class Contactenos( FlaskForm ):
    nombre = StringField( 'Nombre', validators=[DataRequired( message='No dejar vacío, completar' )] )
    correo = EmailField( 'Correo', validators=[DataRequired( message='No dejar vacío, completar' )] )
    mensaje = StringField( 'Mensaje', validators=[DataRequired( message='No dejar vacío, completar' )] )
    enviar = SubmitField( 'Enviar Mensaje' )

class formularioI(FlaskForm):
    documento = StringField("Numedo de identificacion: ", validators=[DataRequired(message="No dejar vacío este campo...")])
    nombre = StringField("Nombre: ")
    lugardesde = SelectField("Lugar de salida:", choices=[("Bogota"), ("Medellin"), ("Cali"), ("Barranquilla"), ("Cartagena")])
    hasta = SelectField("Lugar de destino: ", choices=[("Barranquilla"), ("Medellin"), ("Cali"), ("Bogota"), ("Cartagena")])
    salida = StringField("Fecha de salida : ")
    regreso = StringField("Fecha de regreso :")
    cantidadpasajeros = StringField("Cantidad de pasajeros a volar : ")

    botonCrear = SubmitField("Crear Reservas", render_kw={"onmouseover": "guardar()"})
    botonEliminar = SubmitField("Eliminar Reservas", render_kw={"onmouseover": "eliminar()"})
    botonActualizar = SubmitField("Actualizar Reservas", render_kw={"onmouseover": "actualizar()"})
    botonVisualizar = SubmitField("Visualizar Reservas", render_kw={"onmouseover": "visualizar()"})

    

class formularioC(FlaskForm):
    documento = StringField("Numero de identificacion del usuario:", validators=[DataRequired(message="No dejar vacío este campo...")])
    nombre = StringField("Nombre:")
    lugar = SelectField("Lugar de Destino:", choices=[("Barranquilla"), ("Bogota"), ("Medellin"), ("Cali"), ("Cartagena")])
    mensaje = TextAreaField("Mensaje , sujerencia o reconocimiento:")
    

    botonCrear = SubmitField("Crear Comentario", render_kw={"onmouseover": "guardarC()"})
    botonEliminar = SubmitField("Eliminar", render_kw={"onmouseover": "eliminarC()"})
    botonActualizar = SubmitField("Actualizar comentario", render_kw={"onmouseover": "actualizarC()"})
    botonVisualizar = SubmitField("Ver ComentarioS ", render_kw={"onmouseover": "visualizarC()"})


class formularioU(FlaskForm):
    documento = StringField("Numero de identificacion del usuario:", validators=[DataRequired(message="No dejar vacío este campo...")])
    nombre = StringField("Nombre:")
    usuario = StringField("Usuario:")
    correo = StringField("Correo:")
    contraseña = PasswordField("Contraseña:")
    nacimiento = SelectField("Lugar de Nacimiento:", choices=[("Barranquilla"), ("Bogota"), ("Medellin"), ("Cali"), ("Cartagena")])
    telefono = TextField("Telefono:")
    direccion = TextField("Direccion:")
    rol = SelectField("Rol:", choices=[("Pasajero"), ("Piloto")])

    botonCrear = SubmitField("botonCrear", render_kw={"onmouseover": "guardarU()"})
    botonEliminar = SubmitField("botonEliminar", render_kw={"onmouseover": "eliminarU()"})
    botonActualizar = SubmitField("botonActualizar", render_kw={"onmouseover": "actualizarU()"})
    botonVisualizar = SubmitField("Ver Usuario ", render_kw={"onmouseover": "visualizarU()"})

class formularioV(FlaskForm):
    documento = StringField("Vuelo o Ticket:", validators=[DataRequired(message="No dejar vacío este campo...")])
    aerolinea = SelectField("Aerolinea:", choices=[("LATAM"), ("AVIANCA"), ("VIVACOLOMBIA"), ("SATENA"), ("VIVAAIR")])
    hora = StringField("Hora:")
    destino  = SelectField("Lugar de destino:", choices=[("Barranquilla"), ("Bogota"), ("Medellin"), ("Cali"), ("Cartagena")])
    horadestino = StringField("Hora Destino:")
    observacion = SelectField("Observación:", choices=[("A tiempo"), ("Retrasado"), ("Aterrizado "), ("Despegado")])
    piloto = StringField("Piloto:")
    capacidad = StringField("Capacidad del avión:")
    idreserva = StringField("Numero de identificacion del usuario:")

    botonCrear = SubmitField("Crear vuelo", render_kw={"onmouseover": "guardarV()"})
    botonEliminar = SubmitField("Eliminar vuelo", render_kw={"onmouseover": "eliminarV()"})
    botonActualizar = SubmitField("Actualizar vuelo", render_kw={"onmouseover": "actualizarV()"})
    botonVisualizar = SubmitField("Ver Vuelos ", render_kw={"onmouseover": "visualizarV()"})