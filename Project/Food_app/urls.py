from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'Home'),
    path('register/', views.register, name = 'Register'),
    path('category/', views.category, name = 'Category'),
    path('category/<str:name>', views.categoryview, name = 'Category'),
    path('category/<str:cname>/<str:pname>', views.productdetail, name = 'Product_detail'),
    path('login/', views.login_page, name = 'Login'),
    path('logout/', views.logout_page, name = 'Logout'),
    path('addtocart/', views.add_to_cart, name = 'AddToCart'),
    path('cart/', views.cart_page, name = 'Cart'),
    path('removecart/<int:Cartid>', views.remove_cart, name = 'RemoveCart'),
    path('addtofav', views.add_to_fav, name = 'AddToFav'),
    path('favourite', views.favourite_page, name = 'Favourite'),
    path('removefav/<int:favid>', views.remove_fav, name = 'RemoveFav')
]