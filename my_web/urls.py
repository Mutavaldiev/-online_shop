from django.urls import path
from my_web import views



urlpatterns = [
    path('', views.home, name='home'),
    path('deals/', views.deals, name='deals'),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('products/', views.products, name='products'),
    path('categories/', views.show_categories, name='categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-product/', views.add_product, name='add_product'),
    path('order/<int:pk>/', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:pk>/edit/', views.update_order, name='update_order'),
    path('orders/<int:pk>/delete/', views.delete_order, name='delete_order'),
]
