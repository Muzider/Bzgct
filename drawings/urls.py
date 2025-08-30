from django.urls import path
from . import views

app_name = 'drawings'

urlpatterns = [
    # 首页
    path('', views.index, name='index'),
    
    # 权限管理模块
    path('permission/', views.permission_index, name='permission_index'),
    
    # 角色管理
    path('role/', views.role_list, name='role_list'),
    path('role/add/', views.role_add, name='role_add'),
    path('role/<int:role_id>/edit/', views.role_edit, name='role_edit'),
    path('role/<int:role_id>/delete/', views.role_delete, name='role_delete'),
    path('role/<int:role_id>/permissions/', views.role_permissions, name='role_permissions'),
    
    # 人员管理
    path('person/', views.person_list, name='person_list'),
    path('person/add/', views.person_add, name='person_add'),
    path('person/<int:person_id>/edit/', views.person_edit, name='person_edit'),
    path('person/<int:person_id>/delete/', views.person_delete, name='person_delete'),
    path('person/<int:person_id>/roles/', views.person_roles, name='person_roles'),
    
    # 权限管理
    path('permission/list/', views.permission_list, name='permission_list'),
    path('permission/add/', views.permission_add, name='permission_add'),
    path('permission/<int:permission_id>/edit/', views.permission_edit, name='permission_edit'),
    path('permission/<int:permission_id>/delete/', views.permission_delete, name='permission_delete'),
    
    # 船型管理
    path('ship-type/', views.ship_type_list, name='ship_type_list'),
    path('ship-type/add/', views.ship_type_add, name='ship_type_add'),
    path('ship-type/<int:ship_type_id>/edit/', views.ship_type_edit, name='ship_type_edit'),
    path('ship-type/<int:ship_type_id>/delete/', views.ship_type_delete, name='ship_type_delete'),
    
    # 典型分段管理
    path('typical-section/', views.typical_section_list, name='typical_section_list'),
    path('typical-section/add/', views.typical_section_add, name='typical_section_add'),
    path('typical-section/<int:section_id>/edit/', views.typical_section_edit, name='typical_section_edit'),
    path('typical-section/<int:section_id>/delete/', views.typical_section_delete, name='typical_section_delete'),
    
    # 作业工种管理
    path('work-type/', views.work_type_list, name='work_type_list'),
    path('work-type/add/', views.work_type_add, name='work_type_add'),
    path('work-type/<int:work_type_id>/edit/', views.work_type_edit, name='work_type_edit'),
    path('work-type/<int:work_type_id>/delete/', views.work_type_delete, name='work_type_delete'),
    
    # 作业工序管理
    path('work-process/', views.work_process_list, name='work_process_list'),
    path('work-process/add/', views.work_process_add, name='work_process_add'),
    path('work-process/<int:process_id>/edit/', views.work_process_edit, name='work_process_edit'),
    path('work-process/<int:process_id>/delete/', views.work_process_delete, name='work_process_delete'),
]
