from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, IntegerField, EmailField, BooleanField
from wtforms import validators

class UserForm(Form):
    nombre = StringField("nombre", [validators.DataRequired(message="el campo es requerido"), 
                         validators.Length(min=4, max=10, message="ingresa nombre valido")])
    email = EmailField("correo", [validators.Email(message="valor no valido")])
    apaterno = StringField("apaterno")
    edad=IntegerField('edad', [validators.number_range(min=1, max=20, message="valor no valido")])

class UserForm2(Form):
    id =IntegerField("id")
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=4,max=10,message='ingresa nombre valido')])
    apaterno = StringField("apaterno")
    email=EmailField('correo',[validators.Email(message='Ingrese un correo valido')])
    
class UserForm3(Form):
    id =IntegerField("id")
    nombre = StringField("nombre",[validators.DataRequired(message='el campo es requerido'), validators.Length(min=4,max=10,message='ingresa nombre valido')])
    apaterno = StringField("apaterno")
    email=EmailField('correo',[validators.Email(message='Ingrese un correo valido')])
    telefono = StringField("telefono")
    materia = StringField("materia")
    

class PizzasForm(Form):
    id = IntegerField("id")
    nombre = StringField("nombre", [validators.DataRequired(message='el campo es requerido'), validators.Length(min=4, max=10, message='ingresa nombre valido')])
    direccion = StringField("direccion", [validators.DataRequired(message='el campo es requerido'), validators.Length(min=4, max=10, message='ingresa direccion valido')])
    telefono = IntegerField("telefono", [validators.number_range(min=1, max=1000000000, message="valor no valido")])
    tamanioPizza = RadioField(choices=[('Chica', 'Chica'), ('Mediana', 'Mediana'), ('Grande', 'Grande')])
    jamon = BooleanField("Jamon")
    pina = BooleanField("Piña")
    champinion = BooleanField("Champiñon")
    numPizzas = IntegerField('Núm de pizzas', [validators.number_range(min=1, max=1000, message="valor no valido")])

