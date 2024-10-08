from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from .models import User, categories, Products, Cart, ProductReview, Payment, Order, OrderItem
from .serializers import UserSerializer, categoriesSerializer, ProductsSerializer, CartSerializer, ProductReviewSerializer, PaymentSerializer, OrderSerializer, OrderItemSerializer, RegisterSerializer,CreatePaymentIntentSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import stripe
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView


stripe.api_key = settings.STRIPE_SECRET_KEY
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class categoryListView(generics.ListCreateAPIView):
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

class ProductReviewListByProduct(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductReview.objects.filter(product_id=product_id)

class payementList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class payementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "message": "User registered successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):
    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password.'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)  # Log the user in to create a session
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
            return Response(response_data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    



class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    









class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            # Créer la commande associée
            order = Order.objects.create(
                user=request.user,
                total_amount=data['amount'],
                status='pending'  # ou un autre statut par défaut
            )

            # Créer un nouveau PaymentIntent sans redirections
            intent = stripe.PaymentIntent.create(
                amount=int(data['amount'] * 100),  # Montant en centimes
                currency=data['currency'],
                payment_method=data['payment_method_id'],
                confirm=True,
                automatic_payment_methods={"enabled": True, "allow_redirects": "never"},
                # Désactivation des redirections explicites
                payment_method_options={
                    "card": {
                        "request_three_d_secure": "automatic",  # Demande automatique 3D Secure uniquement si nécessaire
                    }
                }
            )

            # Sauvegarder le PaymentIntent et l'ordre
            Payment.objects.create(
                order=order,
                stripe_payment_intent_id=intent.id,
                amount=data['amount'],
                payment_status='pending'
            )

            return Response({'clientSecret': intent['client_secret']}, status=status.HTTP_200_OK)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)






class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retourner uniquement les commandes de l'utilisateur connecté
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ongoing_orders = queryset.filter(status='pending')
        past_orders = queryset.filter(status__in=['completed', 'canceled'])

        return Response({
            'ongoing_orders': OrderSerializer(ongoing_orders, many=True).data,
            'past_orders': OrderSerializer(past_orders, many=True).data
        })