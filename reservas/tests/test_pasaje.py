from django.test import TestCase, Client
from django.urls import reverse
from reservas.models.ruta import Ruta
from reservas.models.pasaje import Pasaje
from usuarios.models import Usuario

# lista_viajeros
# agregar_viajero
# editar_viajero
# eliminar_viajero
    
class PasajeUnitTest(TestCase):
    def setUp(self):
        rutao = Ruta.objects.create(
            lugar = 'La Habana',
        )
        rutad = Ruta.objects.create(
            lugar = 'Las Villas',
        )

        self.viajero = Pasaje.objects.create(
            origen = rutao,
            destino = rutad,
            precio = 100,
            capacidad = 40,
            fecha = '2/4/2024',
            transporte = 'BU'
        )
        
    def test_model(self):
        # Configura el objeto de prueba
        pasaje = Pasaje.objects.first()
        self.assertEqual(pasaje.precio, 100)
        self.assertEqual(pasaje.capacidad, 40)
        self.assertEqual(pasaje.fecha, '2/4/2024')
        self.assertEqual(pasaje.transporte, 'BU')
        self.assertEqual(pasaje.origen.lugar, 'La Habana')
        self.assertEqual(pasaje.destino.lugar, 'Las Villas')

class ViajeroTestCase(TestCase):
    def setUp(self):
        # Configura el entorno de prueba
        self.client = Client()
        self.usuario = Usuario.objects.create_superuser(username='admin', password='admin')

        rutao = Ruta.objects.create(
            lugar = 'La Habana',
        )
        
        rutad = Ruta.objects.create(
            lugar = 'Las Villas',
        )
        
    def test_get_ok(self):
        self.client.login(username='admin', password='admin')
        
        # Obtener la URL de la vista
        url = reverse('lista_viajeros')
        # Realizar la solicitud GET a la vista
        response = self.client.get(url)
        # Verificar que la respuesta es 200 OK
        self.assertEqual(response.status_code, 200)
        # Verificar que la plantilla correcta se esté utilizando
        self.assertTemplateUsed(response, 'pasajes/lista_viajeros.html')
        # Verificar que los usuarios estén en el contexto de la respuesta
        viajeros_en_contexto = response.context['viajeros']
        self.assertEqual(len(viajeros_en_contexto), 2)
        # Verificar que los datos de los usuarios estén en el contenido de la respuesta
        self.assertContains(response, 'Carlos Brayan')
        self.assertContains(response, 'Javier Gonzalez')
        
    def test_form_post(self):
        self.client.login(username='admin', password='admin')
        
        # Aquí debes definir los datos que enviarás en la petición POST
        data = {
            'ci': '01210598724',
            'nombre': 'Alejandro Santana',
        }
        
        # Utiliza reverse para obtener la URL basada en el nombre de la vista
        url = reverse('agregar_viajero')
        urlr = reverse('lista_viajeros')
        
        # Realiza la petición POST con el cliente de prueba
        response = self.client.post(url, data)
        
        # Aquí verificar la respuesta
        # Verificar que la respuesta redirige a la URL correcta
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, urlr)
        
        # Verifica que se creo correctamente en la base de datos
        objeto_creado = Viajero.objects.filter(ci='01210598724', nombre='Alejandro Santana').exists()
        self.assertTrue(objeto_creado)