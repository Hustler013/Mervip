from flask import Flask, render_template, request, session, redirect, url_for, flash
from bdatos import *
from bddmetricas import *
from datetime import datetime
import time


app = Flask(__name__)
app.secret_key = 'jsp1234'




################# METODOS DONDE SE RENDERIZAN PAGINAS WEB ##################
@app.route('/')
def index() -> 'html':
    return render_template('index.html', titulo='Mervip')


@app.route('/login')
def login() -> 'html':
    return render_template('login.html', titulo='Mervip/Inicio Sesion')


@app.route('/registro')
def cuentanueva() -> 'html':
    return render_template('registrarse.html', titulo='Crear una Cuenta Nueva')

@app.route('/contactos')
def ayudaclc() -> 'html':
    return render_template('ayuda.html', titulo='Mervip/Soporte')

@app.route('/comunicar1',methods=['POST'])
def correoinv()->'html':
    nombre = str(request.form['nombre'])
    mensaje = str(request.form['mensaje'])
    correo=str(request.form['correo'])
    #ban=enviarcorreo(correo,mensaje,nombre)
    flash(
        '<div class="alert alert-success" role="alert"> <center><b><i class="bi bi-bookmark-check-fill"></i> Su requerimiento fue aceptado correctamente, nuestros asesores se comunicaran al correo ingresado. </b></center> </div>')
    return redirect(url_for('ayudaclc'))





@app.route('/verproductos')
def listaproductos() -> 'html':
    lista = listaproductosg()
    numero = numerogeneralpro()
    nua = numerogeneralproa()
    nux = numerogeneralprox()
    prog, proa = prodgoogle();
    return render_template('productosbase.html', titulo='Mervip/Lista de Productos', lstp=lista, np=numero, na=nua,
                           nx=nux, am=prog, go=proa)


@app.route('/productod', methods=['GET'])
def productogeneral() -> 'html':
    prod = request.args.get('id')

    datpro, cat = mostrarproducto(prod)
    daca = mprodcat(cat, prod)
    #print(datpro)

    return render_template('detallep.html', titulo="Mervip/Producto Detalle", pr=datpro, pc=daca)





#################METODOS PRINCIPALES DE FUNCIONAMIENTO DEL SITIO ##################
# Metodo para Ingresar a la Sesion,Valida el Cliente

@app.route('/ingresar', methods=['POST'])
def ingreso() -> 'html':
    user = request.form['correo']
    clave1 = request.form['contrasenia']
    validar = queryDatos(user, clave1)
    #print(validar)

    if validar == True:
        perfilu = 1
        nombre = nombreuser(user)
        #print(nombre)
        cedula = ciuser(user)
        session['username'] = user
        session['pass'] = clave1
        session['perfiluser'] = perfilu
        session['nombre'] = nombre
        session['ci'] = cedula

        ###variables de las metricas
        #session['tiempo'] = time.time()
        #session['gtiempo']=0
        #session['nayudas'] = 0
        #session['nerrores'] = 0
        #session['tiempop'] = 0
        #session['ntrans'] = 0
        #session['tiempotran'] = time.time()
        #session['pcerradas']=0

        return redirect(url_for('paginicio'))
    else:
        flash(
            '<div class="alert alert-danger" role="alert"> <center><b> Correo Electronico o Contraseña son Incorrectos</b></center> </div>')
        return redirect(url_for('login'))


# Metodo que redirige a la pagina de inicio del cliente
@app.route('/inicio')
def paginicio() -> 'html':
    if 'username' in session:

        # menu=menuopciones(str(session['perfiluser']))
        usuario = session['username']
        nom = str(session['nombre'])
        ced = str(session['ci'])

        ####IDENTIFICADOR DE PEDIDO EN VARIABLE DE SESION
        pedido=idpedido();
        session['idpedido']=pedido+1

        #tr=session['pcerradas']
        #sd=tr+1
        #session['pcerradas']=sd
        ###############

        lista = listaproductosg()
        numero = numerogeneralpro()
        nua = numerogeneralproa()
        nux = numerogeneralprox()
        proa, prog = prodgoogle()
        cpro = cantidadcarrito(ced)
        return render_template('cliente.html', titulo="Mervip", lstp=lista, nomb=nom, np=numero ,na=nua,
                               nx=nux, go=prog, am=proa, cant=cpro)


    else:
        return redirect(url_for('login'))


@app.route('/producto', methods=['GET'])
def mostrarprod() -> 'html':
    if 'username' in session:

        # menu=menuopciones(str(session['perfiluser']))
        usuario = session['username']
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        nom = str(session['nombre'])
        prod = request.args.get('id')


        #metrica de cuanto tiempo necesita el usuario para pasar de una pagina a otra
        #times=float(session['tiempo'])
        #ctie=round(time.time()-times)

        #if  str(session['tiempop']) =="0":
           # session['tiempop']=ctie
        #print("tiempo entre cliente y producto es ",round(time.time()-times))
        ##############################################################################
        #######metrica de tiempo para completar una transaccion



        datpro, cat = mostrarproducto(prod)
        daca = mprodcat(cat, prod)
        #print(datpro)

        return render_template('producto.html', titulo="Mervip", nomb=nom, pr=datpro, pc=daca, cant=cpro)


    else:
        return redirect(url_for('index'))


@app.route('/ingresarclie', methods=['POST'])
def ingusuario() -> 'html':
    cedula = request.form['cedula']
    apellido = request.form['apellido']
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['domicilio']
    correo = request.form['correo']
    clave = request.form['contrasenia']
    existe = existeuser(cedula)

    #print(existe)
    if existe == True:

        flash('<div class="alert alert-danger" role="alert"> <center><b> EL USUARIO YA EXISTE</b></center> </div>')
        return redirect(url_for('cuentanueva'))
    else:
        ingresar = nuevocliente(cedula, nombre, apellido, telefono, direccion, correo, clave)

    if ingresar == True:
        flash(
            '<div class="alert alert-success" role="alert"> <center><b> <i class="bi bi-bookmark-check-fill"></i> Cuenta Creada Exitosamente </b></center> </div>')
        return redirect(url_for('login'))
    else:
        flash(
            '<div class="alert alert-danger" role="alert"> <center><b> Se ha producido un error al crear la cuenta. Porfavor Intente Nuevamente</b></center> </div>')
        return redirect(url_for('cuentanueva'))


@app.route('/comparar')
def vcomparar() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        listap = listaproductosg()
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        return render_template('comparacion.html', titulo='Comparación de Productos', nomb=nom, prod=listap, cant=cpro)

    else:
        return redirect(url_for('index'))


@app.route('/pcomparar', methods=['POST'])
def comparaciones() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        p1 = request.form['prod1']
        p2 = request.form['prod2']
        proa = verprocompara(p1)
        prob = verprocompara(p2)
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        return render_template('vercomparaciones.html', titulo='Comparación de Productos', nomb=nom, pa=proa, pb=prob,
                               cant=cpro)

    else:
        return redirect(url_for('index'))


@app.route('/ayuda')
def ayudasclie() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        #metrica veces que el usuario accede a ayudas en linea
        #ar=int(session['nayudas'])
        #session['nayudas']=ar+1


        return render_template('ayudaclie.html', titulo='Ayuda', nomb=nom, cant=cpro,correo=usuario)

    else:
        return redirect(url_for('index'))


@app.route('/agcarrito', methods=['POST'])
def carritoag() -> 'html':
    if 'username' in session:
        cedula = session['ci']
        usuario = session['username']
        nom = str(session['nombre'])
        npro = request.form['numc']
        idpro = request.form['prodId']
        #print(npro)

        if npro =="0" :
            # metrica de numero de errores###

            #er = int(session['nerrores'])
            #session['nerrores'] = er + 1

            ####
            flash('<div class="alert alert-danger" role="alert"> <center><b><i class="bi bi-bookmark-x-fill"></i> Escoga una cantidad del Producto </b></center> </div>')
            return redirect("/producto?id="+idpro)


        ingresar = agcarrito(cedula, npro, idpro,session['idpedido']);

        if ingresar == True:
            flash(
                '<div class="alert alert-success" role="alert"> <center><b> <i class="bi bi-cart-check"></i> Producto Añadido a su Carrito Exitosamente </b></center> </div>')
            return redirect(url_for('vcarritocompra'))
        else:
            flash(
                '<div class="alert alert-danger" role="alert"> <center><b> <i class="bi bi-bookmark-x-fill"></i>  Error al Añadir su Producto por favor verifique si existe existencias.</b></center> </div>')
            # metrica de numero de errores###

            #er = int(session['nerrores'])
            #session['nerrores'] = er + 1

            ####

            return redirect(url_for('vcarritocompra'))


@app.route('/vercarrito')
def vcarritocompra() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        cedula = session['ci']
        valores= visualcarrito(cedula)
        envio=5.00
        sub=vsubtotal(cedula)

        banderas="false"
        if sub == None:
            sub=0.00
            iva=0.00
            total=0.00
            envio=0.00
            banderas="true"
            flash('<div class="alert alert-warning" role="alert"> <center><b> <i class="bi bi-exclamation-triangle-fill"></i> No tiene Productos Añadido al Carrito <i class="bi bi-exclamation-triangle-fill"></i> </b></center> </div>')
        else:
            iva = float(sub) * 0.12
            total = float(sub) + iva+envio

        cpro = cantidadcarrito(cedula)
        #####metrica de efectividad
        ##se calcula en base a los productos que existen el carrito ya que se considerarian transacciones incompletas
        #fecha = datetime.now()
        #fechas = fecha.date()
        #efectividad(cpro,fechas)
        #######
        return render_template('vercarrito.html', titulo='Carrito de Compras', nomb=nom, carpro=valores, sto=sub,
                               cant=cpro,bloq=banderas,pedido=session['idpedido'],iva=iva,total=total,en=envio)

    else:
        return redirect(url_for('index'))


@app.route('/eliminarcar', methods=['GET'])
def eliminarcar() -> 'html':
    if 'username' in session:

        ced = str(session['ci'])
        pr = request.args.get('prod')

        eliminar = eliminarcarrito(pr, ced)

        if eliminar == True:

            flash(
                '<div class="alert alert-success" role="alert"> <center><b> Producto Eliminado del Carrito de Compras</b></center> </div>')
            return redirect("/vercarrito")
        else:
            flash(
                '<div class="alert alert-danger" role="alert"> <center><b> No se ha podido eliminar el producto de su carrito por favor comuniquese con ayuda al cliente.</b></center> </div>')
            return redirect(url_for('vcarritocompra'))

    else:
        return redirect(url_for('index'))


@app.route('/confirmapago',methods=['POST'])
def pagarproductos() -> 'html':
    if 'username' in session:
        cedula = session['ci']
        usuario = session['username']
        nom = str(session['nombre'])
        tarjet = str(request.form['tarjeta'])
        mes = str(request.form['mes'])
        anio=str(request.form['anio'])
        subtotal=str(request.form['total'])
        clave=str(request.form['clave'])
        cpro = cantidadcarrito(cedula)
        tot=float(subtotal)*0.12
        total=round(float(subtotal)+tot,2)
        fecha = datetime.now()
        fechas = fecha.date()

        if tarjet=="" or mes=="" or anio=="" or clave=="":

            flash(
                '<div class="alert alert-danger" role="alert"> <center><b> Estimado Cliente por favor verifique que todos los campos de su tarjeta hayan sidos completados.</b></center> </div>')
            return redirect(url_for('vcarritocompra'))
        else:
            ingresar=factura(cedula,cpro,subtotal,total,fechas,session['idpedido'])
            ingdetalle=detallefacturainsert(cedula)
            e=carritoel(cedula)
            pedido = session['idpedido']
            insertsecpedido(int(pedido))

            session['idpedido']=idpedido()+1


        if ingresar == True :
            # ####################################metrica de eficiencia
            ##metrica para completar una transaccion
            #times = float(session['tiempotran'])
            #timesv=round(time.time() - times)
            #session['tiempotran']=timesv

            #fecha = datetime.now()
            #fechas = fecha.date()

            #eficiencia(timesv, 1, fechas)
            ########################################################
            idfact=ultimafactura(cedula)
            return render_template('compra.html', titulo='Compra',val=total,nomb=nom,facid=idfact)

        else:
            # metrica de numero de errores###

            #er = int(session['nerrores'])
            #session['nerrores'] = er + 1

            ####
            flash(
                '<div class="alert alert-danger" role="alert"> <center><b> Error al Generar su Pago </b></center> </div>')
            return redirect(url_for('vcarritocompra'))

    else:
        return redirect(url_for('index'))

@app.route('/compra')
def compraval() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        cedula = session['ci']
        valores, sub = visualcarrito(cedula)
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)


        return render_template('compra.html', titulo='Compra')

    else:
        return redirect(url_for('index'))

@app.route('/misfacturas')
def misfact() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        cedula = session['ci']
        ced = str(session['ci'])
        fac=verfacturas(ced)
        cpro = cantidadcarrito(ced)
        return render_template('miscompras.html', titulo='Mis Facturas',carpro=fac,nomb=nom,cant=cpro)

    else:
        return redirect(url_for('index'))

@app.route('/comunicar',methods=['POST'])
def comunic() -> 'html':
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        #correo = str(request.form['corres'])
        #print("correo"+usuario)
        mensaje = str(request.form['mensaje'])
        #print("mensaje  " + mensaje)
        #eliminar=enviarcorreos(usuario,mensaje)
        flash('<div class="alert alert-success" role="alert"> <center><b> <i class="bi bi-shield-fill-check"></i> Su requerimiento fue recibido correctamente</b></center> </div>')
        return redirect("/ayuda")




    else:
        return redirect(url_for('index'))


# Metodo para Cerrar la Sesion
@app.route('/cerrarsesion')
def salir() -> 'html':
    # metrica veces que el usuario accede a ayudas en linea
    #ar=int(session['nayudas'])
    #print(ar)

    #metrica numero de errores en una sesion
    #er=int(session['nerrores'])
    #print(er)

    #metrica del tiempo entre paginas
    #tp=int(session['tiempop'])
    #print(tp)

    #ingreso de la metrica a la bdd
    #fecha = datetime.now()
    #fechas = fecha.date()

    #paginas cerradas
    #cr=int(session['pcerradas'])
    #entendibilidad(ar,cr,er,tp,fechas)


    session.clear()


    return redirect(url_for('index'))

@app.route('/vfactura',methods=['GET'])
def verfact():
    if 'username' in session:
        usuario = session['username']
        nom = str(session['nombre'])
        ced = str(session['ci'])
        cpro = cantidadcarrito(ced)
        id=request.args.get('id')
        detalle,fecha,subtotal=verdetallefact(ced,id)
        iva=subtotal*0.12
        total=subtotal+iva

        return render_template('facturas.html', titulo='Factura',nomb=nom,cedula=ced,fat=id,fact=detalle,fecha=fecha,sub=round(subtotal,2),iva=round(iva,2),tt=round(total,2))


    else:
        return redirect(url_for('index'))


###########FIN DEL PROGRAMA #################
app.run(debug=True)
