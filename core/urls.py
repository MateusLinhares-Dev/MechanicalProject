from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # API URLs
    path('api/v1/', include('authentication.api_urls')),
    path('api/v1/', include('products.api_urls')),
    path('api/v1/', include('vehicles.api_urls')),

    # Web URLs
    path('', include('home.urls')),
    path('authentication/', include('authentication.urls')),
    path('product/', include('products.urls')),
    path('admin/', admin.site.urls),
    path('vehicles/', include('vehicles.urls')),
    path('services/', include('services.urls')),
    path('customers/', include('customers.urls')),
    path('inflows/', include('inflows.urls')),
    path('outflows/', include('outflows.urls')),
    path('supplier/', include('supplier.urls')),
]