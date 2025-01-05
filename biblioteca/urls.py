from django.urls import path
from .views import BookListCreateView, BookDetailView, BookAvgPriceByYearView, ObtainAuthTokenView

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/avg-price/<int:year>/', BookAvgPriceByYearView.as_view(), name='avg-price-by-year'),
    path('auth-token/', ObtainAuthTokenView.as_view(), name='auth-token'),
]
