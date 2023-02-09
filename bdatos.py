import psycopg2

db = psycopg2.connect(host="localhost", database="proyectom", user="postgres", password="1234")



def queryDatos(user, contra):

    sql = "SELECT * FROM clientes WHERE correo='"+str(user)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:

        email=row[5]
        contrasenia=row[6]

        if email == user and contrasenia == contra:
            return True
        else:
            return False

def existeuser(id):
    sql = "select exists(select 1 from clientes where cedula='"+str(id)+"');"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        dato = row[0]


    return dato



def perfiluser(user):

    dato=0
    sql = "SELECT * FROM clientes WHERE correo='"+str(user)+"'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        dato = row[1]
    return dato

def nombreuser(user):

    sql = "SELECT * FROM clientes WHERE correo='" + str(user) + "'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        nombre = row[1]+" "+row[2]

    return nombre

def ciuser(user):

    sql = "SELECT * FROM clientes WHERE correo='" + str(user) + "'"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        ci = row[0]
    return ci

def listaproductosg():

    sql = "SELECT * FROM productos "
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    return data

def mostrarproducto(id):

    sql = "select * from productos where id_producto="+id
    #print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    #print(data)

    for row in data:
        cat = row[5]


    return data,cat

def mprodcat(categoria,id):

    sql = "select * from productos where tipo='" + str(categoria) + "' and id_producto<>"+id
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


def nuevocliente(cedula,nombre,apellido,telefono,direccion,correo,clave):
    try:
        sql="INSERT INTO CLIENTES (cedula,nombre,apellido,telefono,direccion,correo,clave) values " \
             "('"+str(cedula)+"','"+str(nombre)+"','"+str(apellido)+"','"+str(telefono)+"','"+str(direccion)+"','"+str(correo)+"','"+str(clave)+"');"
        #print(apellido)
        print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def verprocompara(id):

    sql = "SELECT nombreprod,detalle,imagen FROM PRODUCTOS where id_producto="+id
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


#metodo para agregar al carrito de compras
def agcarrito(cedula,nite,idpro,pedido):

    try:
        sql = "INSERT INTO carro (id_producto,cedula,cantidad,pedido) values " \
          "('" + str(idpro) + "','" + str(cedula) + "','" + str(nite) + "','"+str(pedido)+"');"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    except:
        return False



def visualcarrito(cedula):

    sql = "SELECT CARRO.ID_CARRITO,PRODUCTOS.NOMBREPROD,PRODUCTOS.IMAGEN,CARRO.CANTIDAD,(PRODUCTOS.PRECIO*CARRO.CANTIDAD) " \
          "AS SUBTOTAL FROM CARRO,PRODUCTOS WHERE CARRO.ID_PRODUCTO = PRODUCTOS.ID_PRODUCTO AND CARRO.CEDULA='"+str(cedula)+"';"
    #print("visual"+sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()


    return data

def vsubtotal(cedula):
    sql = "SELECT SUM(PRODUCTOS.PRECIO*CARRO.CANTIDAD) FROM CARRO,PRODUCTOS WHERE CARRO.ID_PRODUCTO = PRODUCTOS.ID_PRODUCTO AND CARRO.CEDULA='" + str(
        cedula) + "';"

    cursor = db.cursor()
    cursor.execute(sql)
    data1 = cursor.fetchall()
    for row in data1:
        stotal = row[0]

    return stotal

def prodgoogle():

    sql="select * from productos where tipo='M'"
    sql1 = "select * from productos where tipo='H'"

    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    cursor1 = db.cursor()
    cursor1.execute(sql1)
    data1 = cursor1.fetchall()


    return data,data1

#######metodos para conteo ###############

def numerogeneralpro():

    sql = "select count(*)as registros from productos;"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data



def numerogeneralproa():

    sql = "select count(*)as registros from productos where tipo='M';"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data

def numerogeneralprox():

    sql = "select count(*)as registros from productos where tipo='H';"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data

def cantidadcarrito(id):

    sql="SELECT count(*) from carro where cedula='"+str(id)+"';"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data


def eliminarcarrito(id,cedula):
    try:
        sql="delete from carro where id_carrito='"+str(id)+"' and cedula='"+str(cedula)+"';"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def factura(cedula,nump,subtotal,total,fecha,pedido):

    try:
        sql = "INSERT INTO factura (cedula,numproductos,subtotal,total,fecha,pedido) values " \
          "('" + str(cedula) + "','" + str(nump) + "','" + str(subtotal) + "','"+str(total)+"','"+str(fecha)+"','"+str(pedido)+"');"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)

        return True

    except:
        return False

def carritoel(cedula):
    try:
        sql="delete from carro where cedula='"+str(cedula)+"'"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True
    except:
        return False


def verfacturas(cedula):

    sql = "SELECT * FROM FACTURA WHERE CEDULA='"+str(cedula)+"';"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()

    return data


#select * from factura where cedula='1234567890'

def enviarcorreo(correo,mensaje,nombre):
    try:
        sql = "INSERT INTO mensaje (correo,nombre,detalle) values " \
              "('" + str(correo) + "','" + str(nombre) + "','" + str(mensaje) + "');"

        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    except:
        return False


def idpedido():

    sql = "select id_pedido from sec_pedidos order by id_pedido desc limit 1;"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data

def detallefacturainsert(cedula):

    try:
        sql = "INSERT INTO DETALLEFACT SELECT * FROM CARRO WHERE CEDULA='"+str(cedula)+"';"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    except:
        return False


def insertsecpedido(pedido):
    try:
        sql = "INSERT INTO SEC_PEDIDOS VALUES ('"+str(pedido)+"','A');"
        #print(sql)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        return True

    except:
        return False


def verdetallefact(cedula,fact):

    sql = "SELECT DETALLEFACT.CANTIDAD,PRODUCTOS.NOMBREPROD,"\
    "FACTURA.PEDIDO,PRODUCTOS.PRECIO,(PRODUCTOS.PRECIO*CAST(DETALLEFACT.CANTIDAD AS DOUBLE PRECISION)) AS TOTAL" \
    " ,FACTURA.FECHA FROM DETALLEFACT,PRODUCTOS,FACTURA,CLIENTES WHERE DETALLEFACT.ID_PRODUCTO=PRODUCTOS.ID_PRODUCTO AND " \
    "DETALLEFACT.PEDIDO=FACTURA.PEDIDO AND DETALLEFACT.CEDULA=CLIENTES.CEDULA AND FACTURA.ID_FACTURA='"+str(fact)+"' " \
    "AND DETALLEFACT.CEDULA='"+str(cedula)+"'"
    #print(sql)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    subtotal=0
    for row in data:
        fecha = row[5]
        subtotal=subtotal+row[4]
    return data,fecha,subtotal

#select id_factura from factura where cedula='5463656365' order by id_factura desc limit 1

def ultimafactura(cedula):

    sql = "select id_factura from factura where cedula='"+str(cedula)+"' order by id_factura desc limit 1"
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    for row in data:
        data = row[0]

    return data