from logging import Formatter
import unittest
from django.test import Client

class PropertyTestCase(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_filter_error(self):
        request_filter = {'year': 2011, 'city': 'medellin and estado="vnedido'}
        response = self.client.post(
            '/properties/filters', request_filter,  format='json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['detail'], "Error with params")

    def test_filter_year_city(self):
        request_filter = {'year': 2011, 'city': 'medellin'}
        response = self.client.post(
            '/properties/filters', request_filter,  format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['inmuebles'][0], {'direccion': 'carrera 100 #15-90', 'ciudad': 'medellin', 'estado': 'en_venta',
                                                           'precio_venta': 325000000, 'descripción': 'Amplio apartamento en conjunto cerrado'})

    def test_filter_not_found(self):
        request_filter = {'status': 2011}
        response = self.client.post(
            '/properties/filters', request_filter,  format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['inmuebles'], [])

    def test_filter_status(self):
        request_filter = {'status': 'pre_venta'}
        response = self.client.post(
            '/properties/filters', request_filter,  format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['inmuebles'][1], {'direccion': 'calle 23 #45-67', 'ciudad': 'medellin', 'estado': 'pre_venta',
                                                           'precio_venta': 210000000, 'descripción': ''})
        self.assertEqual(response.json()['inmuebles'][2], {'direccion': 'carrera 100 #15-90', 'ciudad': 'barranquilla', 'estado': 'pre_venta',
                                                           'precio_venta': 35000000, 'descripción': ''})

    def test_filter_year(self):
        request_filter = {'year':2011}
        response = self.client.post('/properties/filters', request_filter,  format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['inmuebles'][0], {'direccion': 'carrera 100 #15-90', 'ciudad': 'bogota', 'estado': 'en_venta',
                                           'precio_venta': 350000000, 'descripción': 'Amplio apartamento en conjunto cerrado'})
    
    def test_available(self):
        response = self.client.post('/properties/available', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['inmuebles'][0], {'direccion': 'carrera 100 #15-90', 'ciudad': 'bogota', 'estado': 'en_venta',
                                              'precio_venta': 350000000, 'descripción': 'Amplio apartamento en conjunto cerrado'})

