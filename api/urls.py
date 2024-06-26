from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserList, UserDetail, categoryListView, UserProfileView, categoriesDetail, 
    ProductsList, ProductsDetail, CartList, CartDetail, ProductReviewList, 
    ProductReviewDetail, payementList, payementDetail, OrderList, OrderDetail, 
    RegisterView, LoginView
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user_detail'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('categories/', categoryListView.as_view(), name='category-list'),
    path('categories/<uuid:pk>/', categoriesDetail.as_view(), name='categories_detail'),
    path('products/', ProductsList.as_view(), name='products_list'),
    path('products/<uuid:pk>/', ProductsDetail.as_view(), name='products_detail'),
    path('cart/', CartList.as_view(), name='cart_list'),
    path('cart/<uuid:pk>/', CartDetail.as_view(), name='cart_detail'),
    path('reviews/', ProductReviewList.as_view(), name='review_list'),
    path('reviews/<uuid:pk>/', ProductReviewDetail.as_view(), name='review_detail'),
    path('payments/', payementList.as_view(), name='payment_list'),
    path('payments/<uuid:pk>/', payementDetail.as_view(), name='payment_detail'),
    path('orders/', OrderList.as_view(), name='order_list'),
    path('orders/<uuid:pk>/', OrderDetail.as_view(), name='order_detail'),
    # Authentification JWT-------------------------------------------------------------
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]

