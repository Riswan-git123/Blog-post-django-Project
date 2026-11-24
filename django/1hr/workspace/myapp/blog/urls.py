from django.urls import path
from . import views
app_name="blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<str:slug>/",views.detail, name="detail"),
    path("fg/",views.home,name="home"),
    path("about/",views.about,name="riswan"),
    path("contact",views.contact_view, name="contact"),
    path("about", views.about_view, name="about"),
    path("register",views.register, name="register"),
    path("login",views.login, name="login"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("newpost", views.new_post, name="newpost"),
    path("post/<int:post_id>/edit", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path("post/<int:post_id>/publish", views.toggle_post_published, name="toggle_post_published"),
    path("logout",views.logout,name="logout"),
    path("forgot_password",views.forgot_password,name="forgot_password"),
    path("reset_password/<uidb64>/<token>",views.reset_password,name="reset_password")
]
