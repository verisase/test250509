from django.urls import path
from . import views

urlpatterns = [
    path('supplies/', views.ListSuppliesView.as_view(), name='list-supplies'),
    path('supplies/<int:pk>/detail/', views.DetailSuppliesView.as_view(), name='detail-supplies'),
    path('supplies/create/', views.CreateSuppliesView.as_view(), name='create-supplies'),
    path('supplies/<int:pk>/update/', views.UpdateSuppliesView.as_view(), name='update-supplies'),
    path('supplies/<int:pk>/delete/', views.DeleteSuppliesView.as_view(), name='delete-supplies'),
    path('supplies/<int:supplies_id>/review/', views.CreateReviewView.as_view(), name='create-review'),
    path('', views.index_view, name='index'),
    path('review/<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete-review'),  

]

