from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('inflows.urls')),
    path('api/v1/', include('outflows.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('supplier.urls')),
    path('api/v1/', include('vehicles.urls')),


    path('', include('home.urls')),
    path('product/', include('products.urls')),
    path('admin/', admin.site.urls),
]
