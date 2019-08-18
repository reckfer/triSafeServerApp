from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from .models import Cliente
from rest_framework.renderers import JSONRenderer
import json

class ClienteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cliente
        fields = ('nome', 'endereco')

# ViewSets define the view behavior.
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
    @action(detail=False)
    def obter(self, request):
        idCliente = 560
        return Response(Cliente.obter(self, idCliente))

    @action(detail=False)
    def recent_users(self, request):
        
        #json = JSONRenderer().render()
        return Response({"a": "abc"})
        #return Response(json.dumps({"a": "b"}))

