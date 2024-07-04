from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from accounts.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from accounts.models import *
from accounts.serializers import *
from accounts.serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from .email import *
from rest_framework.response import Response
from main.email import *
from api_portal.models import APIRequest, APIUsers
from api_portal.serializers import APIRequestSerializer, APIUsersSerializer


# Create your views here.



User = get_user_model()



class AdminDatatsetView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = DatasetSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'status', 'slug']
    queryset = Datasets.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):
            
        queryset = self.filter_queryset(self.get_queryset())
        state = request.GET.get('status', None)

        if state == "published":
            queryset = queryset.filter(status="published")

        if state == "unpublished":
            queryset = queryset.filter(status="unpublished")

        if state == "rejected":
            queryset = queryset.filter(status="rejected")

        if state == "pending":
            queryset = queryset.filter(status="pending")

        if state == "further_review":
            queryset = queryset.filter(status="further_review")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DatasetSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = DatasetSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    

class AdminDatasetDetails(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    

    def get(self, request, pk):
        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DatasetSerializer(dataset, context={'request': request})

        return Response(serializer.data)





class AdminDatasetFiles(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = DatasetFileSerializer
    pagination_class = LimitOffsetPagination
    queryset = DatasetFiles.objects.filter(is_deleted=False).order_by('-created_at')


    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        pk = self.kwargs['pk']

        try:
            dataset = Datasets.objects.get(pk=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset pk not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return DatasetFiles.objects.filter(is_deleted=False, dataset=dataset).order_by('-created_at')





class AdminOrganisationView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrganisationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'status', 'slug']
    queryset = Organisations.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination


    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        state = request.GET.get('status', None)
        verified = request.GET.get('verified', None)
        active = request.GET.get('active', None)

        if state == "approved":
            queryset = queryset.filter(status="approved")

        if state == "rejected":
            queryset = queryset.filter(status="rejected")

        if state == "pending":
            queryset = queryset.filter(status="pending")

        if active == "False":
            queryset = queryset.filter(is_active=False)

        if active == "True":
            queryset = queryset.filter(is_active=True)

        if verified == "true":
            queryset = queryset.filter(is_verified=True)

        if verified == "false":
            queryset = queryset.filter(is_verified=False)

        if state == "undeleted":
            queryset = queryset.filter(is_deleted=False)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = OrganisationSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = OrganisationSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)



    
    




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def dataset_actions(request, pk, action):

    if request.method == 'POST':
        if pk is None:
            return Response({"error": "dataset id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if action is None:
            return Response({"error": "action is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            dataset = Datasets.objects.get(id=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "dataset does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "rejected":

            dataset.status = "rejected"
            remark = request.data.get('remark', None)
            if remark is None:
                return Response({"error": "remark is required"}, status=status.HTTP_400_BAD_REQUEST) 
               
            dataset.save()
            message = f"""
Your dataset {str(dataset.title).capitalize()} has been rejected. 

Admin Remark: {str(remark).title()}
Please contact the administrator for more information.

"""
            dataset_actions_mail(user=dataset.user, action="rejected", message=message)

            return Response({"message": "dataset rejected successfully"}, status=status.HTTP_200_OK)
        
        elif action == "published":

            dataset.status = "published"
            dataset.save()

            message = f"""
Your dataset {str(dataset.title).capitalize()} has been published successfully.

"""
            dataset_actions_mail(user=dataset.user, action="published", message=message)

            if dataset.organisation:
                dataset.organisation.dataset_count += 1
                dataset.organisation.save()

            return Response({"message": "dataset approved successfully"}, status=status.HTTP_200_OK)
        
        elif action == "unpublished":

            dataset.status = "unpublished"
            dataset.save()
            message = f"""
Your dataset {str(dataset.title).capitalize()} has been unpublished.
Please contact the administrator for more information.

"""
            dataset_actions_mail(user=dataset.user, action="unpublished", message=message)

            return Response({"message": "dataset unpublished successfully"}, status=status.HTTP_200_OK)

        
        elif action == "further_review":

            dataset.status = "further_review"
            dataset.save()
            message = f"""
Your dataset {str(dataset.title).capitalize()} has been kept for further review.
Please contact the administrator for more information.

"""
            dataset_actions_mail(user=dataset.user, action="further_review", message=message)

            return Response({"message": "dataset kept for further review successfully"}, status=status.HTTP_200_OK)
        
        elif action == "delete":
                        
            dataset.is_deleted = True
            dataset.save()
            message = f"""
Your dataset {str(dataset.title).capitalize()} has been deleted. As it goes against our policies.
Please contact the administrator for more information.

"""
            dataset_actions_mail(user=dataset.user, action="deleted", message=message)

            return Response({"message": "dataset deleted successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def organisation_actions(request, pk, action):

    if request.method == 'POST':
      
        try:
            organisation = Organisations.objects.get(id=pk)
        except Datasets.DoesNotExist:
            return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "rejected":

            organisation.status = "rejected"
            organisation.save()

            users = organisation.users.all()
            message = """
Your request to create an organisation has been rejected. Please contact the administrator for more information.

"""
            for user in users:
                organisation_actions_mail(user=user, action="rejected", message=message)
            
            return Response({"message": "organisation rejected successfully"}, status=status.HTTP_200_OK)
        
        elif action == "approved":

            organisation.status = "approved"
            organisation.is_active = True
            organisation.save()

            users = organisation.users.all()
            message = f"""
Your request to create an organisation {str(organisation.name).capitalize()} has been approved. Please contact the administrator for more information.

"""
            for user in users:
                organisation_actions_mail(user=user, action="approved", message=message)
            
            return Response({"message": "organisation approved successfully"}, status=status.HTTP_200_OK)


        elif action == "block":

            organisation.is_active = False
            organisation.save()

            users = organisation.users.all()
            message = f"""
The organisation {str(organisation.name).capitalize()} has been placed on a temporary ban. Please contact the administrator for more information.
"""
            for user in users:
                organisation_actions_mail(user=user, action="blocked", message=message)
        
            return Response({"message": "organisation blocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "unblock":
                
            organisation.is_active = True
            organisation.save()

            users = organisation.users.all()
            message = f"""

The tempoary ban place on the organisation {str(organisation.name).capitalize()} has been lifted. Please contact the administrator for more information.

"""
            for user in users:
                organisation_actions_mail(user=user, action="unblocked", message=message)

            return Response({"message": "organisation unblocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "delete":
                    
            organisation.is_deleted = True
            organisation.save()

            return Response({"message": "organisation deleted successfully"}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def organisation_indicators(request):

    if request.method == 'GET':
      
        data = {
          
        "count": Organisations.objects.filter(is_deleted=False).count(),
        "approved": Organisations.objects.filter(is_deleted=False, status="approved").count(),
        "rejected": Organisations.objects.filter(is_deleted=False, status="rejected").count(),
        "pending": Organisations.objects.filter(is_deleted=False, status="pending").count()

    }
        
        return Response(data, status=status.HTTP_200_OK)




class NewsView(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewsSerializer

    @swagger_auto_schema(request_body=NewsSerializer)
    @action(detail=True, methods=['POST'])
    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            data = NewsSerializer(serializer.instance).data

            return Response(data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminOrganisationDetailView(generics.RetrieveUpdateAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrganisationSerializer
    queryset = Organisations.objects.filter(is_deleted=False).order_by('-created_at')
    lookup_field = 'pk'

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class AdminListNewsView(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    pagination_class  = LimitOffsetPagination
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title']
    queryset = News.objects.filter(is_deleted=False).order_by('-created_at')

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        state = request.query_params.get('status', None)

        if state == "published":
            queryset = queryset.filter(status='published')

        if state == "unpublished":
            queryset = queryset.filter(status='unpublished')

        if state == "draft":
            queryset = queryset.filter(status='draft')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = NewsSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = NewsSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)


   
   

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_deleted=False).order_by('-created_at')
    lookup_field = 'pk'

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def news_views(request, pk):

    if request.method == 'POST':
        
        try:
            news = News.objects.get(id=pk)
        except News.DoesNotExist:
            return Response({"error": "news does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        news.views += 1
        news.save()

        return Response({"message": "news views updated successfully"}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def news_actions(request, pk, action):

    if request.method == 'POST':
      
        try:
            news = News.objects.get(id=pk)
        except News.DoesNotExist:
            return Response({"error": "news does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "publish":

            news.status = "published"
            news.published_at = timezone.now()
            news.save()
            
            return Response({"message": "news objectt updated successfully"}, status=status.HTTP_200_OK)
        
        if action == "unpublish":

            news.satus = "unpublished"
            news.save()

            return Response({"message": "news updated successfully"}, status=status.HTTP_200_OK)
        
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
    


    
class AdminOrganisation_Requests(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrganisationRequestSerializer
    queryset = OrganisationRequests.objects.filter(is_deleted=False, status='pending').order_by('-created_at')
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def list(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)

        if pk:

            try:
                organisation = Organisations.objects.get(id=pk)
            except Organisations.DoesNotExist:
                return Response({"error": "organisation does not exist"}, status=status.HTTP_404_NOT_FOUND)
    
            queryset = self.filter_queryset(self.get_queryset()).filter(organisation=organisation)

            serializer = OrganisationRequestSerializer(queryset, many=True)

            return Response(serializer.data)
        
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrganisationRequestSerializer(queryset, many=True)

        return Response(serializer.data)




@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def organisation_request_actions(request, pk, action):

    if request.method == 'POST':
      
        try:
            organisation_request = OrganisationRequests.objects.get(id=pk)
        except OrganisationRequests.DoesNotExist:
            return Response({"error": "organisation request does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if action == "reject":

            organisation_request.status = "rejected"
            organisation_request.save()

            organisation_reject_users(organisation=organisation_request.organisation, user=organisation_request.user)
            
            return Response({"message": "organisation request rejected successfully"}, status=status.HTTP_200_OK)
        
        elif action == "approve":

            organisation_request.status = "approved"
            organisation_request.save()

            organisation_request.organisation.users.add(organisation_request.user)

            organisation_request.organisation.save()

            organisation_add_users(organisation=organisation_request.organisation, user=organisation_request.user)


            return Response({"message": "organisation request approved successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        


class AdminCategories(generics.ListAPIView):
    
    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'slug']
    queryset = Categories.objects.filter(is_deleted=False).order_by('-created_at')
    pagination_class = LimitOffsetPagination

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context







class AdminUsers(generics.ListAPIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]
    serializer_class = CustomUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']
    pagination_class = LimitOffsetPagination
    queryset = User.objects.filter(is_deleted=False).order_by('-date_joined')

    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        state = request.GET.get('status', None)

        if state == "active":
            queryset = queryset.filter(is_active=True)

        if state == "inactive":
            queryset = queryset.filter(is_active=False)

    
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomUserSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = CustomUserSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def user_actions(request, pk, action):

    if request.method == "POST":

        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

        if action == "block":

            user.is_active = False
            user.save()

            return Response({"message": "user blocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "unblock":

            user.is_active = True
            user.save()

            return Response({"message": "user unblocked successfully"}, status=status.HTTP_200_OK)
        
        elif action == "delete":

            user.is_deleted = True
            user.save()

            return Response({"message": "user deleted successfully"}, status=status.HTTP_200_OK)
        
        else:
            return Response({"error": "invalid action"}, status=status.HTTP_400_BAD_REQUEST)
        


class AdminDashboardCounts(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        data = {
            "users": User.objects.filter(is_deleted=False).count(),
            "organisations": Organisations.objects.filter(is_deleted=False).count(),
            "datasets": Datasets.objects.filter(is_deleted=False).count(),
            "news": News.objects.filter(is_deleted=False).count()
        }

        return Response(data, status=status.HTTP_200_OK)
    

class AverageCategoryView(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        daily = []
        weekly = []
        monthly = []

        category = Categories.objects.filter(is_deleted=False).order_by('-views')[:6]
        category_analysis = CategoryAnalysis.objects.all()
 
        for cat in category:
            daily.append({
                "name": cat.name,
                "views": category_analysis.filter(category=cat, created_at__day=timezone.now().day, attribute='view').count()
            })

        for cat in category:
            weekly.append({
                "name": cat.name,
                "views": category_analysis.filter(category=cat, created_at__week=timezone.now().isocalendar()[1], attribute='view').count()
            })

        for cat in category:
            monthly.append({
                "name": cat.name,
                "views": category_analysis.filter(category=cat, created_at__month=timezone.now().month, attribute='view').count()
            })

        data = {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly
        }
        
        return Response(data, status=status.HTTP_200_OK)
    


class AverageDownloadView(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]


    def get(self, request):

        daily = []
        weekly = []
        monthly = []

        category = Categories.objects.filter(is_deleted=False).order_by('-downloads')[:6]
        category_analysis = CategoryAnalysis.objects.all()
        
 
        for cat in category:
            daily.append({
                "name": cat.name,
                "downloads": category_analysis.filter(category=cat, created_at__day=timezone.now().day, attribute='download').count()
            })

        for cat in category:
            weekly.append({
                "name": cat.name,
                "downloads": category_analysis.filter(category=cat, created_at__week=timezone.now().isocalendar()[1], attribute='download').count()
            })

        for cat in category:
            monthly.append({
                "name": cat.name,
                "downloads": category_analysis.filter(category=cat, created_at__month=timezone.now().month, attribute='download').count()
            })
        

        data = {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly
        }
        
        
        return Response(data, status=status.HTTP_200_OK)
    

class AdminMostPublishedOrganisation(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]


    def get(self, request):

        organisation = Organisations.objects.filter(is_deleted=False, status='approved').order_by('-dataset_count')[:5]

        data = OrganisationSerializer(organisation, many=True, context={'request': request}).data

        return Response(data, status=status.HTTP_200_OK)




class AdminAPIUsers(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]
    queryset = APIUsers.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = APIUsersSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__email', 'user__first_name', 'user__last_name' ]
    pagination_class = LimitOffsetPagination


    def get_serializer_context(self):
       
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


    def list(self, request, *args, **kwargs):
            
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = DatasetSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = DatasetSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data)
    







