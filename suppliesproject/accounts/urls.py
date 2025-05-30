from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
# ↓ SignupViewのインポートを追加
from .views import SignupView

app_name = 'accounts' 

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # ↓この行を追加
    path('signup/', SignupView.as_view(), name='signup'),

]