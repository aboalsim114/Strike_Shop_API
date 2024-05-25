from django.shortcuts import render
from rest_framework import generics
from .models import User, categories, Products, Cart, ProductReview, payement, Order, OrderItem
from .serializers import UserSerializer, categoriesSerializer, ProductsSerializer, CartSerializer, ProductReviewSerializer, payementSerializer, OrderSerializer, OrderItemSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class categoriesList(generics.ListCreateAPIView):
    queryset = categories.objects.all()
    serializer_class = categoriesSerializer


class categoriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = categories.objects.all()
    serializer_class = categoriesSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class ProductsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer


class CartList(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ProductReviewList(generics.ListCreateAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class ProductReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer


class payementList(generics.ListCreateAPIView):
    queryset = payement.objects.all()
    serializer_class = payementSerializer


class payementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = payement.objects.all()
    serializer_class = payementSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
