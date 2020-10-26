from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Tutorial
from .serializers import TutorialSerializer, MyTokenObtainPairSerializer, CustomUserSerializer
# Create your views here.


class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class CustomUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeView(APIView):
    
    def get(self, request):
        return Response(data={"Hello":"World"}, status=status.HTTP_200_OK)


class LogoutAndBlacklist(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def tutorial_list(request):
    if request.method == "GET":
        tutorials = Tutorial.objects.all()

        title = request.GET.get("title", None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
    elif request.method == "POST":
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        count = Tutorial.objects.all().delete()
        return JsonResponse({"message": "{} Tutorials were deleted successfully!".format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
def tutorial_detail(request, pk):
    try:
        tutorial = Tutorial.objects.get(pk=pk)
    except Tutorial.DoesNotExist:
        return JsonResponse({"message": "The tutorial does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET" and request.user.is_authenticated:
        tutorial_serializer = TutorialSerializer(tutorial)
        return JsonResponse(tutorial_serializer.data)
    
    elif request.method == "PUT":
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data) 
    
    elif request.method == "DELETE":
        tutorial.delete()
        return JsonResponse({"message": "Tutorial was deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)

    if request.method == "GET":
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)