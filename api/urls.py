from django.urls import path
from .views import UserList, UserDetail, categoriesList, categoriesDetail, ProductsList, ProductsDetail, CartList, CartDetail, ProductReviewList, ProductReviewDetail, payementList, payementDetail, OrderList, OrderDetail
urlpatterns = [
    path('users/', UserList.as_view(), name='user_list'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user_detail'),
    path('categories/', categoriesList.as_view(), name='categories_list'),
    path('categories/<uuid:pk>/', categoriesDetail.as_view(),
         name='categories_detail'),
    path('products/', ProductsList.as_view(), name='products_list'),
    path('products/<uuid:pk>/', ProductsDetail.as_view(), name='products_detail'),
    path('cart/', CartList.as_view(), name='cart_list'),
    path('cart/<uuid:pk>/', CartDetail.as_view(), name='cart_detail'),
    path('payement/', payementList.as_view(), name='payement_list'),
    path('payement/<uuid:pk>/', payementDetail.as_view(), name='payement_detail'),
    path('order/', OrderList.as_view(), name='order_list'),
    path('order/<uuid:pk>/', OrderDetail.as_view(), name='order_detail'),
]
