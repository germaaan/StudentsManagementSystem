from flask import Flask
from nose.tools import *
import unittest
import os
import main
import tempfile
from flask.ext.testing import TestCase

class MainTestCase(unittest.TestCase):

    #Inicio del esqueleto principal de tests en Flask

    def setUp(self):
        self.db_fd, inicio.app.config['DATABASE'] = tempfile.mkstemp()
        inicio.app.config['TESTING'] = True
        self.app = inicio.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(inicio.app.config['DATABASE'])

    #Aqui acaba el esqueleto principal

    """
    Tests correspondientes a objetos Alumno
    """

    #Comprobamos que la petición GET de /alumnos es correcta
    def test_alumnos_get(self):
        respuesta = self.app.get('/alumnos')
        self.assertTrue(('dni' in str(respuesta.data)) or ('[]' in str(respuesta.data)))

    #Comprobamos que la petición GET de /alumnos/argumentos es correcta
    def test_alumnos_get_with_arg(self, dni='11223344A'):
        respuesta = self.app.get('/alumnos/'+dni)
        self.assertTrue('11223344A' in str(respuesta.data))


    #Comprobamos que la petición PUT de /alumnos es correcta
    def test_alumnos_put(self):
        respuesta = self.app.put('/alumnos')
        self.assertTrue('puting' in str(respuesta.data))

    #Comprobamos que la petición DELETE de /alumnos es correcta
    def test_alumnos_delete(self):
        respuesta = self.app.delete('/alumnos')
        self.assertTrue('deleting' in str(respuesta.data))

    #Comprobamos que la petición DELETE de /alumnos/argumentos es correcta
    def test_alumnos_delete_with_arg(self):
        respuesta = self.app.delete('/alumnos/11223344A')
        self.assertTrue('Elemento eliminado' in str(respuesta.data))

    #Comprobamos que la petición POST de /alumnos es correcta
    def test_alumnos_post(self):
        posibles_errores=[404, 400]
        respuesta1 = self.app.post('/alumnos&nombre=Juan&dni=45601218Z&direccion=Calle+arabl&localidad=Jerez+de+la+frontera&provincia=Granada&fecha_nac=1988-2-6&telefono=677164459')
        respuesta2 =
        respuesta3 =
        self.assertTrue('OK' in str(respuesta.data) or respuesta.status_code in posibles_errores)  #agnadir lo que queda de elementos
        if 'OK' in str(respuesta.data):
            test_alumnos_get_with_arg('45601218Z')


    """
    Tests correspondientes a objetos Profesor
    """




    #Ver si la página carga correctamente
    def test_home_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.get('/')
        # assert the status code of the response
        self.assertEqual(result.status_code, 200)


if __name__ == '__main__':
    unittest.main()
