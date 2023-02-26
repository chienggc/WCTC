
from django.urls import path
from . import views
from .views import UserEditView, AdminEditView, AwardListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name="user_login"),
    path('user_logout', views.user_logout, name="user_logout"),
    path('register_user', views.register_user, name="register_user"),
    path('edit_profile', UserEditView.as_view(), name="edit_profile"),
    path('edit_profile/<user_id>', views.AdminEditView, name="admin_edit_profile"),
    path('list_profile', views.list_user, name="list_profile"),
    path('edit_award/<award_id>', views.edit_award, name="edit_award"),
    path('delete_award/<award_id>', views.delete_award, name="delete_award"),
    path('add_award', views.add_award, name="add_award"),
    path('list_award', AwardListView.as_view(), name="list_award"),
    path('give_award/<user_id>', views.give_award, name="give_award"),
    path('dashboard', views.dashboard, name="dash_board"),
]
