
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired

class formularioI(FlaskForm):
    documento = StringField("Documento identidad", validators=[DataRequired(message="No dejar vacío este campo...")])
    nombre = StringField("Nombre")
    lugardesde = SelectField("lugardesde", choices=[("Bogota"), ("Medellin"), ("Cali"), ("Barranquilla"), ("Cartagena")])
    hasta = SelectField("hasta", choices=[("Barranquilla"), ("Medellin"), ("Cali"), ("Bogota"), ("Cartagena")])
    salida = DateField("Fecha de salida")
    regreso = DateField("Fecha de regreso")
    cantidadpasajeros = StringField("Cantidad de pasajeros a volar")

    botonCrear = SubmitField("botonCrear", render_kw={"onmouseover": "guardar()"})
    botonEliminar = SubmitField("botonEliminar", render_kw={"onmouseover": "eliminar()"})
    botonActualizar = SubmitField("botonActualizar", render_kw={"onmouseover": "actualizar()"})
    botonVisualizar = SubmitField("Visualizar Reservas", render_kw={"onmouseover": "visualizar()"})