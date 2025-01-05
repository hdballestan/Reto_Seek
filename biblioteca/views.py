import datetime
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .models import Book
from .serializers import BookAvgPriceSerializer, BookDetailSerializer, BookSerializer
from utils.constants import get_pipeline
from utils.mongo_connection import MongoDBConnection


class ObtainAuthTokenView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description="Obtiene el token de autenticación para el usuario.",
        responses={
            200: BookSerializer,  
            400: 'Solicitud incorrecta, falta el nombre de usuario o contraseña.',
            401: 'Credenciales inválidas.',
            404: 'Usuario inactivo.'
        }
    )
    def post(self, request):
        """
        Obtiene un token JWT de acceso y refresco para el usuario proporcionado.
        Si el usuario no existe o la contraseña es incorrecta, se devuelve un error de autenticación.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"detail": "User is inactive."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class BookListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description="Obtiene una lista paginada de libros.",
        responses={200: BookSerializer(many=True), 401: 'Acceso no autorizado.'},
    )
    def get(self, request):
        """
        Devuelve una lista de libros paginada. Solo los usuarios autenticados pueden acceder a esta vista.
        """
        paginator = CustomPagination()
        books = Book.objects.all()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        description="Crea un nuevo libro.",
        request=BookSerializer,
        responses={201: BookSerializer, 400: 'Datos inválidos.'},
    )
    def post(self, request):
        """
        Crea un nuevo libro en la base de datos. Requiere autenticación y datos válidos.
        """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        """
        Obtiene el libro según el ID proporcionado. Retorna None si no existe.
        """
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    @extend_schema(
        description="Obtiene los detalles de un libro por su ID.",
        responses={200: BookDetailSerializer, 404: 'Libro no encontrado.'},
    )
    def get(self, request, pk):
        """
        Obtiene los detalles de un libro específico por su ID. Si no se encuentra el libro, se retorna un error 404.
        """
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookDetailSerializer(book)
        return Response(serializer.data)

    @extend_schema(
        description="Actualiza los detalles de un libro.",
        request=BookDetailSerializer,
        responses={200: BookDetailSerializer, 400: 'Datos inválidos.', 404: 'Libro no encontrado.'},
    )
    def put(self, request, pk):
        """
        Actualiza los detalles de un libro existente. Si no se encuentra el libro, se retorna un error 404.
        """
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookDetailSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        description="Elimina un libro por su ID.",
        responses={204: 'Libro eliminado exitosamente.', 404: 'Libro no encontrado.'},
    )
    def delete(self, request, pk):
        """
        Elimina un libro por su ID. Si el libro no existe, se retorna un error 404.
        """
        book = self.get_object(pk)
        if not book:
            return Response({"detail": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookAvgPriceByYearView(APIView):
    @extend_schema(
        description="Obtiene el precio promedio de los libros publicados en un año específico.",
        responses={
            200: 'Precio promedio de libros por año.',
            404: 'No se encontraron libros publicados en el año proporcionado.',
            500: 'Error interno del servidor.'
        }
    )
    def get(self, request, year):
        """
        Devuelve el precio promedio de los libros publicados en el año solicitado.
        Si no se encuentran libros, retorna un error 404. Si ocurre un error, se retorna un error 500.
        """
        try:
            # Conexión a MongoDB
            with MongoDBConnection() as client:
                collection = client["biblioteca_db"]["biblioteca_book"]

                start_date = datetime.datetime(int(year), 1, 1)
                end_date = datetime.datetime(int(year), 12, 31, 23, 59, 59)

                pipeline = get_pipeline(start_date, end_date)
                results = list(collection.aggregate(pipeline))

            if not results:
                return JsonResponse(
                    {"mensaje": f"No se encontraron libros publicados en el año {year}."}, 
                    status=404
                )

            return JsonResponse(results, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



