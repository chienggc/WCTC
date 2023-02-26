
from django.urls import path
from . import views
from members.views import user_login



urlpatterns = [
    path('', user_login, name="login"),
    path('add_product', views.add_product, name="add-product"),
    path('list_product', views.list_products, name="list-products"),
    path('reedem_product/<prod_id>', views.reedem_product, name="reedem-product"),
    path('list_redemption', views.list_redemption, name="list_redemption"),
    path('update_redemption/<redemption_id>/<status>', views.update_redemption, name="update-redemption"),
    path('edit_product/<product_id>', views.edit_product, name="edit-product"),
    path('delete_product/<product_id>', views.delete_product, name="delete-product"),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='authenticate/change-password.html')),
    path('password/', views.PasswordsChangeView.as_view(template_name='authenticate/change-password.html')),
    path('password_success/', views.password_success, name='password_success'),
]
