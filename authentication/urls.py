from django.urls import path

from .views import login_view, register_view, logout_view, otp_view, forget_password_view, user_stats

urlpatterns = [
    path('login', login_view.user_login, name="login"),
    path('register', register_view.user_register, name="register"),
    path('forget_password', forget_password_view.forget_password, name="forget_password"),
    path('send_otp', otp_view.send_otp, name="send_otp"),
    path('verify_otp', otp_view.verify_otp, name="verify_otp"),
    path('logout', logout_view.user_logout, name="logout"),
    path('user_stat', user_stats.get_stat, name="user_stat"),
]
