from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'gender', 'price']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookAvgPriceSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    avg_price = serializers.DecimalField(max_digits=10, decimal_places=2)
