from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.DefaultRouter()
router.register(r'tables', views.TableViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="OpenAPI Specification",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('table/', views.tables_home, name='table-list'),
    path('table/create/', views.tables_create_table, name='table-create'),
    path('table/<int:id>/', views.tables_get_table, name='table-detail'),
    path('table/<int:id>/delete', views.tables_delete_table, name='table-delete'),
    path('table/<int:id>/add_col', views.tables_add_col, name='table-add-col'),
    path('table/<int:id>/edit_col/<str:col_name>', views.tables_edit_col, name='table-edit-col'),
    path('table/<int:id>/del_col/<str:col_name>', views.tables_delete_col, name='table-del-col'),
    path('table/<int:id>/add_row', views.tables_add_row, name='table-add-row'),
    path('table/<int:id>/del_row/<int:row_num>', views.tables_del_row, name='table-del-row'),

    path('save_database', views.export_to_csv, name='database-save'),
    path('set_database', views.database_set, name='database-set'),
    path('clear_database', views.database_clear, name='database-clear'),

    path('rest', include(router.urls)),
    path('rest/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


