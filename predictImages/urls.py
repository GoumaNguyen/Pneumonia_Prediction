from django.urls import path
from . import views

urlpatterns = [
    path("index/", views.index, name="app-index"),
    path("predict/", views.predict_image, name="app-predict"),  # Thêm đường dẫn cho API dự đoán
]
