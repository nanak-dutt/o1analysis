from django.contrib import admin
from django.urls import path

from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views
# from myapp import views as myapp_views

schema_view = get_schema_view(
	openapi.Info(
		title="Apti APIs",
		default_version='v1',
		description="Welcome to the world of coding",
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

	path('quesbank/', views.question_bank),

	# authentication - register & login
	path('auth/register/', views.register),
    path('auth/login/', views.login),

	path('get_test_analysis',views.get_test_analysis),

	path('analytics/', views.analytics),
	path('ranklist/college', views.ranklist),
	path('ranklist/global', views.globalranklist),

	# added to test gsheet data
    # path('gs' , views.user_responses)
	#path('test/', views.testing_function),
	path('analytics/', views.analytics),
    path('get_test_analysis',views.get_test_analysis),

    # added to test gsheet data
    path('gs' , views.fetch_user_responses),
	path('college_list' , views.college_list),

	path('weak_topic' , views.weakest_topics),
	path('get_user_ranklist' , views.get_user_ranklist_data),
	
]
