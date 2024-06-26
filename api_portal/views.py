from django.shortcuts import render
from .serializers import *
from .models import *
import hashlib
from django.shortcuts import render
from .serializers import *
from .models import *
from django.db import IntegrityError
from accounts.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.permissions import *
from django.db.models import Q, Sum
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from accounts.permissions import *
import hashlib
from djoser.views import UserViewSet
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from rest_framework.pagination import LimitOffsetPagination
from accounts.serializers import CustomUserSerializer
import requests
import os
from rest_framework.response import Response
from main.serializers import *
from main.models import *
from .permissions import AuthHandler




# Create your views here.





class APIDatasetView(generics.ListAPIView):

    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'category__name', 'tags__name', 'organisation__name']


    def list(self, request, *args, **kwargs):

        user = AuthHandler(request)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DatasetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = DatasetSerializer(queryset, many=True)
        return Response(serializer.data)
    

