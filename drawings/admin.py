from django.contrib import admin
from .models import (
    ShipType, Role, Person, Permission, RolePermission, PersonRole,
    TypicalSection, WorkType, WorkProcess, Project, Section, Pallet,
    StandardProcessFlow, ProcessFlowStep
)

# Register your models here.

@admin.register(ShipType)
class ShipTypeAdmin(admin.ModelAdmin):
    list_display = ['ship_type', 'ship_subtype', 'created_at', 'updated_at']
    search_fields = ['ship_type', 'ship_subtype']
    list_filter = ['created_at', 'updated_at']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'created_at']


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['name', 'employee_id', 'department', 'position', 'gender', 'is_active']
    search_fields = ['name', 'employee_id', 'department']
    list_filter = ['department', 'gender', 'is_active', 'created_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['module', 'action', 'description', 'is_active']
    search_fields = ['module', 'action', 'description']
    list_filter = ['module', 'action', 'is_active']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'permission', 'created_at']
    list_filter = ['role', 'permission', 'created_at']


@admin.register(PersonRole)
class PersonRoleAdmin(admin.ModelAdmin):
    list_display = ['person', 'role', 'created_at']
    list_filter = ['person', 'role', 'created_at']


@admin.register(TypicalSection)
class TypicalSectionAdmin(admin.ModelAdmin):
    list_display = ['ship_type', 'section_name', 'section_code', 'is_active', 'created_at']
    search_fields = ['section_name', 'section_code']
    list_filter = ['ship_type', 'is_active', 'created_at']


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ['work_type_name', 'work_type_code', 'standard_hours', 'is_active', 'created_at']
    search_fields = ['work_type_name', 'work_type_code']
    list_filter = ['is_active', 'created_at']


@admin.register(WorkProcess)
class WorkProcessAdmin(admin.ModelAdmin):
    list_display = ['process_name', 'process_code', 'work_type', 'coefficient', 'work_hours', 'is_active']
    search_fields = ['process_name', 'process_code']
    list_filter = ['work_type', 'is_active', 'created_at']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['project_name', 'ship_type', 'classification_society', 'delivery_date', 'is_active']
    search_fields = ['project_name', 'classification_society']
    list_filter = ['ship_type', 'is_active', 'delivery_date', 'created_at']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['section_number', 'project', 'section_type', 'planned_start_date', 'is_active']
    search_fields = ['section_number', 'project__project_name']
    list_filter = ['project', 'section_type', 'is_active', 'created_at']


@admin.register(Pallet)
class PalletAdmin(admin.ModelAdmin):
    list_display = ['pallet_code', 'pallet_name', 'project', 'section', 'required_date', 'is_received']
    search_fields = ['pallet_code', 'pallet_name', 'project__project_name']
    list_filter = ['project', 'section', 'is_received', 'is_active', 'created_at']


class ProcessFlowStepInline(admin.TabularInline):
    model = ProcessFlowStep
    extra = 1
    fields = ['step_name', 'work_process', 'step_order', 'parallel_group', 'estimated_hours', 'description']


@admin.register(StandardProcessFlow)
class StandardProcessFlowAdmin(admin.ModelAdmin):
    list_display = ['name', 'ship_type', 'typical_section', 'estimated_total_hours', 'is_active', 'created_at']
    search_fields = ['name', 'ship_type__ship_type', 'typical_section__section_name']
    list_filter = ['ship_type', 'typical_section', 'is_active', 'created_at']
    inlines = [ProcessFlowStepInline]


@admin.register(ProcessFlowStep)
class ProcessFlowStepAdmin(admin.ModelAdmin):
    list_display = ['step_name', 'process_flow', 'work_process', 'step_order', 'parallel_group', 'estimated_hours']
    search_fields = ['step_name', 'process_flow__name', 'work_process__process_name']
    list_filter = ['process_flow', 'work_process', 'parallel_group', 'is_active']
    ordering = ['process_flow', 'step_order', 'parallel_group']
