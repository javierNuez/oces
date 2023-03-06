from http.client import BAD_REQUEST
from locale import normalize
from random import randint
from audioop import add
from datetime import datetime, timedelta
from lib2to3.pytree import convert
from tokenize import Number
from unicodedata import numeric
from flask import Flask, jsonify, session
from flask import render_template, request, redirect, flash
from flask import send_file
import requests
from flaskext.mysql import MySQL
from datetime import date
import json
from datetime import date
from datetime import datetime
import ast

# Día actual
# today = date.today()

# Fecha actual y hora
# now = datetime.now()


app = Flask(__name__)


app.secret_key = "vigoray"
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitiobeta'
mysql.init_app(app)


@app.route('/')
def inicio():

    return render_template('sitio/index.html')

# prueba
# @app.route('/admin/')
# def open():

#    return render_template('admin/index.html')


@app.route('/apms/')
def apms_index():
    return render_template('apms/index.html')


@app.route('/apms/inicio')
def apms_inicio():
    _desde = "2022-01-01"
    _hasta = "9999-12-31"
    usuario = session['hash']
    usuarioEntero = int(usuario)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql = "SELECT * FROM `pedidosaaprobar` WHERE pa_usuario = %s order by id_pedidoa desc;"
    datos = (usuarioEntero)
    cursor.execute(sql, datos)
    pedidosTotales = cursor.fetchall()
    lospedidos = pedidosTotales
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    for i in pedidosDC:
        fecha = i[5].date()
        i[5] = fecha
    conta = 0
    listaFechas = []
    listaValores = []
    for x in pedidosDC:
        llave = x[5]

        valor = x[7]

        if conta == 0:
            listaFechas.append(llave)
            listaValores.append(valor)
            conta = conta+1
        else:
            if llave == pedidosDC[conta-1][5]:
                valorViejo = listaValores.pop()
                valorViejo = int(valorViejo)

                valor = int(valor)

                listaValores.append(valorViejo+valor)
            else:
                listaFechas.append(llave)
                listaValores.append(valor)
            conta = conta+1
    graficoLista = list(zip(listaFechas, listaValores))

    return render_template('/apms/inicio.html', lospedidos=graficoLista, desde=_desde, hasta=_hasta)


@app.route('/admin/inicio')
def admin_inicio():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `pedidosaaprobar` order by id_pedidoa desc;")
    lospedidos = cursor.fetchall()
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    for i in pedidosDC:
        fecha = i[5].date()
        i[5] = fecha
    conta = 0
    listaFechas = []
    listaValores = []
    for x in pedidosDC:
        llave = x[5]

        valor = x[7]

        if conta == 0:
            listaFechas.append(llave)
            listaValores.append(valor)
            conta = conta+1
        else:
            if llave == pedidosDC[conta-1][5]:
                valorViejo = listaValores.pop()
                valorViejo = int(valorViejo)

                valor = int(valor)

                listaValores.append(valorViejo+valor)
            else:
                listaFechas.append(llave)
                listaValores.append(valor)
            conta = conta+1
    graficoLista = list(zip(listaFechas, listaValores))

    return render_template('admin/inicio.html', lospedidos=graficoLista)


@app.route('/admin/mensaje')
def admin_mensaje():
    return render_template('admin/mensaje.html')


@app.route('/sup/inicio')
def sup_inicio():
    _desde = "2022-01-01"
    _hasta = "9999-12-31"
    usuario = session['hash']

    usuarioEntero = int(usuario)
    listaRegionMetro = [1200, 1300, 1400, 1500]
    listaRegionNacional = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000]
    desdeU = usuarioEntero
    if desdeU in listaRegionMetro:
        hastaU = usuarioEntero + 99
    elif desdeU in listaRegionNacional:
        hastaU = usuarioEntero + 999

    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql = "SELECT * FROM `pedidosaaprobar` WHERE pa_usuario BETWEEN %s AND %s order by id_pedidoa desc;"
    datos = (desdeU, hastaU)
    cursor.execute(sql, datos)
    pedidosTotales = cursor.fetchall()
    lospedidos = pedidosTotales
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    for i in pedidosDC:
        fecha = i[5].date()
        i[5] = fecha
    conta = 0
    listaFechas = []
    listaValores = []
    for x in pedidosDC:
        llave = x[5]

        valor = x[7]

        if conta == 0:
            listaFechas.append(llave)
            listaValores.append(valor)
            conta = conta+1
        else:
            if llave == pedidosDC[conta-1][5]:
                valorViejo = listaValores.pop()
                valorViejo = int(valorViejo)

                valor = int(valor)

                listaValores.append(valorViejo+valor)
            else:
                listaFechas.append(llave)
                listaValores.append(valor)
            conta = conta+1
    graficoLista = list(zip(listaFechas, listaValores))
    return render_template('/sup/inicio.html', lospedidos=graficoLista, usuario=usuario, desde=_desde, hasta=_hasta)


@ app.route('/admin/conformarOferta00')
def cargaOferta():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('admin/conformarOferta00.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/admin/conformarEspecial00')
def cargaEspecial():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('admin/conformarEspecial00.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/sup/conformarEspecial00')
def supCargaEspecial():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM ofertas where o_especial='si' ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('sup/conformarEspecial00.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/admin/conformarOferta01/drogueria/', methods=['POST'])
def ofer01():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('admin/conformarOferta02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/admin/conformarEspecial01/drogueria/', methods=['POST'])
def especial01():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('admin/conformarEspecial02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/apms/conformarEspecial00')
def apmsCargaEspecial():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM ofertas where o_especial='si' ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('apms/conformarEspecial00.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/sup/conformarEspecial01/drogueria/', methods=['POST'])
def supEspecial01():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/conformarEspecial02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/apms/conformarEspecial01/drogueria/', methods=['POST'])
def apmsEspecial01():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('apms/conformarEspecial02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/admin/conformarOferta02/cliente/', methods=['POST'])
def ofer02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/admin/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('admin/conformarOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/apms/conformarOferta02/cliente/', methods=['POST'])
def apmsofer02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/admin/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('apms/conformarOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/admin/conformarEspecial02/cliente/', methods=['POST'])
def especial02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/admin/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('admin/conformarEspecial04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/sup/conformarEspecial02/cliente/', methods=['POST'])
def supEspecial02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/sup/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('sup/conformarEspecial04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/apms/conformarEspecial02/cliente/', methods=['POST'])
def apmsEspecial02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/apms/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('apms/conformarEspecial04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/admin/conformarOferta04/cliente/', methods=['POST'])
def ofer04():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'no';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    # print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('admin/conformarOferta05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=listaOfertaVigenteO, salidas=salidaModulos)


@ app.route('/admin/conformarEspecial04/cliente/', methods=['POST'])
def especial04():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('admin/conformarEspecial05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=listaOfertaVigenteO, salidas=salidaModulos)


@ app.route('/sup/conformarEspecial04/cliente/', methods=['POST'])
def supEspecial04():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('sup/conformarEspecial05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=listaOfertaVigenteO, salidas=salidaModulos)
# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@ app.route('/apms/conformarEspecial04/cliente/', methods=['POST'])
def apmsEspecial04():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'si';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('apms/conformarEspecial05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=listaOfertaVigenteO, salidas=salidaModulos)


@app.route('/sup')
def sup_of():
    usuario = request.form["hashUsuario"]

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidos` WHERE o_usuario_hash=%s;", (usuarios))
    pedidos = cursor.fetchall()
    conexion.commit()
    # print(pedidos)

    return render_template('sup/pedidos.html', pedidos=pedidos)
    # return render_template('sup/index.html')


def traerUsuario(usuario):
    session['hash'] = usuario


@app.route('/sup')
def sup_index():
    usuario = request.form['hasUsuario']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('sup/index.html', usuarios=usuarios)


# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@app.route('/login/', methods=['POST'])
def admin_index():
    now = datetime.now()
    usuario = request.form['txtUsuario']
    traerUsuario(usuario)

    contraseña = request.form['txtPassword']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "select * FROM usuarios where u_rrdzz =%s and u_pass =%s;", (usuario, contraseña))
    _usuario = cursor.fetchall()
    
    conexion.commit()
    no = 'no'

    if _usuario:
        _fechaD = datetime.strptime(f"{_usuario[0][5]}", "%Y-%m-%d")
        _fechaH = datetime.strptime(f"{_usuario[0][6]}", "%Y-%m-%d")

        if _fechaD >= now or _fechaH <= now:
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE usuarios SET u_habilitado=%s WHERE u_hash=%s;", (no, _usuario[0][9]))
            conexion.commit()
            flash('Usuario bloqueado.')
            return redirect('/sitio/loguin')
        if _usuario[0][10] == "no":
            flash('Usuario no habilitado.')
            return redirect('/sitio/loguin')

        if _usuario[0][8] == "ADM":
            us = _usuario[0][9]
            return render_template('/admin/index.html', usuarioStorage=us)
        elif _usuario[0][8] == "SUP":
            us = _usuario[0][9]
            return render_template('/sup/index.html', usuarioStorage=us)

        elif _usuario[0][8] == "APM":
            us = _usuario[0][9]
            return render_template('/apms/index.html', usuarioStorage=us)
    else:
        flash('¡Usuario o contraseña, no válido!')
        return redirect('/sitio/loguin')


@app.route('/sitio/loguin')
def admin_loguin():
    return render_template('sitio/loguin.html')
# funciones de oferta comercial:


@app.route('/admin/ofertas/borrar', methods=['POST'])
def admin_ofertas_borrar():
    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM ofertas where id_o=%s;", (_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/verOfertas')


@app.route('/admin/ofertas/guardar', methods=['POST'])
def admin_ofertas_guardar():
    now = datetime.now()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    listaProductoVigente = []
    for i in productos:
        desdeP = datetime.strptime(f"{i[3]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaProductoVigente.append(i)

    conexion.commit()
    # verificar valores:
    for i in listaProductoVigente:
        idProducto = i[0]
        idProducto = str(idProducto)
        _minima = request.form['txtMinima'+idProducto]
        _descuento = request.form['txtDescuento'+idProducto]
        _minimav = int(_minima)
        _descuentov = int(float(_descuento))

        if _minimav < 0 or _descuentov < 0 or _descuentov > 100:
            flash('Verifique, el descuento, debe ser numérico entre 0 y 100.')
            return redirect('/admin/ofertas')

    # -----------------------------------------------------------------

    try:

        for i in listaProductoVigente:
            _modulo = request.form['txtModulo']
            idProducto = i[0]
            idProducto = str(idProducto)

            _producto = request.form['txtProducto'+idProducto]
            _minima = request.form['txtMinima'+idProducto]
            _descuento = request.form['txtDescuento'+idProducto]
            datos_modulo = [_modulo.split('#')]
            datos_producto = [_producto.split('#')]
            _obligatorio = request.form['txtObligatorio'+idProducto]
            _restringido = datos_producto[0][5]
            _minima = int(_minima)
            _descuento = float(_descuento)
            # verificar modulo si existe:
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM `ofertas` where o_modulo=%s and o_producto=%s;", (datos_modulo[0][0], datos_producto[0][0]))
            ofertasPorModulos = cursor.fetchall()

            if _minima > 0 and _descuento > 0 and _descuento < 101:
                if len(ofertasPorModulos) == 0:
                    sql = "INSERT INTO `ofertas` (`id_o`, `o_modulo`,`o_mod_nom`,`o_mod_tit`,`o_mod_pie`,`o_mod_d`,`o_mod_h`, `o_mod_minima`, `o_producto`,`o_prod_cod`,`o_prod_des`,`o_prod_d`,`o_prod_h`, `o_minima`, `o_descuento`, `o_obligatorio`,o_especial, o_restringido) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                    datos = (datos_modulo[0][0], datos_modulo[0][1], datos_modulo[0][2], datos_modulo[0][3], datos_modulo[0][4], datos_modulo[0][5], datos_modulo[0][6],
                             datos_producto[0][0], datos_producto[0][1], datos_producto[0][2], datos_producto[0][3], datos_producto[0][4], _minima, _descuento, _obligatorio, datos_modulo[0][7], _restringido)

                    conexion = mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql, datos)
                    conexion.commit()
                    print(
                        f"Se agrego el modulo {datos_modulo[0][0]} con el producto {datos_producto[0][0]} 1")

                else:
                    sql = "UPDATE ofertas SET o_minima=%s,o_descuento=%s, o_obligatorio=%s WHERE o_modulo=%s and o_producto=%s;"
                    datos = (_minima, _descuento,
                             _obligatorio, _modulo, int(idProducto))
                    conexion = mysql.connect()
                    cursor = conexion.cursor()
                    cursor.execute(sql, datos)
                    conexion.commit()
                    print(
                        f"Se actualizó el modulo {datos_modulo[0][0]} con el producto {datos_producto[0][0]}")

    except ValueError:
        flash('Verifique, el descuento con decimales debe ser con "punto".')

    return redirect('/admin/verOfertas')


@ app.route("/admin/prepararOferta", methods=['POST'])
def prepararOferta():
    now = datetime.now()
    _modulos = request.form['txtModulos']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos` where id_m=%s;", (_modulos))
    modulos = cursor.fetchall()
    listaModuloVigente = []
    for i in modulos:
        desdeM = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        hastaM = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        if desdeM <= now and hastaM > now:
            listaModuloVigente.append(i)

    cursor.execute("SELECT * FROM `productos` order by p_descripcion;")
    productos = cursor.fetchall()
    cursor.execute("SELECT * FROM `ofertas` where o_modulo=%s;",
                   (modulos[0][0]))
    ofertas = cursor.fetchall()
    listaOfertasVigente = []
    for i in ofertas:
        desdeP = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaOfertasVigente.append(i)
    listaProductoVigente = []
    for i in productos:
        desdeP = datetime.strptime(f"{i[3]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaProductoVigente.append(i)
    conexion.commit()
    listaProductosModificados = []

    for i in listaProductoVigente:
        listaPM = list(i)
        listaPM.append(0)
        listaPM.append(0)
        listaPM.append('no')
        for x in listaOfertasVigente:
            ofertasProductos = int(x[8])
            if i[0] == ofertasProductos:
                listaPM[6] = x[13]
                listaPM[7] = x[14]
                listaPM[8] = x[16]
        listaProductosModificados.append(listaPM)

    return render_template('admin/prepararOferta01.html', modulos=listaModuloVigente, productos=listaProductosModificados)


# ofertas control

@ app.route('/admin/verOfertas')
def admin_ver_ofertas():
    now = datetime.now()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` ORDER BY `o_mod_nom` , `o_prod_des`;")
    ofertas = cursor.fetchall()
    listaOfertaVigente = []
    conexion.commit()
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now+timedelta(days=-1):
            if desdeP <= now and hastaP > now+timedelta(days=-1):
                listaOfertaVigente.append(i)
    return render_template('admin/verOfertas.html', ofertas=listaOfertaVigente)


@ app.route('/admin/ofertas')
def admin_ofertas():
    now = datetime.now()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` ORDER BY `o_mod_nom`, `o_prod_des`;")
    ofertas = cursor.fetchall()
    listaOfertaVigente = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now+timedelta(days=-1):
            if desdeP <= now and hastaP > now+timedelta(days=-1):
                listaOfertaVigente.append(i)

    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    listaModuloVigente = []
    for i in modulos:
        desdeM = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        hastaM = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        if desdeM <= now and hastaM > now:
            listaModuloVigente.append(i)

    cursor.execute("SELECT * FROM `productos` order by p_descripcion;")
    productos = cursor.fetchall()
    listaProductoVigente = []
    for i in productos:
        desdeP = datetime.strptime(f"{i[3]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaProductoVigente.append(i)

    conexion.commit()

    return render_template('admin/ofertas.html', ofertas=listaOfertaVigente, modulos=listaModuloVigente, productos=listaProductoVigente)


@ app.route('/admin/editarOfertas/<int:id>')
def admin_ofertas_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE id_o=%s;", (id))
    ofertas = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarOferta.html', ofertas=ofertas)


@app.route('/admin/copiarOferta')
def admin_copiar_oferta():
    now = datetime.now()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    listaModuloVigente = []
    for i in modulos:
        desdeM = datetime.strptime(f"{i[4]}", "%Y-%m-%d")
        hastaM = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        if desdeM <= now and hastaM > now:
            listaModuloVigente.append(i)

    return render_template('admin/copiarOferta.html', modulos=listaModuloVigente)
# copiar


@app.route('/admin/guardar/copiaOferta', methods=['POST'])
def admin_copiarOferta():

    now = datetime.now()
    _modulos = request.form['txtOrigen']
    _destino = request.form['txtDestino']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `ofertas` where o_modulo=%s;", (_modulos))
    ofertas = cursor.fetchall()
    listaModulosVigente = []
    for i in ofertas:
        desdeP = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaModulosVigente.append(i)
    listaProductoVigente = []
    for i in listaModulosVigente:
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeP <= now and hastaP > now:
            listaProductoVigente.append(i)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos` where id_m=%s;", (_destino))
    modulos = cursor.fetchall()
    conexion.commit()

    _destino = request.form['txtDestino']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `ofertas` where o_modulo=%s;", (_destino))
    ofertasD = cursor.fetchall()
    conexion.commit()
    if len(ofertasD) == 0:
        conta = 0

        for i in listaProductoVigente:

            sql = "INSERT INTO `ofertas` (`id_o`, `o_modulo`,`o_mod_nom`,`o_mod_tit`,`o_mod_pie`,`o_mod_d`,`o_mod_h`, `o_mod_minima`, `o_producto`,`o_prod_cod`,`o_prod_des`,`o_prod_d`,`o_prod_h`, `o_minima`, `o_descuento`, `o_obligatorio`,`o_especial`, `o_restringido`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            datos = (modulos[0][0], modulos[0][1], modulos[0][2], modulos[0][3], modulos[0][4], modulos[0][5], modulos[0][6], i[8], i[9],
                     i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17])

            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            conta = conta+1
        flash(
            f"Se han copiado {conta} productos a la oferta {_destino} - {modulos[0][1]}.")

    else:
        flash('La oferta destino ya posee productos asignados, no se ha podido copiar..')
    return redirect('/admin/verOfertas')


@app.route('/admin/procesarOfertas', methods=['POST'])
def admin_ofertas_procesar():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE `pa_estado`='Aprobado';")
    aprobados = cursor.fetchall()
    if len(aprobados) < 1:
        conexion.commit()
        flash('No se encontraron pedidos "Aprobados"')
        return redirect("/admin/pedidos")

    try:
        archivo_texto = open("Procesados.txt", "x")
    except FileExistsError:
        archivo_texto = open("Procesados.txt", "w")
    conta = 1
    tope = len(aprobados)

    for i in aprobados:
        aprobado = {}
        aprobado["id_pedido"] = i[0]
        aprobado["usuario"] = i[1]
        aprobado["drogueria"] = i[2]
        aprobado["cliente"] = i[3]
        aprobado["pedidos"] = i[4]
        aprobado["fecha"] = str(i[5])
        aprobado["estado"] = i[6]
        aprobado["total_unidades"] = i[7]
        aprobado["detalle"] = i[8]

        if conta == 1:
            archivo_texto.write('['+str(aprobado)+',')
        elif tope != conta:
            archivo_texto.write(str(aprobado)+",")
        else:
            archivo_texto.write(str(aprobado)+']')
        conta = conta+1
    archivo_texto.close()

    path = "Procesados.txt"

    sql = "UPDATE `pedidosaaprobar` SET `pa_estado`='Procesado' WHERE `pa_estado`='Aprobado';"
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql)

    conexion.commit()
    flash(f'Se procesaron {tope} registros correctamente.')
    return send_file(path, as_attachment=True)


@app.route('/admin/editarOfertas/editar', methods=['POST'])
def admin_ofertas_editar():
    _id = request.form['txtId']
    _minima = request.form['txtMinProducto']
    _descuento = request.form['txtDescProducto']
    _obligatorio = request.form['txtObligatorio']

    sql = "UPDATE `ofertas` SET `o_minima`=%s, `o_descuento`=%s, `o_obligatorio`=%s WHERE id_o=%s;"
    datos = (_minima, _descuento, _obligatorio, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/verOfertas')
# funciones de usuarios:
# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@ app.route('/sup/cargaOferta00/')
def sup_ofertas():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigente = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            listaOfertaVigente.append(i)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('sup/ofertas.html', ofertas=listaOfertaVigente, droguerias=droguerias, clientes=clientes)


@ app.route('/apms/cargaOferta00/')
def apms_carga_ofertas():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigente = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            listaOfertaVigente.append(i)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('apms/ofertas.html', ofertas=listaOfertaVigente, droguerias=droguerias, clientes=clientes)


@ app.route('/apms/ofertas/')
def apms_ofertas():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM ofertas where o_especial = 'no' ORDER BY o_modulo;")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigente = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            listaOfertaVigente.append(i)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('apms/ofertas.html', ofertas=listaOfertaVigente, droguerias=droguerias, clientes=clientes)


@ app.route('/sup/cargaOfert01/drogueria/', methods=['POST'])
def sup_cargaOferta01_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'no';")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/cargaOferta02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/apms/cargaOfert01/drogueria/', methods=['POST'])
def apms_cargaOferta01_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('apms/cargaOferta02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/sup/cargaOferta02/cliente/', methods=['POST'])
def sup_cargaOferta02_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial = 'no';")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/sup/clientes/')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('sup/cargaOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/apms/cargaOferta02/cliente/', methods=['POST'])
def apms_cargaOferta02_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/apms/clientes/')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('apms/cargaOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/sup/cargaOferta04/cliente/', methods=['POST'])
# @ app.route('/sup/cargaOfert02/cliente/', methods=['POST'])
def sup_cargaOferta04_d_c():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente2']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial='no';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    # print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('sup/cargaOferta05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=listaOfertaVigenteO, salidas=salidaModulos)


@ app.route('/apms/cargaOferta04/cliente/', methods=['POST'])
# @ app.route('/sup/cargaOfert02/cliente/', methods=['POST'])
def apms_cargaOferta04_d_c():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente2']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` where o_especial= 'no';")
    ofertas = cursor.fetchall()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaUnidades = []
    listaOfertaVigente = []
    for i in listaOfertaVigenteO:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    # ancho = len(ofertas)
    # print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in listaOfertaVigenteO:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in listaOfertaVigenteO:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    # print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    # print(modulosFuncion)
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        # print(elScript)
        listaInput.append(f'{m}:{elScript}')

    # print(anchoModulos)
    listaInput = json.dumps(listaInput)
    # print(listaInput)

    return render_template('apms/cargaOferta05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=ofertas, salidas=salidaModulos)


@ app.route('/sup/pedidos', methods=['GET'])
def pedidosTemplate():
    _desde = "2022-01-01"
    _hasta = "9999-12-31"
    usuario = session['hash']

    usuarioEntero = int(usuario)
    listaRegionMetro = [1200, 1300, 1400, 1500]
    listaRegionNacional = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000]
    desdeU = usuarioEntero
    if desdeU in listaRegionMetro:
        hastaU = usuarioEntero + 99
    elif desdeU in listaRegionNacional:
        hastaU = usuarioEntero + 999

    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql = "SELECT * FROM `pedidosaaprobar` WHERE pa_usuario BETWEEN %s AND %s order by id_pedidoa desc;"
    datos = (desdeU, hastaU)
    cursor.execute(sql, datos)
    pedidosTotales = cursor.fetchall()
    lospedidos = pedidosTotales
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes
    return render_template('/sup/pedidos.html', lospedidos=pedidosDC, usuario=usuario, desde=_desde, hasta=_hasta)


# guardamos el pedido del usuario.
@ app.route('/sup/guardar/pedidosaaprobar', methods=['POST'])
def pedidosAprobar():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_obligatorio = 'si';")

    ofertasSi = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertasSi:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    for i in listaOfertaVigenteO:

        input = str(i[0])
        modulo = str(i[1])
        inputPagina = request.form[input]
        inputPagina = int(inputPagina)
        totalModulo = request.form[modulo]
        totalModulo = int(totalModulo)
        if inputPagina == 0 and totalModulo > 0:
            flash('El modulo tiene al menos un producto obligatorio.')
            return redirect('../../admin/mensaje')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'no';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    for oferta in listaOfertaVigenteO:

        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            listaValor.append(valor)

        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor)
    pedidoUser = list(losInputs)
    # print(pedidoUser)
    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    con = 0
    for o in ofertaCompleta:
        contax = 0
        for l in o[1]:
            for i in pedidoUser:
                item = list(l)  # aca puede estar
                print(item)
                print(i)

                if item[0] == i[0]:
                    item.append(i[1])
                    ofertaCompletaConDescuento.append(tuple(item))

            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0

    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)

    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)
    return redirect('/sup/pedidos')


@ app.route('/apms/guardar/pedidosaaprobar', methods=['POST'])
def apmspedidosAprobar():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_obligatorio = 'si';")

    ofertasSi = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertasSi:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    for i in listaOfertaVigenteO:

        input = str(i[0])
        modulo = str(i[1])
        inputPagina = request.form[input]
        inputPagina = int(inputPagina)
        totalModulo = request.form[modulo]
        totalModulo = int(totalModulo)
        if inputPagina == 0 and totalModulo > 0:
            flash('El modulo tiene al menos un producto obligatorio.')
            return redirect('../../admin/mensaje')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'no';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    for oferta in listaOfertaVigenteO:

        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            listaValor.append(valor)

        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor)
    pedidoUser = list(losInputs)
    # print(pedidoUser)
    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    con = 0
    for o in ofertaCompleta:
        contax = 0
        for l in o[1]:
            for i in pedidoUser:
                item = list(l)  # aca puede estar
                print(item)
                print(i)

                if item[0] == i[0]:
                    item.append(i[1])
                    ofertaCompletaConDescuento.append(tuple(item))

            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0

    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)

    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)
    return redirect('/apms/pedidos')


@ app.route('/admin/guardar/pedidosaaprobar', methods=['POST'])
def pedidosAprobarA():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_obligatorio = 'si';")

    ofertasSi = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertasSi:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    for i in listaOfertaVigenteO:

        input = str(i[0])
        modulo = str(i[1])
        inputPagina = request.form[input]
        inputPagina = int(inputPagina)
        totalModulo = request.form[modulo]
        totalModulo = int(totalModulo)
        if inputPagina == 0 and totalModulo > 0:
            flash('El modulo tiene al menos un producto obligatorio.')
            return redirect('../../admin/mensaje')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'no';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    for oferta in listaOfertaVigenteO:

        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            listaValor.append(valor)

        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor)
    pedidoUser = list(losInputs)
    # print(pedidoUser)
    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    con = 0
    for o in ofertaCompleta:
        contax = 0
        for l in o[1]:
            for i in pedidoUser:
                item = list(l)  # aca puede estar
                print(item)
                print(i)

                if item[0] == i[0]:
                    item.append(i[1])
                    ofertaCompletaConDescuento.append(tuple(item))

            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0

    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)

    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)

    return redirect('/admin/pedidos')


@ app.route('/sup/guardar/pedidosaaprobarE', methods=['POST'])
def supPedidosAprobarEspecial():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    listaDescuento = []

    for oferta in listaOfertaVigenteO:
        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            # print(valor)
            descuento = request.form[f"descuento{oferta[0]}"]
            # print(str(descuento))
            listaValor.append(valor)
            listaDescuento.append(descuento)
        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")
            listaDescuento.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor, listaDescuento)
    pedidoUser = list(losInputs)
    print(pedidoUser)

    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    contax = 0
    for o in ofertaCompleta:
        for l in o[1]:
            item = list(l)  # aca puede estar
            print(item)
            for p in pedidoUser:
                if item[0] == p[0]:
                    item[14] = p[2]

            item.append(pedidoUser[contax][1])
            ofertaCompletaConDescuento.append(tuple(item))
            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0
    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)
    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)a
    return redirect('/sup/pedidos')


@ app.route('/apms/guardar/pedidosaaprobarE', methods=['POST'])
def apmsPedidosAprobarEspecial():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    listaDescuento = []

    for oferta in listaOfertaVigenteO:
        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            # print(valor)
            descuento = request.form[f"descuento{oferta[0]}"]
            # print(str(descuento))
            listaValor.append(valor)
            listaDescuento.append(descuento)
        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")
            listaDescuento.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor, listaDescuento)
    pedidoUser = list(losInputs)
    print(pedidoUser)

    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    contax = 0
    for o in ofertaCompleta:
        for l in o[1]:
            item = list(l)  # aca puede estar
            print(item)
            for p in pedidoUser:
                if item[0] == p[0]:
                    item[14] = p[2]

            item.append(pedidoUser[contax][1])
            ofertaCompletaConDescuento.append(tuple(item))
            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0
    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)
    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)a
    return redirect('/apms/pedidos')


@ app.route('/admin/guardar/pedidosaaprobarE', methods=['POST'])
def pedidosAprobarEspecial():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE o_especial = 'si';")
    ofertas = cursor.fetchall()
    conexion.commit()
    now = datetime.now()
    listaOfertaVigenteO = []
    for i in ofertas:
        desdeO = datetime.strptime(f"{i[5]}", "%Y-%m-%d")
        hastaO = datetime.strptime(f"{i[6]}", "%Y-%m-%d")
        desdeP = datetime.strptime(f"{i[11]}", "%Y-%m-%d")
        hastaP = datetime.strptime(f"{i[12]}", "%Y-%m-%d")
        if desdeO <= now and hastaO > now:
            if desdeP <= now and hastaP > now:
                listaOfertaVigenteO.append(i)
    listaInputs = []
    listaValor = []
    listaDescuento = []

    for oferta in listaOfertaVigenteO:
        try:
            listaInputs.append(oferta[0])
            valor = request.form[f"{oferta[0]}"]
            # print(valor)
            descuento = request.form[f"descuento{oferta[0]}"]
            # print(str(descuento))
            listaValor.append(valor)
            listaDescuento.append(descuento)
        except KeyError:
            listaInputs.append(oferta[0])
            listaValor.append("0")
            listaDescuento.append("0")

    listaInputs = set(listaInputs)
    listaInputs = list(listaInputs)
    # print(listaInputs, "inputs")
    # print(listaValor, "valores")
    # print(listaDescuento, "Descuentos")
    losInputs = zip(listaInputs, listaValor, listaDescuento)
    pedidoUser = list(losInputs)
    print(pedidoUser)

    usuario = request.form['pedidoUsuario']
    # print(usuario)
    drogueria = request.form['pedidoDrogueria']
    # print(drogueria)
    cliente = request.form['pedidoCliente']
    # print(cliente)
    salidas = request.form['pedidoOferta']
    output = ast.literal_eval(salidas)  # convertimos un string a lista.
    ofertaCompleta = output
    ofertaCompletaConDescuento = []
    contax = 0
    for o in ofertaCompleta:
        for l in o[1]:
            item = list(l)  # aca puede estar
            print(item)
            for p in pedidoUser:
                if item[0] == p[0]:
                    item[14] = p[2]

            item.append(pedidoUser[contax][1])
            ofertaCompletaConDescuento.append(tuple(item))
            contax = contax+1
    # print(ofertaCompleta[0])
    # print(ofertaCompleta)
    pedido = pedidoUser
    fecha = datetime.now()
    estado = "Sin aprobar"
    # print(ofertaCompleta[0][1][0][0])

    totalUnidades = 0
    conta = 0
    for i in pedido:
        unidad = int(pedido[conta][1])
        conta = conta + 1
        totalUnidades = totalUnidades + unidad
    _detalle = request.form['txtDetalle']
    jsonPedido = json.dumps(ofertaCompletaConDescuento)
    sql = "INSERT INTO `pedidosaaprobar` (`id_pedidoA`,`pa_usuario`,`pa_drogueria`, `pa_cliente`, `pa_pedido`, `pa_fecha`,`pa_estado`, `pa_total`,`pa_detalle`) VALUES (null, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (usuario, drogueria, cliente, jsonPedido,
             str(fecha), estado, totalUnidades, _detalle)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    # print(jsonPedido)a
    return redirect('/admin/pedidos')


@ app.route('/apms/clientes/')
def apms_clientes():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('apms/clientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/sup/clientes/')
def sup_clientes():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/clientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/sup/clientes/editar', methods=['POST'])
def sup_clientes_editar():
    usuario = request.form['hashUsuario']
    cliente = request.form['id_cliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` where u_hash = %s;", (usuario))
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` where id_c = %s;", (cliente))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/editarClientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/sup/clientes/guardar', methods=['POST'])
def sup_clientes_guardar():

    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _postal = request.form['c_postal']

    sql = "INSERT INTO `clientes` (`id_c`, c_id_drogueria,`c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, c_nombre, c_cuit, c_domicilio, c_localidad, c_postal) VALUES (NULL, %s, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/sup/clientes')


@ app.route('/admin/clientes/borrar/<int:id>')
def admin_clientes_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (id))
    # clientes = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/clientes')


"""
@ app.route('/sup/clientes/guardar/<int:usuario>', methods=['POST'])
def sup_clientes_guardar(usuario):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    conexion.commit()
    _drogueria = request.form['txtDrogueria']
    _cuenta = request.form['txtCuenta']
    _nombre = request.form['txtNombre']
    _cuit = request.form['txtCuit']
    _localidad = request.form['txtLocalidad']
    _postal = request.form['txtPostal']
    datos_drogueria = [_drogueria.split('#')]
    if _drogueria == 'Seleccione':
        flash('¡Por favor elija una Droguería!')
        return redirect(f'../{usuario}')

    sql = "INSERT INTO `clientes` (`id_c`, `c_id_drogueria`, `c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, `c_nombre`, `c_cuit`, `c_localidad`, c_postal) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (datos_drogueria[0][0], datos_drogueria[0][1],
             datos_drogueria[0][2], _cuenta, _nombre, _cuit, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect(f'../{usuario}')
"""


@ app.route('/admin/pedidos', methods=['GET'])
def pedidosTemplateA():

    _desde = "2022-01-01"
    _hasta = "9999-12-31 23:59:59"

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `pedidosaaprobar` order by id_pedidoa desc;")
    lospedidos = cursor.fetchall()
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    return render_template('/admin/pedidos.html', lospedidos=pedidosDC, desde=_desde, hasta=_hasta)


@ app.route('/admin/pedidosf', methods=['POST'])
def pedidosfTemplateA():
    _desde = request.form['pedidosDesde']
    _hasta = request.form['pedidosHasta']
    if _desde == _hasta or _hasta == "":
        _hasta = _desde+" 23:59:59"
    else:
        _hasta = _hasta+" 23:59:59"
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE pa_fecha BETWEEN %s AND %s order by id_pedidoa desc;", (_desde+" 00:00:00", _hasta+" 00:00:00"))
    lospedidos = cursor.fetchall()
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    return render_template('/admin/pedidos.html', lospedidos=pedidosDC, desde=_desde, hasta=_hasta)


@ app.route('/sup/pedidosf', methods=['POST'])
def suppedidosfTemplateA():
    _desde = request.form['pedidosDesde']
    _hasta = request.form['pedidosHasta']
    if _desde == _hasta or _hasta == "":
        _hasta = _desde+" 23:59:59"
    else:
        _hasta = _hasta+" 23:59:59"

    usuario = session['hash']

    usuarioEntero = int(usuario)
    listaRegionMetro = [1200, 1300, 1400, 1500]
    listaRegionNacional = [4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000]
    desdeU = usuarioEntero
    if desdeU in listaRegionMetro:
        hastaU = usuarioEntero + 99
    elif desdeU in listaRegionNacional:
        hastaU = usuarioEntero + 999

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE pa_fecha BETWEEN %s AND %s AND pa_usuario BETWEEN %s AND %s order by id_pedidoa desc;", (_desde+" 00:00:00", _hasta+" 00:00:00", desdeU, hastaU))
    lospedidos = cursor.fetchall()
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    return render_template('/sup/pedidos.html', lospedidos=pedidosDC, desde=_desde, hasta=_hasta)


@ app.route('/apms/pedidosf', methods=['POST'])
def apmspedidosfTemplateA():
    _desde = request.form['pedidosDesde']
    _hasta = request.form['pedidosHasta']
    usuario = session['hash']
    usuarioEntero = int(usuario)
    if _desde == _hasta or _hasta == "":
        _hasta = _desde+" 23:59:59"
    else:
        _hasta = _hasta+" 23:59:59"

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE pa_fecha BETWEEN %s AND %s AND pa_usuario = %s order by id_pedidoa desc;", (_desde+" 00:00:00", _hasta+" 00:00:00", usuarioEntero))
    lospedidos = cursor.fetchall()
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    return render_template('/apms/pedidos.html', lospedidos=pedidosDC, desde=_desde, hasta=_hasta)


@ app.route('/admin/usuarios')
def admin_usuarios():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/usuarios.html', usuarios=usuarios)


@ app.route('/admin/editarUsuarios/<int:id>')
def admin_usuarios_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` WHERE id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarUsuario.html', usuarios=usuarios)


@ app.route('/admin/usuarios/borrar/<int:id>')
def admin_usuarios_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios where id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/usuarios')


@ app.route('/sup/clientes/borrar', methods=['POST'])
def sup_clientes_borrar():
    _cliente = request.form['id_cliente']
    _usuario = request.form['usuario_Hash']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (_cliente))
    conexion.commit()
    hash = int(_usuario)

    return redirect(f'/sup/clientes/{hash}')


@ app.route('/sup/clientes/editar', methods=['POST'])
def sup_clientes_update():
    _usuario = request.form['usuario_Hash']
    _cuenta = request.form['txtCuenta']
    _nombre = request.form['txtNombre']
    _cuit = request.form['txtCuit']
    _localidad = request.form['txtLocalidad']
    _postal = request.form['txtPostal']
    _id = request.form['txtID']

    sql = "UPDATE clientes SET c_cuenta=%s, c_nombre=%s, c_cuit=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_cuenta, _nombre, _cuit, _localidad, _postal, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    hash = int(_usuario)

    return redirect(f'/sup/clientes/{hash}')


@ app.route('/admin/editarUsuario/editar', methods=['POST'])
def admin_usuarios_editar():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']
    _roll = request.form['txtRoll']
    _id = request.form['txtID']
    _habilitado = request.form['txtHabilitado']

    sql = "UPDATE usuarios SET u_nombre=%s, u_apellido=%s, u_rrdzz=%s, u_mail=%s, u_desde=%s, u_hasta=%s, u_pass=%s, u_roll=%s , u_habilitado=%s WHERE id_u=%s;"
    datos = (_nombre, _apellido, _rrdzz, _mail,
             _desde, _hasta, _pass, _roll, _habilitado, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')


@ app.route('/admin/usuarios/guardar', methods=['POST'])
def admin_usuarios_guardar():
    now = datetime.now()
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']
    _roll = request.form['txtRoll']
    _hash = randint(1000000000, 9999999999)
    _hash = str(_hash)+_rrdzz
    _habilitado = request.form['txtHabilitado']

# condicional para ver si existe usuario en vigencia

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE u_rrdzz=%s;", (_rrdzz))
    _existeUsuario = cursor.fetchall()
    conexion.commit()
    if _existeUsuario:
        desde = datetime.strptime(f"{_existeUsuario[0][5]}", "%Y-%m-%d")
        hasta = datetime.strptime(f"{_existeUsuario[0][6]}", "%Y-%m-%d")
        if desde <= now and hasta >= now:
            flash('El usuario está vigente, modifique vigencia o elimine el usuario.')
            return redirect('/admin/usuarios')


# condicional para usar mensajes
    sql = "SELECT * FROM usuarios WHERE u_mail=%s;"
    datos = (_mail)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    _existe = cursor.fetchall()
    conexion.commit()

    if _existe:
        flash('Correo, ya registrado')
        return redirect('/admin/usuarios')

    sql = "INSERT INTO `usuarios` (`id_u`, `u_nombre`, `u_apellido`, `u_rrdzz`, `u_mail`, `u_desde`, `u_hasta`, `u_pass`, `u_roll`, `u_hash`, `u_habilitado`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (_nombre, _apellido, _rrdzz, _mail,
             _desde, _hasta, _pass, _roll, _hash, _habilitado)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')
# funciones de productos:


@ app.route('/admin/productos')
def admin_productos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos` order by `p_descripcion`;")
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/productos.html', productos=productos)


@ app.route('/admin/editarProducto/<int:id>')
def admin_producto_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos` WHERE id_p=%s;", (id))
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarProducto.html', productos=productos)


@ app.route('/admin/productos/guardar', methods=['POST'])
def admin_productos_guardar():
    _restringido = request.form['txtRestringido']
    _codigo = request.form['p_cod']
    _desc = request.form['p_descripcion']
    _desde = request.form['p_desde']
    _hasta = request.form['p_hasta']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql = "SELECT * FROM `productos` WHERE p_cod = %s ;"
    datos = _codigo
    cursor.execute(sql, datos)
    productos = cursor.fetchall()
    conexion.commit()
    existe = len(productos)
    if existe > 0:
        flash('El producto ya existe!.')
        return redirect('/admin/productos')

    sql = "INSERT INTO `productos` (`id_p`, `p_cod`, `p_descripcion`, p_desde, p_hasta, p_restringido) VALUES (NULL, %s,%s,%s,%s,%s);"
    datos = (_codigo, _desc, _desde, _hasta, _restringido)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/productos')


@ app.route('/admin/productos/borrar/<int:id>')
def admin_productos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos where id_p=%s;", (id))
    productos = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/productos')


@ app.route('/admin/editarProducto/editar', methods=['POST'])
def admin_productos_editar():

    _cod = request.form['p_cod']
    _desc = request.form['p_descripcion']
    _desde = request.form['p_desde']
    _hasta = request.form['p_hasta']
    _restringido = request.form['txtRestringido']
    _id = request.form['txtID']

    sql = "UPDATE productos SET p_cod=%s, p_descripcion=%s, p_desde =%s, p_hasta=%s, p_restringido=%s WHERE id_p=%s;"
    sql2 = "UPDATE ofertas SET o_prod_cod=%s, o_prod_des=%s, o_prod_d=%s, o_prod_h=%s, o_restringido=%s WHERE o_producto=%s;"
    datos = (_cod, _desc, _desde, _hasta, _restringido, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    cursor.execute(sql2, datos)
    conexion.commit()

    return redirect('/admin/productos')
# funciones de pedidos:


@ app.route('/apms/pedidos')
def apms_pedidos():
    _desde = "2022-01-01"
    _hasta = "9999-12-31"
    usuario = session['hash']
    usuarioEntero = int(usuario)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    sql = "SELECT * FROM `pedidosaaprobar` WHERE pa_usuario = %s order by id_pedidoa desc;"
    datos = (usuarioEntero)
    cursor.execute(sql, datos)
    pedidosTotales = cursor.fetchall()
    lospedidos = pedidosTotales
    conexion.commit()
    pedidosDrogueria = []
    pedidosClientes = []
    for i in lospedidos:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `droguerias`;")
        drogueria = cursor.fetchall()
        for x in drogueria:
            if i[2] == x[1]:
                lista = list(i)
                lista.append(x[2])
                pedidosDrogueria.append(lista)
    for y in pedidosDrogueria:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `clientes`;")
        clientes = cursor.fetchall()
        for z in clientes:
            if y[3] == z[4]:
                lista2 = list(y)
                lista2.append(z[5])
                pedidosClientes.append(lista2)

    pedidosDC = pedidosClientes

    return render_template('/apms/pedidos.html', lospedidos=pedidosDC, desde=_desde, hasta=_hasta)


@ app.route('/apms/clientes/guardar', methods=['POST'])
def apms_clientes_guardar():

    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _postal = request.form['c_postal']

    sql = "INSERT INTO `clientes` (`id_c`, c_id_drogueria,`c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, c_nombre, c_cuit, c_domicilio, c_localidad, c_postal) VALUES (NULL, %s, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/apms/clientes')


@ app.route('/admin/pedidos')
def admin_pedidos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `pedidos`;")
    pedidos = cursor.fetchall()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/pedidos.html', pedidos=pedidos, droguerias=droguerias)


@ app.route('/admin/pedidos/guardar', methods=['POST'])
def admin_pedidos_guardar():

    _droguerias = request.form['pe_droguerias']
    _codigo = request.form['pe_cod']
    _cuit = request.form['pe_cuit']
    _postal = request.form['pe_postal']
    _nombre = request.form['pe_nombre']
    _localidades = request.form['pe_localidades']
    _domicilio = request.form['pe_domicilio']

    sql = "INSERT INTO `pedidos` (`id_pe`, `pe_droguerias`, `pe_cod`, `pe_cuit`,`pe_postal`, `pe_nombre`,`pe_localidades`,`pe_domicilio`) VALUES (NULL, %s,%s, %s,%s, %s,%s, %s);"
    datos = (_droguerias, _codigo, _cuit, _postal,
             _nombre, _localidades, _domicilio)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/pedidos')


@ app.route('/admin/pedidos/borrar', methods=['POST'])
def admin_pedidos_borrar():
    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pedidos where id_pe=%s;", (_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/pedidos')

# funciones de clientes:


@ app.route('/admin/clientes')
def admin_clientes():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/clientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/admin/editarCliente/<int:id>')
def admin_cliente_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarClientes.html', clientes=clientes, droguerias=droguerias)


@ app.route('/sup/editarCliente/<int:id>')
def sup_cliente_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('sup/editarClientes.html', clientes=clientes, droguerias=droguerias)


@ app.route('/apms/editarCliente/<int:id>')
def apms_cliente_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('apms/editarClientes.html', clientes=clientes, droguerias=droguerias)


@ app.route('/sup/editarCliente/editar', methods=['POST'])
def sup_cliente_editar():
    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _postal = request.form['c_postal']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _id = request.form['txtID']
    sql = "UPDATE clientes SET c_id_drogueria=%s, c_cod_drogueria=%s, c_desc_drogueria=%s, c_cuenta=%s, c_nombre =%s, c_cuit=%s, c_domicilio=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal, _id)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/sup/clientes')


@ app.route('/apms/editarCliente/editar', methods=['POST'])
def apms_cliente_editar():
    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _postal = request.form['c_postal']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _id = request.form['txtID']
    sql = "UPDATE clientes SET c_id_drogueria=%s, c_cod_drogueria=%s, c_desc_drogueria=%s, c_cuenta=%s, c_nombre =%s, c_cuit=%s, c_domicilio=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal, _id)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/apms/clientes')


@ app.route('/admin/editarCliente/editar', methods=['POST'])
def admin_cliente_editar():
    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _postal = request.form['c_postal']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _id = request.form['txtID']
    sql = "UPDATE clientes SET c_id_drogueria=%s, c_cod_drogueria=%s, c_desc_drogueria=%s, c_cuenta=%s, c_nombre =%s, c_cuit=%s, c_domicilio=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal, _id)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/clientes')


@ app.route('/admin/clientes/guardar', methods=['POST'])
def admin_clientes_guardar():

    drogueria = request.form['c_cod']
    drog = drogueria.split('#')
    _idDrogueria = drog[0]
    _codigo = drog[1]
    _descrip = drog[2]
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _domicilio = request.form['c_domicilio']
    _localidad = request.form['c_localidad']
    _postal = request.form['c_postal']

    sql = "INSERT INTO `clientes` (`id_c`, c_id_drogueria,`c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, c_nombre, c_cuit, c_domicilio, c_localidad, c_postal) VALUES (NULL, %s, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (_idDrogueria, _codigo, _descrip, _cuenta, _nombre,
             _cuit, _domicilio, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/clientes')


"""
@ app.route('/admin/clientes/borrar/<int:id>')
def admin_clientes_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/clientes')
"""
# funciones de droguerias:


@ app.route('/admin/editarDroguerias/<int:id>')
def admin_droguerias_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias` WHERE id_d=%s;", (id))
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarDrogueria.html', droguerias=droguerias)


@ app.route('/admin/droguerias')
def admin_droguerias():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/droguerias.html', droguerias=droguerias)


@ app.route('/admin/droguerias/guardar', methods=['POST'])
def admin_droguerias_guardar():

    _codigo = request.form['d_cod']
    _desc = request.form['d_descripcion']

    sql = "INSERT INTO `droguerias` (`id_d`, `d_cod`, `d_descripcion`) VALUES (NULL, %s,%s);"
    datos = (_codigo, _desc)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/droguerias')


@ app.route('/admin/droguerias/borrar/<int:id>')
def admin_droguerias_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM droguerias where id_d=%s;", (id))
    drogueria = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/droguerias')


@ app.route('/admin/editarDrogueria/editar', methods=['POST'])
def admin_droguerias_editar():

    _cod = request.form['txtCodigo']
    _desc = request.form['txtDescripcion']
    _id = request.form['txtID']

    sql = "UPDATE droguerias SET d_cod=%s, d_descripcion=%s WHERE id_d=%s;"
    datos = (_cod, _desc, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/droguerias')
# funciones de módulos:


@ app.route('/apms/modulos')
def apms_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('apms/modulos.html', modulos=modulos)


@ app.route('/sup/modulos')
def sup_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('sup/modulos.html', modulos=modulos)


@ app.route('/admin/modulos')
def admin_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/modulos.html', modulos=modulos)

# -------------------------------------------------------------------------


@ app.route('/apibeta', methods=['GET'])
def usuarios_oces():
    try:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `modulos`;")
        modulo = cursor.fetchall()
        listaModulos = []
        for m in modulo:
            modulos = {}
            modulos["id_m"] = m[0]
            modulos["m_nombre"] = m[1]
            modulos["m_titulo"] = m[2]
            modulos["m_pie"] = m[3]
            modulos["m_desde"] = m[4]
            modulos["m_hasta"] = m[5]
            modulos["m_cantidad_minima"] = m[6]
            listaModulos.append(modulos)

        return jsonify({"modulo": listaModulos, "mensaje": "Módulos encontrados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@ app.route('/apibeta/<int:id>', methods=['GET'])
def usuarios_oces_uno(id):
    try:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `modulos` where id_m = %s;", (id))
        modulo = cursor.fetchone()
        if modulo != None:
            listaModulos = []
            modulos = {}
            modulos["id_m"] = modulo[0]
            modulos["m_nombre"] = modulo[1]
            modulos["m_titulo"] = modulo[2]
            modulos["m_pie"] = modulo[3]
            modulos["m_desde"] = modulo[4]
            modulos["m_hasta"] = modulo[5]
            modulos["m_cantidad_minima"] = modulo[6]
            listaModulos.append(modulos)

            return jsonify({"modulo": listaModulos, "mensaje": "Modulo encontrado."})
        else:
            return jsonify({"mensaje": "Modulo no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@ app.route('/apibeta', methods=['POST'])
def registrar_modulos_api():
    respuesta = request.json
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _id = request.json['modulo'][count]['idM']
            sql = "DELETE FROM modulos WHERE id_m = %s;"
            datos = (_id)
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
            nw_mensaje = _mensaje+" OK del server"
        return jsonify({"mensaje": nw_mensaje+" "+respuesta})
    except Exception as ex:
        return jsonify({'mensaje': f"Error {respuesta}"})


@ app.route('/apibeta2', methods=['DELETE'])
def registrar_modulos_api_DELETE_():
    respuesta = request.json
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _id = request.json['modulo'][count]['idM']
            sql = "DELETE FROM modulos WHERE id_m = %s;"
            datos = (_id)
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
            nw_mensaje = _mensaje+" OK del server"
        return jsonify({"mensaje": nw_mensaje+" "+respuesta})
    except Exception as ex:
        return jsonify({'mensaje': f"Error {respuesta}"})


@ app.route('/apibeta2', methods=['PUT'])
def registrar_modulos_api_put_():
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:

            _nombre = request.json['modulo'][count]['Mnombre']
            _titulo = request.json['modulo'][count]['Mtitulo']
            _pie = request.json['modulo'][count]['Mpie']
            _desde = request.json['modulo'][count]['Mdesde']
            _hasta = request.json['modulo'][count]['Mhasta']
            _minima = request.json['modulo'][count]['Mcantidad']
            _id = request.json['modulo'][count]['idM']

            if _nombre != None:
                sql = "UPDATE modulos SET m_nombre=%s WHERE id_m=%s;"
                datos = (_nombre, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'nombre', error"
            if _titulo != None:
                sql = "UPDATE modulos SET m_titulo=%s WHERE id_m=%s;"
                datos = (_titulo, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'titulo', error"
            if _pie != None:
                sql = "UPDATE modulos SET m_pie=%s WHERE id_m=%s;"
                datos = (_pie, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'Pie', error"
            if _desde != None:
                sql = "UPDATE modulos SET m_desde=%s WHERE id_m=%s;"
                datos = (_desde, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'desde', error"
            if _hasta != None:
                sql = "UPDATE modulos SET m_hasta=%s WHERE id_m=%s;"
                datos = (_hasta, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'hasta', error"
            if _minima != None:
                sql = "UPDATE modulos SET m_cantidad_minima = %s WHERE id_m=%s;"
                datos = (_minima, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'minima', error"
            count += 1
        nw_mensaje = _mensaje+" OK del server: PUT por ID"
        return jsonify({"mensaje": nw_mensaje})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@ app.route('/apibeta2', methods=['POST'])
def registrar_modulos_api_sin_():

    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _nombre = request.json['modulo'][count]['Mnombre']
            _titulo = request.json['modulo'][count]['Mtitulo']
            _pie = request.json['modulo'][count]['Mpie']
            _desde = request.json['modulo'][count]['Mdesde']
            _hasta = request.json['modulo'][count]['Mhasta']
            _cantidad = request.json['modulo'][count]['Mcantidad']

            sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`, `m_cantidad_minima`) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
            datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad)

            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
        return jsonify({"mensaje": _mensaje})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})
# ----------------------------------------------------------------------------------


@ app.route('/admin/editarModulos/editar', methods=['POST'])
def admin_modulo_editar():

    _nombre = request.form['txtNombre']
    _titulo = request.form['txtTitulo']
    _pie = request.form['txtPie']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _id = request.form['txtID']
    _cantidad = request.form['txtCantidad']
    _especial = request.form['txtEspecial']
    sql = "UPDATE modulos SET m_nombre=%s, m_titulo=%s, m_pie=%s, m_desde=%s, m_hasta=%s, m_cantidad_minima=%s, m_especial=%s WHERE id_m=%s;"
    datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad, _especial, _id)
    sql2 = "UPDATE ofertas SET o_mod_nom=%s, o_mod_tit=%s, o_mod_pie=%s, o_mod_d=%s, o_mod_h=%s, o_mod_minima=%s,o_especial=%s WHERE o_modulo=%s;"
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    cursor.execute(sql2, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/modulos/guardar', methods=['POST'])
def admin_modulos_guardar():
    _especial = request.form['txtEspecial']
    if _especial == "si":
        _nombre = request.form['m_nombre']
        _titulo = request.form['m_titulo']
        _pie = request.form['m_pie']
        _desde = request.form['m_desde']
        _hasta = request.form['m_hasta']
        _cantidad = request.form['txtCantidad']

        sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`, `m_cantidad_minima`, `m_especial`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s);"
        datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad, _especial)
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
        return redirect('/admin/modulos')

    _nombre = request.form['m_nombre']
    _titulo = request.form['m_titulo']
    _pie = request.form['m_pie']
    _desde = request.form['m_desde']
    _hasta = request.form['m_hasta']
    _cantidad = request.form['txtCantidad']

    sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`, `m_cantidad_minima`, `m_especial`) VALUES (NULL, %s,%s,%s,%s,%s,%s,'no');"
    datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/modulos/borrar/<int:id>')
def admin_modulos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM modulos where id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/pedidorealizado/<int:id>')
def admin_pedido_realizado(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    lospedidos = cursor.fetchall()
    conexion.commit()
    usuario = lospedidos[0][1]
    drogueria = lospedidos[0][2]
    cliente = lospedidos[0][3]
    lospedidosU = lospedidos[0][4]
    lista = json.loads(lospedidosU)
    listaModulosPedidos = []
    for i in lista:
        listaModulosPedidos.append(i[1])
    listaModulos = set(listaModulosPedidos)

    listaGeneral = []
    for i in listaModulos:
        listaM = []
        for x in lista:
            if i == x[1]:
                listaM.append(x)
        listaGeneral.append(listaM)
    if listaGeneral[0][0][17] == "no":
        listaGeneral = listaGeneral[::-1]  # para ver los pedidos comunes bien
    total = lospedidos[0][7]
    detalle = lospedidos[0][8]

    return render_template('admin/pedidoRealizado.html', lospedidos=lospedidos, usuario=usuario, drogueria=drogueria, cliente=cliente, lista=listaGeneral, total=total, detalle=detalle)


@ app.route('/sup/pedidorealizado/<int:id>')
def sup_pedido_realizado(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    lospedidos = cursor.fetchall()
    conexion.commit()
    usuario = lospedidos[0][1]
    drogueria = lospedidos[0][2]
    cliente = lospedidos[0][3]
    lospedidosU = lospedidos[0][4]
    lista = json.loads(lospedidosU)
    listaModulosPedidos = []
    for i in lista:
        listaModulosPedidos.append(i[1])
    listaModulos = set(listaModulosPedidos)

    listaGeneral = []
    for i in listaModulos:
        listaM = []
        for x in lista:
            if i == x[1]:
                listaM.append(x)
        listaGeneral.append(listaM)
    if listaGeneral[0][0][17] == "no":
        listaGeneral = listaGeneral[::-1]  # para ver los pedidos comunes bien
    total = lospedidos[0][7]
    detalle = lospedidos[0][8]

    return render_template('sup/pedidoRealizado.html', lospedidos=lospedidos, usuario=usuario, drogueria=drogueria, cliente=cliente, lista=listaGeneral, total=total, detalle=detalle)


@ app.route('/apms/pedidorealizado/<int:id>')
def apms_pedido_realizado(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    lospedidos = cursor.fetchall()
    conexion.commit()
    usuario = lospedidos[0][1]
    drogueria = lospedidos[0][2]
    cliente = lospedidos[0][3]
    lospedidosU = lospedidos[0][4]
    lista = json.loads(lospedidosU)
    listaModulosPedidos = []
    for i in lista:
        listaModulosPedidos.append(i[1])
    listaModulos = set(listaModulosPedidos)

    listaGeneral = []
    for i in listaModulos:
        listaM = []
        for x in lista:
            if i == x[1]:
                listaM.append(x)
        listaGeneral.append(listaM)
    if listaGeneral[0][0][17] == "no":
        listaGeneral = listaGeneral[::-1]  # para ver los pedidos comunes bien
    total = lospedidos[0][7]
    detalle = lospedidos[0][8]

    return render_template('apms/pedidoRealizado.html', lospedidos=lospedidos, usuario=usuario, drogueria=drogueria, cliente=cliente, lista=listaGeneral, total=total, detalle=detalle)


@ app.route('/admin/editarModulos/<int:id>')
def admin_modulos_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos` WHERE id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarModulo.html', modulos=modulos)


@ app.route('/admin/aprobar/<int:id>')
def admin_aprobar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/admin/pedidos')
    if estadoPedido[0][6] != "Sin aprobar":
        flash('Pedido debe estar en estado "Sin aprobar".')
        return redirect('/admin/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Aprobado' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/admin/pedidos')


@ app.route('/admin/rechazar/<int:id>')
def admin_rechazar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/admin/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Sin aprobar' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/admin/pedidos')


@ app.route('/admin/revisar/<int:id>')
def admin_revisar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/admin/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Revisar' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/admin/pedidos')


@ app.route('/sup/aprobar/<int:id>')
def sup_aprobar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/sup/pedidos')
    if estadoPedido[0][6] != "Sin aprobar":
        flash('Pedido debe estar en estado "Sin aprobar".')
        return redirect('/sup/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Aprobado' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/sup/pedidos')


@ app.route('/sup/rechazar/<int:id>')
def sup_rechazar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/sup/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Sin aprobar' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/sup/pedidos')


@ app.route('/sup/revisar/<int:id>')
def sup_revisar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/sup/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE `pedidosaaprobar` SET `pa_estado`='Revisar' WHERE id_pedidoA=%s;", (id))
    conexion.commit()

    return redirect('/sup/pedidos')


@ app.route('/sup/eliminar/<int:id>')
def sup_eliminar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/sup/pedidos')
    if estadoPedido[0][6] != "Revisar":
        flash('Pedido debe estar en estado "Revisar".')
        return redirect('/sup/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM `pedidosaaprobar` WHERE id_pedidoA='%s';", (id))
    conexion.commit()
    return redirect('/sup/pedidos')


@ app.route('/admin/eliminar/<int:id>')
def admin_eliminar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/admin/pedidos')
    if estadoPedido[0][6] != "Revisar":
        flash('Pedido debe estar en estado "Revisar".')
        return redirect('/admin/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM `pedidosaaprobar` WHERE id_pedidoA='%s';", (id))
    conexion.commit()

    return redirect('/admin/pedidos')


@ app.route('/apms/eliminar/<int:id>')
def apms_eliminar_pedido(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidosaaprobar` WHERE id_pedidoA=%s;", (id))
    estadoPedido = cursor.fetchall()
    conexion.commit()
    if estadoPedido[0][6] == "Procesado":
        flash('El pedido fue procesado.')
        return redirect('/admin/pedidos')
    if estadoPedido[0][6] != "Revisar":
        flash('Pedido debe estar en estado "Revisar".')
        return redirect('/apms/pedidos')
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM `pedidosaaprobar` WHERE id_pedidoA='%s';", (id))
    conexion.commit()

    return redirect('/apms/pedidos')


def pagina_no_encontrada(error):
    return "<h2>La página no existe.</h2>", 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host="192.168.1.33", port=8000,debug=True)
# host="192.168.0.117", port=8000,
# host="89.0.0.28", port=8000,
