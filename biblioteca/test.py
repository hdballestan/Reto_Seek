from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book
from rest_framework_simplejwt.tokens import RefreshToken

class BookTests(APITestCase):
    def setUp(self):
        """
        Configura el usuario de prueba y crea un libro para las pruebas.
        """
        self.user = User.objects.create_user(username='testuser', password='t18$V3Y9]lE)')
        
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': '2020-01-01',
            'price': 19.99,
            'gender': 'Fiction'  # Agregar campo obligatorio 'gender'
        }

        self.token = self._get_jwt_token(self.user)

    def _get_jwt_token(self, user):
        """
        Método auxiliar para obtener el token JWT del usuario.
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_book(self):
        """
        Prueba para crear un libro.
        """
        url = reverse('book-list-create')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.post(url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['title'], self.book_data['title'])
        self.assertEqual(response.data['author'], self.book_data['author'])
        self.assertEqual(response.data['gender'], self.book_data['gender'])  # Verificar que el campo 'gender' se guardó

    def test_get_book_detail(self):
        """
        Prueba para obtener los detalles de un libro.
        """
        book = Book.objects.create(**self.book_data)
        
        url = reverse('book-detail', args=[book.id])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['title'], book.title)
        self.assertEqual(response.data['author'], book.author)
        self.assertEqual(response.data['gender'], book.gender)  # Verificar que 'gender' está en la respuesta

    def test_get_book_not_found(self):
        """
        Prueba para obtener un libro que no existe (404).
        """
        url = reverse('book-detail', args=[999])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized_create_book(self):
        """
        Prueba para crear un libro sin autenticación (401).
        """
        url = reverse('book-list-create')

        response = self.client.post(url, self.book_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_get_book_detail(self):
        """
        Prueba para obtener los detalles de un libro sin autenticación (401).
        """
        book = Book.objects.create(**self.book_data)
        
        url = reverse('book-detail', args=[book.id])

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


