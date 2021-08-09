import psycopg2
from flask import Flask, render_template, request, url_for, redirect
#from flaskext.mysql import MySQL#
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
db = SQLAlchemy(app)
conn = psycopg2.connect(

    host="ec2-52-6-77-239.compute-1.amazonaws.com",
    database="d4jkv2qfinl45h",
    user="xpmzhonxqoudej",
    password="14b6895a1cf3b295acec7f4dd2ee1d4242aaef5a18f170685a953c14ee468678"
)


@app.route("/")

def index():

    return render_template("index.html")

@app.route("/rejilla")
def rejilla_htm():
    return render_template("html_rejilla.html")

@app.route("/formulario")
def formulario_htm():


    conect = conn.cursor()

    conect.execute("select * from productos")

    datos = conect.fetchall()

    print(datos)
    conect.close()

    return render_template("html_formulario.html", lista_productos=datos)

@app.route("/guardar_producto", methods=["POST"])
def guardar_producto():
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    descrip = request.form["descrip"]



    conect = conn.cursor()

    conect.execute("INSERT INTO productos(nombre, precio, descrip) VALUES (%s,%s,%s)",
                  (nombre, precio, descrip))

    conn.commit()

    conect.close()

    # return "Dato insertado "+nombre+" "+precio+" "+descrip

    return redirect("/formulario")


@app.route("/eliminar_producto/<string:id>")
def eliminar_producto(id):


    conect = conn.cursor()

    conect.execute("DELETE FROM productos where id={0}".format(id))
    conn.commit()
    conect.close()

    return redirect("/formulario")


@app.route("/consultar_producto/<id>")
def consultar_producto(id):


    conect = conn.cursor()

    conect.execute("SELECT * FROM productos where id= %s", (id))
    dato=conect.fetchone()
    print(dato)
    conect.close()

    return render_template("/form_editar_producto.html", producto=dato)

@app.route("/editar_producto/<id>", methods=['POST'])
def editar_producto(id):
    nombre = request.form["nombre"]
    descrip = request.form["descrip"]
    precio = request.form["precio"]


    conect = conn.cursor()

    conect.execute("UPDATE productos SET nombre=%s, descrip=%s,  precio=%s WHERE id=%s",
                   (nombre, descrip, precio, id))
    conn.commit()
    conect.close()
    return redirect("/formulario")

@app.route("/bootstrap")
def bootstrap_htm():
    return render_template('/Bootstrap.html')


if __name__== '__main__':
    app.run(port=3000,debug=True)
