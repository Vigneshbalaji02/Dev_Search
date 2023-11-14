from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import Projectserializers
from web.models import Project
from api import serializers

from rest_framework import status


@api_view(['GET'])

def getroutes(request):
    routes=[
        {'GET':'api/web'},
        {'GET':'api/web/id'},
        {'GET':'api/web/id/vote'},

        {'GET':'api/users/token'},
        {'GET':'api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET', 'POST'])

def getproject(request):
    if request.method == "GET":
        projects=Project.objects.all()
        serializers=Projectserializers(projects, many=True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        serializer=Projectserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def getprojects(request,pk):
        projects=Project.objects.get(id=pk)
        serializers=Projectserializers(projects, many=False)
        return Response(serializers.data)
    
