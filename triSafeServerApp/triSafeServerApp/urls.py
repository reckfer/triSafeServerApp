"""triSafeServerApp URL Configuration

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

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.conf.urls import url
from cliente.views import ClienteViewSet
# from cliente.models import Cliente
from django.conf.urls import url, include
from rest_framework import routers

# # Serializers define the API representation.
# class ClienteSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Cliente
#         fields = ('nome', 'endereco')

# # ViewSets define the view behavior.
# class ClienteViewSet(viewsets.ModelViewSet):
#     queryset = Cliente.objects.all()
#     serializer_class = ClienteSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'clientes/incluir/', ClienteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    
]

urlpatterns = [
    # url(r'^$', home),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # url(r'^home/', home),
    # url(r'^api-auth/', include('rest_framework.urls')),

]