from datetime import date
import os
import datetime
from flask import Flask, request, render_template, Response, redirect, url_for
import forms
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import flash
from models import Alumnos, Maestros, Pizzas, db
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.route("/")
def principal():
    pizza_form=forms.PizzasForm(request.form)

    return render_template("prueba.html", form=pizza_form)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    nom=""
    apaterno=""
    correo=""
    alum_form=forms.UserForm(request.form)
    if request.method == "POST" and alum_form.validate():
        nom = alum_form.nombre.data
        correo = alum_form.email.data
        apaterno = alum_form.apaterno.data
        mensaje = "Bienvenido: {}".format(nom)
        flash(mensaje)
        print("nombre: {}".format(nom))
        print("correo: {}".format(correo))
        print("apaterno: {}".format(apaterno))
    return render_template("alumnos.html", form=alum_form, nom=nom, apaterno=apaterno,correo=correo)

@app.route("/index", methods=["GET", "POST"])
def index():
    alum_form=forms.UserForm2(request.form)
    if request.method=="POST":
        alum=Alumnos(nombre=alum_form.nombre.data, 
                     apaterno=alum_form.apaterno.data,
                     email=alum_form.email.data)
        #insert into alumnos values()
        db.session.add(alum)
        db.session.commit()
    return render_template("index.html", form=alum_form)

@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABCompleto():
    alum_form=forms.UserForm2(request.form)
    alumno=Alumnos.query.all()
    
    return render_template("ABC_Completo.html", alumno=alumno)


@app.route("/indexMaestros", methods=["GET", "POST"])
def indexMaestros():
    mae_form=forms.UserForm3(request.form)
    if request.method=="POST":
        alum=Maestros(nombre=mae_form.nombre.data, 
                     apaterno=mae_form.apaterno.data,
                     email=mae_form.email.data,
                     telefono=mae_form.telefono.data,
                     materia=mae_form.materia.data)
        #insert into alumnos values()
        db.session.add(alum)
        db.session.commit()
    return render_template("indexMaestros.html", form=mae_form)

@app.route("/ABC_CompletoMaetros", methods=["GET", "POST"])
def ABCompletoMaetros():
    mae_form=forms.UserForm3(request.form)
    profesor=Maestros.query.all()
    
    return render_template("ABC_CompletoMaetros.html", profesor=profesor)


@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    subTotal = 0.0
    nombre = ""
    tamaño = ""
    numPizzas = 0
    ingredientes = []
    pizzas_form = forms.PizzasForm(request.form)
    
    if request.method == "POST" and pizzas_form.validate():
        nombre = pizzas_form.nombre.data
        tamaño = pizzas_form.tamanioPizza.data
        numPizzas = pizzas_form.numPizzas.data
        ingredientes_seleccionados = []
        if 'registrar' in request.form:
            if pizzas_form.jamon.data:
                ingredientes_seleccionados.append("Jamon")
            if pizzas_form.champinion.data:
                ingredientes_seleccionados.append("Champiñones")
            if pizzas_form.pina.data:
                ingredientes_seleccionados.append("Piña")

            subTotal = calcular_subtotal(tamaño, numPizzas, ingredientes_seleccionados)

            guardar_pedido(tamaño, ingredientes_seleccionados, numPizzas, subTotal)

            with open("pedidos.txt", "r",  encoding="utf-8") as file:
                pedidos = file.readlines()
            pedidos_formateados = []
            for dato in pedidos:
                partes = dato.strip().split(", ")
                pedido = {}
                for parte in partes:
                    if ": " in parte:
                        clave, valor = parte.split(": ", 1)
                    else:
                        clave = parte.split(":")[0]
                        valor = parte.split(":", 1)[1].strip() if len(parte.split(":")) > 1 else ""
                    if clave == "Ingredientes":
                        if valor:
                            if 'Ingredientes' not in pedido:
                                pedido['Ingredientes'] = []
                            ingredientes = valor.split(", ")
                            pedido['Ingredientes'].extend(ingredientes)
                    else:
                        pedido[clave] = valor
                pedidos_formateados.append(pedido)
            totalBD = 0.0
            with open("pedidos.txt", "r", encoding="utf-8") as file:
                pedidos = file.readlines()

            for pedido in pedidos:
                partes = pedido.strip().split(", ")
                for parte in partes:
                    if "Subtotal: " in parte:
                        subtotal = float(parte.split(": ")[1])
                        totalBD += subtotal

            return render_template("pizzas.html", form=pizzas_form, sub=subTotal, p=pedidos_formateados, nombre=nombre, total=totalBD)
        elif 'eliminar' in request.form:
                id = int(request.form['eliminar'])
                with open("pedidos.txt", "r", encoding="utf-8") as file:
                    lineas = file.readlines()

                with open("pedidos.txt", "w", encoding="utf-8") as file:
                    for linea in lineas:
                        partes = linea.strip().split(", ")
                        for parte in partes:
                            if "id: " in parte:
                                pedido_id = int(parte.split(": ")[1])
                                if pedido_id == id:
                                    break
                        else:
                            file.write(linea)
                with open("pedidos.txt", "r",  encoding="utf-8") as file:
                    pedidos = file.readlines()
                if len(pedidos) != 0:
                    pedidos_formateados = []
                    for dato in pedidos:
                        partes = dato.strip().split(", ")
                        pedido = {}
                        for parte in partes:
                            if ": " in parte:
                                clave, valor = parte.split(": ", 1)
                            else:
                                clave = parte.split(":")[0]
                                valor = parte.split(":", 1)[1].strip() if len(parte.split(":")) > 1 else ""
                            if clave == "Ingredientes":
                                if valor:
                                    if 'Ingredientes' not in pedido:
                                        pedido['Ingredientes'] = []
                                    ingredientes = valor.split(", ")
                                    pedido['Ingredientes'].extend(ingredientes)
                            else:
                                pedido[clave] = valor
                        pedidos_formateados.append(pedido)
                        totalBD = 0.0
                        with open("pedidos.txt", "r", encoding="utf-8") as file:
                            pedidos = file.readlines()

                        for pedido in pedidos:
                            partes = pedido.strip().split(", ")
                            for parte in partes:
                                if "Subtotal: " in parte:
                                    subtotal = float(parte.split(": ")[1])
                                    totalBD += subtotal
                    return render_template("pizzas.html", form=pizzas_form, sub=subTotal, p=pedidos_formateados, nombre=nombre, total=totalBD)
                else:
                    return  render_template("pizzas.html", form=pizzas_form, sub=subTotal, nombre=nombre)
        elif 'insertar' in request.form:
            pizzas_form = forms.PizzasForm(request.form)
            totalBD = 0.0
            with open("pedidos.txt", "r", encoding="utf-8") as file:
                pedidos = file.readlines()

            for pedido in pedidos:
                partes = pedido.strip().split(", ")
                for parte in partes:
                    if "Subtotal: " in parte:
                        subtotal = float(parte.split(": ")[1])
                        totalBD += subtotal
            alum = Pizzas(nombre=pizzas_form.nombre.data,
                            direccion=pizzas_form.direccion.data,
                            telefono=pizzas_form.telefono.data,
                            total=totalBD,
                            fecha_venta=pizzas_form.fecha_venta.data)

            db.session.add(alum)
            db.session.commit()
            os.remove("pedidos.txt")
    
        elif 'obtenerTotalMes' in request.form:
            fecha_hoy = datetime.datetime.now()
            v = Pizzas.query.all()
            pizzas_form = forms.PizzasForm(request.form)
            nombre_mes = pizzas_form.buscar.data
            total_mes = 0.0
            total_dia = 0.0
            usuarios = []
            mes = ""
            for venta in v:
                if venta.fecha_venta.strftime("%B") == "January":
                    mes = "Enero"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "February":
                    mes = "Febrero"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "March":
                    mes = "Marzo"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "April":
                    mes = "Abril"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "May":
                    mes = "Mayo"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "June":
                    mes = "Junio"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "July":
                    mes = "Julio"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "August":
                    mes = "Agosto"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "September":
                    mes = "Septiembre"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "October":
                    mes = "Octubre"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "November":
                    mes = "Noviembre"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%B") == "December":
                    mes = "Diciembre"
                    if mes == nombre_mes:
                        total_mes+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)

            return render_template("pizzas.html", form=pizzas_form, total_mes=total_mes, usuarios=usuarios)   

        elif 'obtenerTotalDia' in request.form:
            fecha_hoy = datetime.datetime.now()
            v = Pizzas.query.all()
            usuarios = []
            pizzas_form = forms.PizzasForm(request.form)
            nombre_dia = pizzas_form.buscar.data
            total_mes = 0.0
            total_dia = 0.0
            dia = ""
            usuarios = []
            for venta in v:
                if venta.fecha_venta.strftime("%A") == "Monday":
                    dia = "Lunes"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%A") == "Tuesday":
                    dia = "Martes"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%A") == "Wednesday":
                    dia = "Miercoles"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%A") == "Thursday":
                    dia = "Jueves"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario + "\n")
                if venta.fecha_venta.strftime("%A") == "Friday":
                    dia = "Viernes"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%A") == "Saturday":
                    dia = "Sabado"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)
                if venta.fecha_venta.strftime("%A") == "Sunday":
                    dia = "Domingo"
                    if dia == nombre_dia:
                        total_dia+=venta.total
                        usuario = venta.nombre + " " + "$"+str(venta.total)
                        usuarios.append(usuario)

                
            return render_template("pizzas.html", form=pizzas_form, total_dia=total_dia, usuarios=usuarios)   

    return render_template("pizzas.html", form=pizzas_form)


def calcular_subtotal(tamaño, numPizzas, ingredientes):
    costo_tamaño = {"Chica": 40, "Mediana": 80, "Grande": 120}
    costo_ingredientes = 0
    for ingrediente in ingredientes:
        costo_ingredientes += 10
    costo_total = (costo_tamaño[tamaño] + costo_ingredientes) * numPizzas
    return costo_total

contador_pedidos = 0

def guardar_pedido(tamaño, ingredientes, numPizzas, subTotal):
    global contador_pedidos
    contador_pedidos += 1
    with open("pedidos.txt", "a", encoding="utf-8") as file:
        ingredientes_str = " y ".join(ingredientes) if ingredientes else ""
        file.write(f"id: {contador_pedidos}, Tamanio: {tamaño}, Ingredientes: {ingredientes_str}, Numero de Pizzas: {numPizzas}, Subtotal: {subTotal}\n")


@app.route('/eliminar_pedido/<int:id>', methods=['GET', 'POST'])
def eliminar_pedido(id):
    with open("pedidos.txt", "r", encoding="utf-8") as file:
        lineas = file.readlines()

    with open("pedidos.txt", "w", encoding="utf-8") as file:
        for linea in lineas:
            partes = linea.strip().split(", ")
            for parte in partes:
                if "id: " in parte:
                    pedido_id = int(parte.split(": ")[1])
                    if pedido_id == id:
                        break
            else:
                file.write(linea)

    return redirect(url_for('pizzas'))



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()


