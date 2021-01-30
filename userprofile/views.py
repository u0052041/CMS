from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import UserProfile
from .serializers import UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_vip = request.data.get("is_vip")
        instance.userprofile.is_vip = is_vip
        instance.userprofile.save(update_fields=["is_vip"])
        return Response(status=status.HTTP_200_OK)