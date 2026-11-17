from django.urls import path
from my_web import views

urlpatterns = [
    path('', views.home, name='home'),
    path('deals/', views.deals, name='deals'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout, name='logout'),
    path('products/', views.show_products, name='show_products'),
    path('categories/', views.show_categories, name='categories'),
    path('create_order/<int:pk>/', views.create_order, name='create_order'),
    path('get_products/', views.get_products, name='get_products'),
    path('categories/', views.categories, name='categories'),
    path('products/', views.products, name='products'),
    path('orders/', views.orders, name='orders'),
    path('get_order/', views.get_order, name='get_order'),

]