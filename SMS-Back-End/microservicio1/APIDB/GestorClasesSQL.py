# -*- coding: utf-8 -*-
"""
Last mod: Feb 2016
@author: Juan A. Fernández
@about: Fichero de creación de la interfaz de interacción con la entidad Clase de la base de datos.
"""

import MySQLdb
#Doc here: http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
from Clase import *
from Asignatura import *
from Alumno import *
from Profesor import  *
#Uso de variables generales par la conexión a la BD.
import dbParams

#Variable global de para act/desactivar el modo verbose para imprimir mensajes en terminal.
v=1

'''Clase controladora de Clases. Que usando la clase que define el modelo de Clase (la info en BD que de el se guarda)
ofrece una interfaz de gestión que simplifica y abstrae el uso.
'''
class GestorClases:
    """
    Manejador de Cursos de la base de datos.
    """

    @classmethod
    def nuevaClase(self, curso, grupo, nivel):
        '''
        Introduce una nueva clase en la base de datos. Son necesarios los tres primeros parámetros.
        '''

        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        #query="INSERT INTO Curso values("+"'"+nombre+"', "+ "'"+id+"');"

        #Añadimos al principio y al final una comilla simple a todos los elementos.
        curso='\''+curso+'\''
        grupo='\''+grupo+'\''
        nivel='\''+nivel+'\''

        query="INSERT INTO Clase VALUES(NULL,"+curso+","+grupo+","+nivel+");"
        if v:
            print '\n'+query
        cursor = db.cursor()
        salida =''
        '''
        Como la ejecución de esta consulta (query) puede producir excepciones como por ejemplo que el Clase con clave
        que estamos pasando ya exista tendremos que tratar esas excepciones y conformar una respuesta entendible.
        '''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==1062:
            return 'Elemento duplicado'

    @classmethod
    def getClases(self):
        '''
        Devuelve una lista con todas las clases registradas en la base de datos.

        @future:
        Podría pasarse un par de parámetros curso y nivel que por defecto fueran null para aumentar
        la flexibilidad de esta clase y que permitiera buscar  todas las clases de un nivel o de un curso
        en concreto.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#

        query="select * from Clase"
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            clase = Clase()
            clase.id=row[0]
            clase.curso=row[1]
            clase.grupo=row[2]
            clase.nivel=row[3]


            lista.append(clase)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        #Devolvemos la lista al completo.
        return lista

    @classmethod
    def getClase(self, idClase):
        '''
        Recupera TODA la información de un Clase en concreto a través de  su clave primaria.
        Aunque ahora sea poca información, la misión de esta función es traer toda la información de esa asignatura en lugar
        de la versión reducida que trae getClases.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        idClase='\''+idClase+'\''
        query="select * from Clase where id="+idClase+";"
        if v:
            print '\n'+query
        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        cursor.close()
        db.close()

        if salida==1:
            #Como se trata de toda la información al completo usaremos todos los campos de la clase Curso.
            #La api del mservicio envia estos datos en JSON sin comprobar nada
            clase = Clase()
            clase.id=row[0]
            clase.curso=row[1]
            clase.grupo=row[2]
            clase.nivel=row[3]


            return clase
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def modClase(self, idClase, campoACambiar, nuevoValor):
        '''
        Esta función permite cambiar cualquier atributo de un Clase.
        Parámetros:
        campoACambiar: nombre del atributo que se quiere cambiar
        nuevoValor: nuevo valor que se quiere guardar en ese campo.
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()

        idClase='\''+idClase+'\''

        #Al parámetro campoACambiar no se le añaden comillas para no generar un error de sintaxis en MySQL.
        nuevoValor='\''+nuevoValor+'\''

        query="UPDATE Clase SET "+campoACambiar+"="+nuevoValor+" WHERE id="+idClase+";"
        if v:
            print '\n'+query

        cursor = db.cursor()
        salida =''
        #Manejo de excepciones.
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        #Efectuamos los cambios
        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        elif salida==1062:
            return 'Elemento duplicado'
        elif salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def delClase(self, idClase):
        if v:
            print "Intentado eliminar Clase con id "+str(idClase)
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="delete from Clase  WHERE id="+idClase+";"
        salida =''
        try:
            salida = cursor.execute(query);
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)

        db.commit()
        cursor.close()
        db.close()

        if salida==1:
            return 'OK'
        if salida==0:
            return 'Elemento no encontrado'

    @classmethod
    def getNumClases(self):
        '''Devuelve el número de clases de la BD'''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db); #La conexión está clara.
        cursor = db.cursor()
        query="select count(*) from Clase;"
        salida =''
        try:
            salida = cursor.execute(query);
            row = cursor.fetchone()
        except MySQLdb.Error, e:
            # Get data from database
            try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                print "Error number: "+str(e.args[0])
                salida=e.args[0]
            except IndexError:
                print "MySQL Error: %s" % str(e)



        #print str(cursor)
        db.commit()

        #print cursor.fetchone()
        cursor.close()
        db.close()

        if salida==1:
            return row[0]
        if salida==0:
            return 'Elemento no encontrado'



    @classmethod
    def getAsignaturas(self, idClase):
        """

        Devuelve una lista con las asignaturas que se dan a esa clase.
        Ejemplo:
        En 2ºESO se da Frances, Lengua, etc...

        Parámetros:
            curso, grupo y nivel: identificadores que forman el unívoco de una clase.

        Devuelve: Una lista de objetos de tipo asignatura

        """
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()

        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idClase='\''+idClase+'\''
        query='select * from Asignatura where id in (select id_asignatura from Ascoia where id_clase ='+idClase+')'
        if v:
            print '\n'+query


        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            asignatura = Asignatura()
            asignatura.id=row[0]
            asignatura.nombre=row[1]
            lista.append(asignatura)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getAlumnos(self, idClase):
        '''
        Devuelve una lista con los alumnos matriculados en esa clase.
        Campos devueltos: id, nombre, apellidos y dni
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()
        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idClase='\''+idClase+'\''
        '''
        Usamos la orden distinct para eliminar los duplicados de una consulta, en este caso id_alumno ya que aparecerá
        que un mismo alumno está matriculado muchas veces en un mismo curso con asignaturas disintas, entonces para evitar
        contabilizar esos repetidos, usamos esta orden.
        '''
        query='SELECT id, nombre, apellidos, dni FROM Alumno where id in (select distinct id_alumno from Matricula where id_clase='+idClase+')'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            alumno = Alumno()
            alumno.nombre=row[0]
            alumno.id=row[1]

            lista.append(alumno)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.close()

        return lista

    @classmethod
    def getProfesores(self, idClase):
        '''
        Devuelve la lista de profesores que están impartien a esa clase.
        Devuelve dni, nombre y apellidos
        '''
        db = MySQLdb.connect(dbParams.host, dbParams.user, dbParams.password, dbParams.db)
        cursor = db.cursor()
        #Sacando los acentos...........
        mysql_query="SET NAMES 'utf8'"
        cursor.execute(mysql_query)
        #-----------------------------#
        idClase='\''+idClase+'\''
        query='SELECT dni, nombre, apellidos from Profesor where dni in (select id_profesor from Imparte where id_clase ='+idClase+')'
        if v:
            print '\n'+query
        cursor.execute(query)
        row = cursor.fetchone()

        lista = []

        while row is not None:
            profesor = Profesor()
            profesor.nombre=row[0]
            profesor.id=row[1]

            lista.append(profesor)
            #print row[0], row[1]
            row = cursor.fetchone()

        cursor.close()
        db.cl
