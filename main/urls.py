from django.urls import path, include
from .views import *
from . import views








urlpatterns = [
    
    path('organisations/', OrganisationView.as_view(), name="organisations"),
    path('organisations/<str:slug>/', OrganisationDetailView.as_view(), name="organisations"),
    path('organisations/<uuid:org_pk>/users/', add_user_to_organisation, name="add_user_to_organisation"),
    path('organisations/users/<uuid:pk>/', OrganisationUsers.as_view(), name="organisation_users"),
    path('organisations/<uuid:org_pk>/users/<str:user_pk>/', delete_user_from_organisation, name="delete_user_from_organisation"),
    path('datasets/<uuid:cat_pk>/', DatasetView.as_view(), name="datasets"),
    path('datasets/files/<uuid:pk>/', CreateDatasetFiles.as_view(), name="datasets_files"),
    path('categories/', CategoryView.as_view(), name="categories"),
    path('categories/<uuid:pk>/', CategoryDetailView.as_view(), name="categories"),
    path('datasets/views/<uuid:pk>/', DatasetViewsView.as_view(), name="datasets_views"),
    path('datasets/downloads/<uuid:pk>/', DatasetDownloadCount.as_view(), name="datasets_downloads"),
    path('datasets/tags/<uuid:pk>/', TagsView.as_view(), name="tags"),
    path('user/organisations/<uuid:pk>/datasets/', UserOrganisationDatasets.as_view(), name="user_organisation_datasets"),
    path('user/organisations/pk/<uuid:org_pk>/dataset/pk/<uuid:pk>/details/', UserOrganisationDatasetDetail.as_view(), name="user_organisation_details"),
    path('user/datasets/', UserDataset.as_view(), name="user_datasets"),
    path('user/token/manager/', UserToken.as_view(), name="user_token_manager"),
    path('user/api/request/', UserAPIRequest.as_view(), name="user_api_request"),
    path('user/dataset/pk/<uuid:pk>/files/', UserDatasetFiles.as_view(), name="user_dataset_files"),
    path('user/datasets/<uuid:pk>/', UserDatasetDetailView.as_view(), name="user_datasets"),
    path('user/organisations/', UserOrganisation.as_view(), name="user_organisations"),
    path('organisations/resend-pin/<uuid:pk>/', resend_pin, name="resend_pin"),
    path('user/dashboard/counts/', UserDashboardCounts.as_view(), name="user_dashboard_counts"),
    path('user/request-to-join-organisation/<uuid:pk>/', request_to_join_organisation, name="request_to_join_organisation"),
    path('admin/most-accessed-data/', views.AdminMostAccesseData.as_view(), name="admin_most_accessed_datasets"),
    path('user/most-accessed-data/', views.UserMostAccessedData.as_view(), name="user_most_accessed_datasets"),
    path('organisation/most-accessed-data/<uuid:pk>/', views.OrganisationMostAccessedData.as_view(), name="organisation_most_accessed_datasets"),
    path('user/location/analysis/', views.UserLocationAnalysisView.as_view(), name="user_location_analysis"),
    path('organisation/location/analysis/<uuid:pk>/', views.OrganisationLocationAnalysis.as_view(), name="organisation_location_analysis"),
    path('admin/location/analysis/', views.AdminLocationAnalysis.as_view(), name="admin_location_analysis"),

]
