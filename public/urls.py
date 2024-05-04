from django.urls import path, include
from .views import *








urlpatterns = [
    path('public/category/', PublicCategoryView.as_view(), name="public_category"),
    path('public/category/<str:slug>/', PublicCategoryDetailView.as_view(), name="public_category"),
    path('public/organisations/', PublicOrganisationView.as_view(), name="public_organisations"),
    path('public/organisations/<str:slug>/', PublicOrganisationDetailView.as_view(), name="public_organisations"),
    path('public/datasets/', PublicDatasetView.as_view(), name="public_datasets"),
    path('public/datasets/<str:slug>/', PublicDatasetDetailView.as_view(), name="public_datasets"),
    path('public/counts/', PublicCounts.as_view(), name="public_counts"),
    path('public/popular/dataset/', PopularDataset.as_view(), name="public_popular"),
    path('public/news/', PublicNews.as_view(), name="public_news"),
    path('public/news/<str:slug>/', PublicNewsDetailView.as_view(), name="public_news_detail"),
    path('public/tags/', PublicTagsView.as_view(), name="public_tags"),
    path('public/user/pk/<uuid:pk>/detail/', PublicUserDetailView.as_view(), name="public_user_detail"),
    path('public/user/pk/<uuid:pk>/datasets/', PublicUserDataset.as_view(), name="public_user_datasets"),
    path('public/popular/organisation/pk/<uuid:pk>/datasets/', PublicPopularOrganisationDataset.as_view(), name="public_popular_organisation_dataset"),
    path('public/support/system/', PublicSupportSystem.as_view(), name="public_support_system"),
    path('public/location/analysis/<uuid:pk>/', PublicLocationRequest.as_view(), name="public_location_analysis"),
    path('public/IP/', GetClientIP.as_view(), name="public_client_ip"),
]