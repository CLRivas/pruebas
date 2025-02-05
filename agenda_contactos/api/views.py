from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# modelos
from app.models import Usuario
# serializers
from .serializers import UsuarioSerializers


class UsuarioAPIView(APIView):

    def get(self, request):
        key = request.GET
        afiliados =Usuario.objects.all()  # con orm
        total = afiliados.count()

        columns=['id','nombre','apellido','email','celular']

        if 'order[0][column]' in key:
            order=columns[int(key['order[0][column]'])]
        if key['order[0][dir]']=='desc':
            order='-'+order
        afiliados= Usuario.objects.all().order_by(order)

        if len(key['search[value]']) > 0:
            afiliados = (Usuario.filter(nombre__icontains=key['search[value]']) | afiliados.filter(apellido__icontains=key['search[value]'])
            | afiliados.filter(identificacion__icontains=key['search[value]']) | afiliados.filter(celular__icontains=key['search[value]']))
        total_filtrado=afiliados.count()
        if 'start' in key:
            l_0=int(key['start'])
            l_1=l_0+int(key['length'])
            if l_1>total:
                l_1=total
            afiliados=afiliados[l_0:l_1]
        afiliados_serializados = UsuarioSerializers(afiliados, many=True).data
        data = {
                "recordsTotal": total,
                "recordsFiltered": total_filtrado,
                "data": afiliados_serializados
                }
        if data != None:
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        afiliados_serializados = UsuarioSerializers(data=request.data)
        user = request.user

        if afiliados_serializados.is_valid():
            celular = request.data.get('celular')
            if Usuario.objects.filter(celular=celular).exists():
                return Response(
                    {"detail": "El celular ya está registrado."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if user.is_authenticated:
                afiliados_serializados.save(user_created=request.user)
            else:
                afiliados_serializados.save(user_created=None)

            return Response(afiliados_serializados.data, status=status.HTTP_201_CREATED)
        
        return Response(afiliados_serializados.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


class UsuarioEdicionAPIView(APIView):
    def put(self, request, pk):
        afiliado = Usuario.objects.filter(id=pk).first()
        afiliado_serializado = UsuarioSerializers(afiliado, data= request.data)
        user = request.user
        if afiliado_serializado.is_valid():
            if user.is_authenticated:
                afiliado_serializado.save(user_created=request.user)
            else:
                afiliado_serializado.save(user_created=None)
            return Response(afiliado_serializado.data)
        return Response(afiliado_serializado.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        afiliado = Usuario.objects.filter(id=pk).first()
        afiliado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)