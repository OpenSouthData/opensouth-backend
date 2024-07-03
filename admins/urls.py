from django.urls import path, include
from .views import *
from . import views








urlpatterns = [


    path('admin/datasets/', AdminDatatsetView.as_view(), name="admin_datatsets"),
    path('admin/dataset/<uuid:pk>/', views.AdminDatasetDetails.as_view(), name="admin_dataset_details"),
    path('admin/dataset/pk/<uuid:pk>/files/', views.AdminDatasetFiles.as_view(), name="admin_dataset_views"),
    path('admin/datasets/pk/<uuid:pk>/actions/<str:action>/', dataset_actions, name="admin_datatsets_actions"),
    path('admin/organisations/pk/<uuid:pk>/actions/<str:action>/', organisation_actions, name="admin_organisations_actions"),
    path('admin/organisations/', AdminOrganisationView.as_view(), name="admin_organisations"),
    path('admin/organisations/<uuid:pk>/', AdminOrganisationDetailView.as_view(), name="admin_organisations_detail"),
    path('admin/organisations/indicators/', organisation_indicators, name="admin_organisations_indicators"),
    path('admin/news/', NewsView.as_view(), name="admin_news"),
    path('admin/news/list/', AdminListNewsView.as_view(), name="admin_news_list"),
    path('admin/news/<uuid:pk>/', NewsDetailView.as_view(), name="admin_news"),
    path('admin/news/<uuid:pk>/actions/<str:action>/', news_actions, name="admin_news_actions"),
    path('news/views/<uuid:pk>/', news_views, name="news_views"),
    path('admin/categories/', AdminCategories.as_view(), name="admin_categories"),
    path('admin/users/', AdminUsers.as_view(), name="admin_users"),
    path('admin/dashboard/counts/', AdminDashboardCounts.as_view(), name="admin_dashboard_counts"),
    path('admin/users/pk/<uuid:pk>/actions/<str:action>/', user_actions, name="admin_users_actions"),
    path('admin/organisation_requests/', AdminOrganisation_Requests.as_view(), name="admin_organisation_requests"),
    path('admin/organisation_requests/pk/<uuid:pk>/actions/<str:action>/', organisation_request_actions, name="admin_organisation_requests_actions"),
    path('admin/average-category/chart/', AverageCategoryView.as_view(), name="admin_average_category_chart"),
    path('admin/average-download/chart/', AverageDownloadView.as_view(), name="admin_average_download_chart"),
    path('admin/most-published/organisation/', AdminMostPublishedOrganisation.as_view(), name="admin_most_published_organisation"),
    path('admin/api/users/', AdminAPIUsers.as_view(), name="admin_api_users"),


]
