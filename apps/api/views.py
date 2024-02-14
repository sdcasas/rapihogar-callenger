from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import Value
from django.db.models.functions import Concat

from core.models import Company, Tecnico, Pedido


class CompanySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Company
        fields = '__all__'


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class PedidoViewSet(viewsets.ModelViewSet):
    http_method_names = ['put', ]
    serializer_class = PedidoSerializer
    queryset = Pedido.objects.all()


class TecnicoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['full_name', 'hours_worked', 'total_pedidos', 'total_payment']


class TecnicoList(APIView):

    def get(self, request, *args, **kwargs):
        tecnico_query = Tecnico.objects.all()
        query = self.request.query_params.get('query', None)
        if query:
            tecnico_query = (Tecnico.objects
                                    .annotate(fullname_search=Concat('apellido', Value(' '), 'nombre'))
                                    .filter(fullname_search__icontains=query))
        serializer = TecnicoSerializers(tecnico_query, many=True)
        return Response(serializer.data)
    

