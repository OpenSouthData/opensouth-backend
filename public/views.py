from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework import status
from .models import *
from .serializers import *
from accounts.permissions import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from accounts.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from accounts.models import *
from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from accounts.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.




User = get_user_model()




class PublicCategoryView(APIView):

    permission_classes = [PublicPermissions]

    def get(self, request):
        categories = Categories.objects.filter(is_deleted=False).order_by('name')
        serializer = CategorySerializer(categories, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class PublicCategoryDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_deleted=False).order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'



class PublicOrganisationView(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False, status='approved').order_by('name')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):

        sort = request.GET.get('sort', None)

        
        queryset = self.filter_queryset(self.get_queryset())

        if sort == 'relevance':
            queryset = queryset.order_by('-views')

        if sort == 'most_recent':
            queryset = queryset.order_by('-created_at')

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)





class PublicOrganisationDetailView(generics.RetrieveAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False, status='approved').order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PublicDatasetView(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['category']
    search_fields = ['title', 'category__name', 'tags__name', 'organisation__name']

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):

        category = request.GET.get('category', None)
        organisation = request.GET.get('organisation', None)
        tags = request.GET.get('tags', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        format = request.GET.get('format', None)
        spatial_coverage = request.GET.get('spatial_coverage', None)
        sort = request.GET.get('sort', None)
        license = request.GET.get('license', None)

        
        queryset = self.filter_queryset(self.get_queryset())

        if sort == 'relevance':
            queryset = queryset.order_by('-views')

        if sort == 'creation_date':
            queryset = queryset.order_by('created_at')

        if sort == 'last_update':
            queryset = queryset.order_by('-updated_at')
        
        if license:
            queryset = queryset.filter(license=license)

        if category:
            queryset = queryset.filter(category__slug=category)

        if organisation:
            queryset = queryset.filter(organisation__slug=organisation)

        if tags:
            queryset = queryset.filter(tags__name=tags)

        if spatial_coverage:
            queryset = queryset.filter(spatial_coverage=spatial_coverage)

        if format:
            queryset = queryset.filter(format=format)

        if start_date and end_date:
            Start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            End_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            queryset = queryset.filter(created_at__range=[Start_date, End_date])


        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    

class PublicDatasetDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context






class PublicCounts(APIView):
    permission_classes = [PublicPermissions]

    def get(self, request):

        data = {

            "datasets": Datasets.objects.filter(is_deleted=False, status='published').count(),
            "organisations": Organisations.objects.filter(is_deleted=False, status='approved').count(),
            "users": User.objects.filter(is_deleted=False).count(),
            "categories": Categories.objects.filter(is_deleted=False).count(),
            "files": DatasetFiles.objects.filter(is_deleted=False).count(),
        }

        return Response(data, status=status.HTTP_200_OK)





class PopularDataset(APIView):

    permission_classes = [PublicPermissions]

    def get(self, request):

        views = Datasets.objects.filter(is_deleted=False, status='published').order_by('-views')[:9]
        serializer = DatasetSerializer(views, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK) 
    



class PublicNews(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    pagination_class = LimitOffsetPagination
    

class PublicNewsDetailView(generics.RetrieveAPIView):
    
    permission_classes = [PublicPermissions]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class PublicTagsView(generics.ListAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = TagsSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Tags.objects.filter(is_deleted=False).order_by('name')
    search_fields = ('name', 'slug')





class PublicUserDetailView(generics.RetrieveAPIView):

    permission_classes = [PublicPermissions]
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(is_deleted=False)
    lookup_field = 'pk'

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class PublicUserDataset(generics.ListAPIView):

    permission_classe = [PublicPermissions]
    serializer_class = DatasetSerializer
    queryset = Datasets.objects.filter(is_deleted=False, status='published').order_by('-created_at')
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            user = User.objects.get(pk=pk)
            
        except User.DoesNotExist:
            raise NotFound("user not found")
        
        return Datasets.objects.filter(is_deleted=False, status='published', user=user, type='individual').order_by('-created_at')




class PublicPopularOrganisationDataset(APIView):

    permission_classes = [PublicPermissions]
    authentication_classes = [JWTAuthentication]


    def get(self, request, pk):
        try:
            organisation = Organisations.objects.get(pk=pk)
        except Organisations.DoesNotExist:
            return Response({"error": "organisation not found"}, status=status.HTTP_404_NOT_FOUND)

        datasets = Datasets.objects.filter(is_deleted=False, status='published', organisation=organisation).order_by('-views')[:9]
        serializer = DatasetSerializer(datasets, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class PublicSupportSystem(APIView):

    permission_classes = [PublicPermissions]

    @swagger_auto_schema(methods=['POST'], request_body=SupportSerializer())
    @action(detail=False, methods=['POST'])
    def post(self, request):

        serializer = SupportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            type = 'public',
            subject = 'support'

        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class PublicLocationRequest(APIView):

    permission_classes = [PublicPermissions]

    def post(self, request, pk):

        country = request.GET.get('country', None)
        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset not found"}, status=status.HTTP_404_NOT_FOUND)

        if country is None:
            raise ValidationError("country is required")
        
        slug = slugify(country)
        
        if LocationAnalysis.objects.filter(slug=slug, dataset=dataset).exists():

            location = LocationAnalysis.objects.get(slug=slug, dataset=dataset)
            location.count += 1
            location.save()

            return Response({"message": "location updated"}, status=status.HTTP_200_OK)
        
        else:
            location = LocationAnalysis.objects.create(country=str(country).lower(), dataset=dataset, slug=slug)
            location.count += 1
            location.save()

            return Response({"message": "location updated"}, status=status.HTTP_200_OK)
        





class GetClientIP(APIView):

    def get(self, request):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        lang = request.GET.get('lang', None)
        id = request.GET.get('id', None)

        langs = lang

        if lang is None: 
            lang = 'en'

        if id:
            if langs is None:
                return Response({"error": "lang is required"}, status=403)
            
            cl_ip = ClientIP.objects.filter(pk=id).first()
            if not cl_ip:
                return Response({"error": "client ip not found"}, status=401)
            cl_ip.lang = langs
            cl_ip.save()

        else:
            if ClientIP.objects.filter(ip_address=ip).exists():

                cl_ip = ClientIP.objects.filter(ip_address=ip).first()
                cl_ip.lang = lang
                cl_ip.save()

            else:   
                cl_ip = ClientIP.objects.create(ip_address=ip, lang=lang if lang else 'en')


        data = {
            "status": "accepted",
            "lang_status": langs if langs else 'en- lang not provided',
            "instance": ClientIPSerializer(cl_ip).data

        }

        return Response(data, status=status.HTTP_200_OK)



        

        

        
