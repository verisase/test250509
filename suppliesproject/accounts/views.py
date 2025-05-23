from django.shortcuts import render

# ↓ ここから追加（SignupViewに必要なインポートを追加）
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
# ↑ ここまで追加（SignupViewに必要なインポートを追加）

# Create your views here.

# ↓ここから追加（SignupViewを追加）
class SignupView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')
# ↑ここまで追加（SignupViewを追加）
