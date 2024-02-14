import json

from rest_framework import viewsets, serializers, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


from django.db.models import Value
from django.db.models.functions import Concat
from django.http import HttpResponse

from core.models import Company, Tecnico, Pedido
from core.services import TecnicoServices


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


@api_view()
@permission_classes([permissions.IsAuthenticated])
def tecnico_informe(request):
    service = TecnicoServices()
    to_json = {
        "avg": service.get_avg(),
        "min": service.get_min(),
        "max": service.get_max(),
        "get_technicians_lt_avg": service.get_technicians_lt_avg(),
    }
    return HttpResponse(json.dumps(to_json), content_type='application/json')