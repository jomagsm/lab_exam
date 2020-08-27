"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from webapp.view.product_views import IndexView, view_product, product_create_view, product_update_view, product_delete_view, \
    filter_name_view, filter_category

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('view/<int:pk>/', view_product, name='view'),
    path('product_create/', product_create_view, name='product_create'),
    path('product_update/<int:pk>',product_update_view, name='product_update'),
    path('product_delete/<int:pk>', product_delete_view, name='product_delete'),
    path('filter_name/<category>', filter_name_view, name='filter_name'),
    path('filter_category/<category>', filter_category, name='filter_category')
]
