from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('zones/', views.zone_list, name='zone_list'),
    path('zones/create/', views.zone_create, name='zone_create'),
    path('zones/<int:pk>/edit/', views.zone_edit, name='zone_edit'),
    path('zones/<int:pk>/delete/', views.zone_delete, name='zone_delete'),
    path('inventoryitems/', views.inventoryitem_list, name='inventoryitem_list'),
    path('inventoryitems/create/', views.inventoryitem_create, name='inventoryitem_create'),
    path('inventoryitems/<int:pk>/edit/', views.inventoryitem_edit, name='inventoryitem_edit'),
    path('inventoryitems/<int:pk>/delete/', views.inventoryitem_delete, name='inventoryitem_delete'),
    path('picklists/', views.picklist_list, name='picklist_list'),
    path('picklists/create/', views.picklist_create, name='picklist_create'),
    path('picklists/<int:pk>/edit/', views.picklist_edit, name='picklist_edit'),
    path('picklists/<int:pk>/delete/', views.picklist_delete, name='picklist_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
