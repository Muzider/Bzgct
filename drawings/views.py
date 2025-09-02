from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db import models
from django.core.paginator import Paginator
from .models import Role, Person, Permission, RolePermission, PersonRole, ShipType, TypicalSection, WorkType, WorkProcess, Project, Section, Pallet

# Create your views here.

def index(request):
    """首页"""
    return render(request, 'drawings/index.html')

def permission_index(request):
    """权限管理首页"""
    return render(request, 'drawings/permission/index.html')

# 角色管理视图
def role_list(request):
    """角色列表"""
    roles = Role.objects.all()
    
    # 分页
    paginator = Paginator(roles, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drawings/role/list.html', {'page_obj': page_obj})

def role_add(request):
    """添加角色"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 创建角色
            role = Role.objects.create(
                name=name,
                description=description,
                is_active=is_active
            )
            
            # 重定向到角色列表页面
            return redirect('drawings:role_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/role/add.html', {
                'error_message': f'保存失败：{str(e)}'
            })
    
    return render(request, 'drawings/role/add.html')

def role_edit(request, role_id):
    """编辑角色"""
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 更新角色
            role.name = name
            role.description = description
            role.is_active = is_active
            role.save()
            
            # 重定向到角色列表页面
            return redirect('drawings:role_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/role/edit.html', {
                'role': role,
                'error_message': f'保存失败：{str(e)}'
            })
    
    return render(request, 'drawings/role/edit.html', {'role': role})

def role_delete(request, role_id):
    """删除角色"""
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        role.delete()
        return redirect('drawings:role_list')
    return render(request, 'drawings/role/delete.html', {'role': role})

def role_permissions(request, role_id):
    """角色权限管理"""
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        # TODO: 处理权限分配
        pass
    return render(request, 'drawings/role/permissions.html', {'role': role})

# 人员管理视图
def person_list(request):
    """人员列表"""
    persons = Person.objects.all()
    
    # 分页
    paginator = Paginator(persons, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drawings/person/list.html', {'page_obj': page_obj})

def person_add(request):
    """添加人员"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            employee_id = request.POST.get('employee_id')
            department = request.POST.get('department')
            position = request.POST.get('position')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 创建人员
            person = Person.objects.create(
                name=name,
                employee_id=employee_id,
                department=department,
                position=position,
                gender=gender,
                phone=phone,
                email=email,
                is_active=is_active
            )
            
            # 处理角色分配
            role_ids = request.POST.getlist('roles')
            for role_id in role_ids:
                try:
                    role = Role.objects.get(id=role_id)
                    PersonRole.objects.create(person=person, role=role)
                except Role.DoesNotExist:
                    pass  # 忽略不存在的角色
            
            # 重定向到人员列表页面
            return redirect('drawings:person_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            roles = Role.objects.filter(is_active=True)
            return render(request, 'drawings/person/add.html', {
                'error_message': f'保存失败：{str(e)}',
                'roles': roles
            })
    
    # GET请求，显示表单
    roles = Role.objects.filter(is_active=True)
    return render(request, 'drawings/person/add.html', {'roles': roles})

def person_edit(request, person_id):
    """编辑人员"""
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.POST.get('name')
            employee_id = request.POST.get('employee_id')
            department = request.POST.get('department')
            position = request.POST.get('position')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone', '')
            email = request.POST.get('email', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 更新人员
            person.name = name
            person.employee_id = employee_id
            person.department = department
            person.position = position
            person.gender = gender
            person.phone = phone
            person.email = email
            person.is_active = is_active
            person.save()
            
            # 处理角色分配
            role_ids = request.POST.getlist('roles')
            # 先删除所有现有角色
            PersonRole.objects.filter(person=person).delete()
            # 重新分配角色
            for role_id in role_ids:
                try:
                    role = Role.objects.get(id=role_id)
                    PersonRole.objects.create(person=person, role=role)
                except Role.DoesNotExist:
                    pass  # 忽略不存在的角色
            
            # 重定向到人员列表页面
            return redirect('drawings:person_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            roles = Role.objects.filter(is_active=True)
            person_roles = PersonRole.objects.filter(person=person).values_list('role_id', flat=True)
            return render(request, 'drawings/person/edit.html', {
                'person': person,
                'roles': roles,
                'person_roles': person_roles,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    roles = Role.objects.filter(is_active=True)
    person_roles = PersonRole.objects.filter(person=person).values_list('role_id', flat=True)
    return render(request, 'drawings/person/edit.html', {
        'person': person,
        'roles': roles,
        'person_roles': person_roles
    })

def person_delete(request, person_id):
    """删除人员"""
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        person.delete()
        return redirect('drawings:person_list')
    return render(request, 'drawings/person/delete.html', {'person': person})

def person_roles(request, person_id):
    """人员角色管理"""
    person = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        # TODO: 处理角色分配
        pass
    return render(request, 'drawings/person/roles.html', {'person': person})

# 权限管理视图
def permission_list(request):
    """权限列表"""
    permissions = Permission.objects.all()
    
    # 分页
    paginator = Paginator(permissions, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drawings/permission/list.html', {'page_obj': page_obj})

def permission_add(request):
    """添加权限"""
    if request.method == 'POST':
        # TODO: 处理表单提交
        pass
    return render(request, 'drawings/permission/add.html')

def permission_edit(request, permission_id):
    """编辑权限"""
    permission = get_object_or_404(Permission, id=permission_id)
    if request.method == 'POST':
        # TODO: 处理表单提交
        pass
    return render(request, 'drawings/permission/edit.html', {'permission': permission})

def permission_delete(request, permission_id):
    """删除权限"""
    permission = get_object_or_404(Permission, id=permission_id)
    if request.method == 'POST':
        permission.delete()
        return redirect('drawings:permission_list')
    return render(request, 'drawings/permission/delete.html', {'permission': permission})

# 船型管理视图
def ship_type_list(request):
    """船型列表"""
    ship_types = ShipType.objects.all()
    
    # 分页
    paginator = Paginator(ship_types, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'drawings/ship_type/list.html', {'page_obj': page_obj})

def ship_type_add(request):
    """添加船型"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            ship_type = request.POST.get('ship_type')
            ship_subtype = request.POST.get('ship_subtype', '')
            
            # 创建船型
            ship_type_obj = ShipType.objects.create(
                ship_type=ship_type,
                ship_subtype=ship_subtype
            )
            
            # 重定向到船型列表页面
            return redirect('drawings:ship_type_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/ship_type/add.html', {
                'error_message': f'保存失败：{str(e)}'
            })
    
    return render(request, 'drawings/ship_type/add.html')

def ship_type_edit(request, ship_type_id):
    """编辑船型"""
    ship_type = get_object_or_404(ShipType, id=ship_type_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            ship_type_name = request.POST.get('ship_type')
            ship_subtype = request.POST.get('ship_subtype', '')
            
            # 更新船型
            ship_type.ship_type = ship_type_name
            ship_type.ship_subtype = ship_subtype
            ship_type.save()
            
            # 重定向到船型列表页面
            return redirect('drawings:ship_type_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/ship_type/edit.html', {
                'ship_type': ship_type,
                'error_message': f'保存失败：{str(e)}'
            })
    
    return render(request, 'drawings/ship_type/edit.html', {'ship_type': ship_type})

def ship_type_delete(request, ship_type_id):
    """删除船型"""
    ship_type = get_object_or_404(ShipType, id=ship_type_id)
    if request.method == 'POST':
        ship_type.delete()
        return redirect('drawings:ship_type_list')
    return render(request, 'drawings/ship_type/delete.html', {'ship_type': ship_type})


# 典型分段管理视图
def typical_section_list(request):
    """典型分段列表"""
    # 获取查询参数
    ship_type_filter = request.GET.get('ship_type', '')
    search_query = request.GET.get('search', '')
    
    # 基础查询
    sections = TypicalSection.objects.select_related('ship_type').all()
    
    # 应用筛选条件
    if ship_type_filter:
        sections = sections.filter(ship_type__ship_type__icontains=ship_type_filter)
    
    if search_query:
        sections = sections.filter(
            models.Q(section_name__icontains=search_query) |
            models.Q(section_code__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(ship_type__ship_type__icontains=search_query)
        )
    
    # 获取所有船型用于筛选下拉框
    ship_types = ShipType.objects.all()
    
    # 分页
    paginator = Paginator(sections, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'ship_types': ship_types,
        'ship_type_filter': ship_type_filter,
        'search_query': search_query,
    }
    return render(request, 'drawings/typical_section/list.html', context)


def typical_section_add(request):
    """添加典型分段"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            ship_type_id = request.POST.get('ship_type')
            section_name = request.POST.get('section_name')
            section_code = request.POST.get('section_code', '')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 获取船型
            ship_type = ShipType.objects.get(id=ship_type_id)
            
            # 创建典型分段
            section = TypicalSection.objects.create(
                ship_type=ship_type,
                section_name=section_name,
                section_code=section_code,
                description=description,
                is_active=is_active
            )
            
            # 重定向到典型分段列表页面
            return redirect('drawings:typical_section_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            ship_types = ShipType.objects.all()
            return render(request, 'drawings/typical_section/add.html', {
                'error_message': f'保存失败：{str(e)}',
                'ship_types': ship_types
            })
    
    # GET请求，显示表单
    ship_types = ShipType.objects.all()
    return render(request, 'drawings/typical_section/add.html', {'ship_types': ship_types})


def typical_section_edit(request, section_id):
    """编辑典型分段"""
    section = get_object_or_404(TypicalSection, id=section_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            ship_type_id = request.POST.get('ship_type')
            section_name = request.POST.get('section_name')
            section_code = request.POST.get('section_code', '')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 获取船型
            ship_type = ShipType.objects.get(id=ship_type_id)
            
            # 更新典型分段
            section.ship_type = ship_type
            section.section_name = section_name
            section.section_code = section_code
            section.description = description
            section.is_active = is_active
            section.save()
            
            # 重定向到典型分段列表页面
            return redirect('drawings:typical_section_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            ship_types = ShipType.objects.all()
            return render(request, 'drawings/typical_section/edit.html', {
                'section': section,
                'ship_types': ship_types,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    ship_types = ShipType.objects.all()
    return render(request, 'drawings/typical_section/edit.html', {
        'section': section,
        'ship_types': ship_types
    })


def typical_section_delete(request, section_id):
    """删除典型分段"""
    section = get_object_or_404(TypicalSection, id=section_id)
    if request.method == 'POST':
        section.delete()
        return redirect('drawings:typical_section_list')
    return render(request, 'drawings/typical_section/delete.html', {'section': section})


# 作业工种管理视图
def work_type_list(request):
    """作业工种列表"""
    work_types = WorkType.objects.all()
    
    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        work_types = work_types.filter(
            models.Q(work_type_name__icontains=search_query) |
            models.Q(work_type_code__icontains=search_query) |
            models.Q(description__icontains=search_query)
        )
    
    # 分页
    paginator = Paginator(work_types, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'drawings/work_type/list.html', context)


def work_type_add(request):
    """添加作业工种"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            work_type_name = request.POST.get('work_type_name')
            work_type_code = request.POST.get('work_type_code')

            standard_hours_str = request.POST.get('standard_hours')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 转换standard_hours为Decimal类型
            try:
                from decimal import Decimal
                standard_hours = Decimal(standard_hours_str)
            except (ValueError, TypeError):
                raise ValueError("标准工时必须是有效的数字")
            
            # 创建作业工种
            work_type = WorkType.objects.create(
                work_type_name=work_type_name,
                work_type_code=work_type_code,
                standard_hours=standard_hours,
                description=description,
                is_active=is_active
            )
            
            # 重定向到作业工种列表页面
            return redirect('drawings:work_type_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/work_type/add.html', {
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    return render(request, 'drawings/work_type/add.html')


def work_type_edit(request, work_type_id):
    """编辑作业工种"""
    work_type = get_object_or_404(WorkType, id=work_type_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            work_type_name = request.POST.get('work_type_name')
            work_type_code = request.POST.get('work_type_code')
            standard_hours_str = request.POST.get('standard_hours')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 转换standard_hours为Decimal类型
            try:
                from decimal import Decimal
                standard_hours = Decimal(standard_hours_str)
            except (ValueError, TypeError):
                raise ValueError("标准工时必须是有效的数字")
            
            # 更新作业工种
            work_type.work_type_name = work_type_name
            work_type.work_type_code = work_type_code
            work_type.standard_hours = standard_hours
            work_type.description = description
            work_type.is_active = is_active
            work_type.save()
            
            # 重定向到作业工种列表页面
            return redirect('drawings:work_type_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            return render(request, 'drawings/work_type/edit.html', {
                'work_type': work_type,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    return render(request, 'drawings/work_type/edit.html', {
        'work_type': work_type
    })


def work_type_delete(request, work_type_id):
    """删除作业工种"""
    work_type = get_object_or_404(WorkType, id=work_type_id)
    if request.method == 'POST':
        work_type.delete()
        return redirect('drawings:work_type_list')
    return render(request, 'drawings/work_type/delete.html', {'work_type': work_type})


# 作业工序管理视图
def work_process_list(request):
    """作业工序列表"""
    work_processes = WorkProcess.objects.all().select_related('work_type')
    
    # 搜索功能
    search_query = request.GET.get('search', '')
    work_type_filter = request.GET.get('work_type', '')
    
    if search_query:
        work_processes = work_processes.filter(
            models.Q(process_name__icontains=search_query) |
            models.Q(process_code__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(work_type__work_type_name__icontains=search_query)
        )
    
    if work_type_filter:
        work_processes = work_processes.filter(work_type__work_type_name__icontains=work_type_filter)
    
    # 获取所有工种用于筛选
    work_types = WorkType.objects.all()
    
    # 分页
    paginator = Paginator(work_processes, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'work_types': work_types,
        'search_query': search_query,
        'work_type_filter': work_type_filter,
    }
    return render(request, 'drawings/work_process/list.html', context)


def work_process_add(request):
    """添加作业工序"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            process_name = request.POST.get('process_name')
            process_code = request.POST.get('process_code')
            work_type_id = request.POST.get('work_type')
            coefficient_str = request.POST.get('coefficient')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not work_type_id:
                raise ValueError("请选择关联工种")
            
            # 获取工种
            work_type = WorkType.objects.get(id=work_type_id)
            
            # 转换coefficient为Decimal类型
            try:
                from decimal import Decimal
                coefficient = Decimal(coefficient_str)
            except (ValueError, TypeError):
                raise ValueError("工时系数必须是有效的数字")
            
            # 创建作业工序
            work_process = WorkProcess.objects.create(
                process_name=process_name,
                process_code=process_code,
                work_type=work_type,
                coefficient=coefficient,
                description=description,
                is_active=is_active
            )
            
            # 重定向到作业工序列表页面
            return redirect('/work-process/')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            work_types = WorkType.objects.all()
            return render(request, 'drawings/work_process/add.html', {
                'error_message': f'保存失败：{str(e)}',
                'work_types': work_types
            })
    
    # GET请求，显示表单
    work_types = WorkType.objects.all()
    return render(request, 'drawings/work_process/add.html', {'work_types': work_types})


def work_process_edit(request, process_id):
    """编辑作业工序"""
    work_process = get_object_or_404(WorkProcess, id=process_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            process_name = request.POST.get('process_name')
            process_code = request.POST.get('process_code')
            work_type_id = request.POST.get('work_type')
            coefficient_str = request.POST.get('coefficient')
            description = request.POST.get('description', '')
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not work_type_id:
                raise ValueError("请选择关联工种")
            
            # 获取工种
            work_type = WorkType.objects.get(id=work_type_id)
            
            # 转换coefficient为Decimal类型
            try:
                from decimal import Decimal
                coefficient = Decimal(coefficient_str)
            except (ValueError, TypeError):
                raise ValueError("工时系数必须是有效的数字")
            
            # 更新作业工序
            work_process.process_name = process_name
            work_process.process_code = process_code
            work_process.work_type = work_type
            work_process.coefficient = coefficient
            work_process.description = description
            work_process.is_active = is_active
            work_process.save()
            
            # 重定向到作业工序列表页面
            return redirect('/work-process/')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            work_types = WorkType.objects.all()
            return render(request, 'drawings/work_process/edit.html', {
                'work_process': work_process,
                'work_types': work_types,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    work_types = WorkType.objects.all()
    return render(request, 'drawings/work_process/edit.html', {
        'work_process': work_process,
        'work_types': work_types
    })


def work_process_delete(request, process_id):
    """删除作业工序"""
    work_process = get_object_or_404(WorkProcess, id=process_id)
    if request.method == 'POST':
        work_process.delete()
        return redirect('/work-process/')
    return render(request, 'drawings/work_process/delete.html', {'work_process': work_process})


# 项目管理视图
def project_list(request):
    """项目信息列表"""
    projects = Project.objects.all().select_related('ship_type')
    
    # 搜索和筛选功能
    search_query = request.GET.get('search', '')
    ship_type_filter = request.GET.get('ship_type', '')
    delivery_year_filter = request.GET.get('delivery_year', '')
    
    if search_query:
        projects = projects.filter(
            models.Q(project_name__icontains=search_query) |
            models.Q(classification_society__icontains=search_query)
        )
    
    if ship_type_filter:
        projects = projects.filter(ship_type__ship_type__icontains=ship_type_filter)
    
    if delivery_year_filter:
        projects = projects.filter(delivery_date__year=delivery_year_filter)
    
    # 获取所有船型用于筛选
    ship_types = ShipType.objects.all()
    
    # 获取所有交船年份用于筛选
    delivery_years = Project.objects.values_list('delivery_date__year', flat=True).distinct().order_by('-delivery_date__year')
    
    # 分页
    paginator = Paginator(projects, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'ship_types': ship_types,
        'delivery_years': delivery_years,
        'search_query': search_query,
        'ship_type_filter': ship_type_filter,
        'delivery_year_filter': delivery_year_filter,
    }
    return render(request, 'drawings/project/list.html', context)


def project_add(request):
    """添加项目信息"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            project_name = request.POST.get('project_name')
            ship_type_id = request.POST.get('ship_type')
            classification_society = request.POST.get('classification_society')
            delivery_date_str = request.POST.get('delivery_date')
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not ship_type_id:
                raise ValueError("请选择所属船型")
            
            # 获取船型
            ship_type = ShipType.objects.get(id=ship_type_id)
            
            # 转换日期
            from datetime import datetime
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            
            # 创建项目信息
            project = Project.objects.create(
                project_name=project_name,
                ship_type=ship_type,
                classification_society=classification_society,
                delivery_date=delivery_date,
                is_active=is_active
            )
            
            # 重定向到项目信息列表页面
            return redirect('drawings:project_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            ship_types = ShipType.objects.all()
            return render(request, 'drawings/project/add.html', {
                'error_message': f'保存失败：{str(e)}',
                'ship_types': ship_types
            })
    
    # GET请求，显示表单
    ship_types = ShipType.objects.all()
    return render(request, 'drawings/project/add.html', {'ship_types': ship_types})


def project_edit(request, project_id):
    """编辑项目信息"""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            project_name = request.POST.get('project_name')
            ship_type_id = request.POST.get('ship_type')
            classification_society = request.POST.get('classification_society')
            delivery_date_str = request.POST.get('delivery_date')
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not ship_type_id:
                raise ValueError("请选择所属船型")
            
            # 获取船型
            ship_type = ShipType.objects.get(id=ship_type_id)
            
            # 转换日期
            from datetime import datetime
            delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
            
            # 更新项目信息
            project.project_name = project_name
            project.ship_type = ship_type
            project.classification_society = classification_society
            project.delivery_date = delivery_date
            project.is_active = is_active
            project.save()
            
            # 重定向到项目信息列表页面
            return redirect('drawings:project_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            ship_types = ShipType.objects.all()
            return render(request, 'drawings/project/edit.html', {
                'project': project,
                'ship_types': ship_types,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    ship_types = ShipType.objects.all()
    return render(request, 'drawings/project/edit.html', {
        'project': project,
        'ship_types': ship_types
    })


def project_delete(request, project_id):
    """删除项目信息"""
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('drawings:project_list')
    return render(request, 'drawings/project/delete.html', {'project': project})


# 分段管理视图
def section_list(request):
    """分段管理列表"""
    sections = Section.objects.all().select_related('project', 'section_type')
    
    # 搜索和筛选功能
    project_filter = request.GET.getlist('project')  # 支持多选
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    
    if project_filter:
        sections = sections.filter(project_id__in=project_filter)
    
    if start_date_filter and end_date_filter:
        # 筛选在此区间内所有在胎的分段（脱胎日期在此区间内）
        sections = sections.filter(off_block_date__range=[start_date_filter, end_date_filter])
    
    # 获取所有项目用于筛选
    projects = Project.objects.filter(is_active=True)
    
    # 分页
    paginator = Paginator(sections, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'projects': projects,
        'project_filter': project_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    }
    return render(request, 'drawings/section/list.html', context)


def section_add(request):
    """添加分段"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            section_number = request.POST.get('section_number')
            project_id = request.POST.get('project')
            section_type_id = request.POST.get('section_type')
            planned_start_date_str = request.POST.get('planned_start_date')
            on_block_date_str = request.POST.get('on_block_date')
            off_block_date_str = request.POST.get('off_block_date')
            end_date_str = request.POST.get('end_date')
            block_number = request.POST.get('block_number')
            model_received = request.POST.get('model_received') == 'on'
            bom_received = request.POST.get('bom_received') == 'on'
            start_conditions_met = request.POST.get('start_conditions_met') == 'on'
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not project_id:
                raise ValueError("请选择所属项目")
            if not section_type_id:
                raise ValueError("请选择分段类型")
            
            # 获取关联对象
            project = Project.objects.get(id=project_id)
            section_type = TypicalSection.objects.get(id=section_type_id)
            
            # 转换日期
            from datetime import datetime
            planned_start_date = datetime.strptime(planned_start_date_str, '%Y-%m-%d').date() if planned_start_date_str else None
            on_block_date = datetime.strptime(on_block_date_str, '%Y-%m-%d').date() if on_block_date_str else None
            off_block_date = datetime.strptime(off_block_date_str, '%Y-%m-%d').date() if off_block_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            
            # 创建分段
            section = Section.objects.create(
                section_number=section_number,
                project=project,
                section_type=section_type,
                planned_start_date=planned_start_date,
                on_block_date=on_block_date,
                off_block_date=off_block_date,
                end_date=end_date,
                block_number=block_number,
                model_received=model_received,
                bom_received=bom_received,
                start_conditions_met=start_conditions_met,
                is_active=is_active
            )
            
            # 重定向到分段列表页面
            return redirect('drawings:section_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            projects = Project.objects.filter(is_active=True)
            typical_sections = TypicalSection.objects.filter(is_active=True)
            return render(request, 'drawings/section/add.html', {
                'error_message': f'保存失败：{str(e)}',
                'projects': projects,
                'typical_sections': typical_sections
            })
    
    # GET请求，显示表单
    projects = Project.objects.filter(is_active=True)
    typical_sections = TypicalSection.objects.filter(is_active=True)
    return render(request, 'drawings/section/add.html', {
        'projects': projects,
        'typical_sections': typical_sections
    })


def section_edit(request, section_id):
    """编辑分段"""
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            section_number = request.POST.get('section_number')
            project_id = request.POST.get('project')
            section_type_id = request.POST.get('section_type')
            planned_start_date_str = request.POST.get('planned_start_date')
            on_block_date_str = request.POST.get('on_block_date')
            off_block_date_str = request.POST.get('off_block_date')
            end_date_str = request.POST.get('end_date')
            block_number = request.POST.get('block_number')
            model_received = request.POST.get('model_received') == 'on'
            bom_received = request.POST.get('bom_received') == 'on'
            start_conditions_met = request.POST.get('start_conditions_met') == 'on'
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not project_id:
                raise ValueError("请选择所属项目")
            if not section_type_id:
                raise ValueError("请选择分段类型")
            
            # 获取关联对象
            project = Project.objects.get(id=project_id)
            section_type = TypicalSection.objects.get(id=section_type_id)
            
            # 转换日期
            from datetime import datetime
            planned_start_date = datetime.strptime(planned_start_date_str, '%Y-%m-%d').date() if planned_start_date_str else None
            on_block_date = datetime.strptime(on_block_date_str, '%Y-%m-%d').date() if on_block_date_str else None
            off_block_date = datetime.strptime(off_block_date_str, '%Y-%m-%d').date() if off_block_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            
            # 更新分段
            section.section_number = section_number
            section.project = project
            section.section_type = section_type
            section.planned_start_date = planned_start_date
            section.on_block_date = on_block_date
            section.off_block_date = off_block_date
            section.end_date = end_date
            section.block_number = block_number
            section.model_received = model_received
            section.bom_received = bom_received
            section.start_conditions_met = start_conditions_met
            section.is_active = is_active
            section.save()
            
            # 重定向到分段列表页面
            return redirect('drawings:section_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            projects = Project.objects.filter(is_active=True)
            typical_sections = TypicalSection.objects.filter(is_active=True)
            return render(request, 'drawings/section/edit.html', {
                'section': section,
                'projects': projects,
                'typical_sections': typical_sections,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    projects = Project.objects.filter(is_active=True)
    typical_sections = TypicalSection.objects.filter(is_active=True)
    return render(request, 'drawings/section/edit.html', {
        'section': section,
        'projects': projects,
        'typical_sections': typical_sections
    })


def section_delete(request, section_id):
    """删除分段"""
    section = get_object_or_404(Section, id=section_id)
    if request.method == 'POST':
        section.delete()
        return redirect('drawings:section_list')
    return render(request, 'drawings/section/delete.html', {'section': section})


def section_import(request):
    """导入Excel文件"""
    if request.method == 'POST':
        try:
            # 处理Excel文件上传
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                raise ValueError("请选择要上传的Excel文件")
            
            # TODO: 实现Excel文件解析和导入逻辑
            # 这里需要根据具体的Excel格式来实现解析逻辑
            
            return redirect('drawings:section_list')
            
        except Exception as e:
            return render(request, 'drawings/section/import.html', {
                'error_message': f'导入失败：{str(e)}'
            })
    
    return render(request, 'drawings/section/import.html')


# 托盘管理视图
def pallet_list(request):
    """托盘列表"""
    pallets = Pallet.objects.select_related('project', 'section').all()
    
    # 获取筛选参数
    project_filter = request.GET.getlist('project')
    section_filter = request.GET.getlist('section')
    required_date_start = request.GET.get('required_date_start')
    required_date_end = request.GET.get('required_date_end')
    is_received_filter = request.GET.get('is_received')
    search_code = request.GET.get('search_code', '').strip()
    
    # 应用筛选条件
    if project_filter:
        pallets = pallets.filter(project_id__in=project_filter)
    
    if section_filter:
        pallets = pallets.filter(section_id__in=section_filter)
    
    if required_date_start:
        pallets = pallets.filter(required_date__gte=required_date_start)
    
    if required_date_end:
        pallets = pallets.filter(required_date__lte=required_date_end)
    
    if is_received_filter in ['true', 'false']:
        is_received = is_received_filter == 'true'
        pallets = pallets.filter(is_received=is_received)
    
    if search_code:
        pallets = pallets.filter(models.Q(pallet_code__icontains=search_code) | 
                                models.Q(pallet_name__icontains=search_code))
    
    # 分页
    paginator = Paginator(pallets, 10)  # 每页显示10项
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取筛选用的数据
    projects = Project.objects.filter(is_active=True)
    sections = Section.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'projects': projects,
        'sections': sections,
        'project_filter': project_filter,
        'section_filter': section_filter,
        'required_date_start_filter': required_date_start,
        'required_date_end_filter': required_date_end,
        'is_received_filter': is_received_filter,
        'search_code_filter': search_code,
    }
    
    return render(request, 'drawings/pallet/list.html', context)


def pallet_add(request):
    """添加托盘"""
    if request.method == 'POST':
        try:
            # 获取表单数据
            pallet_code = request.POST.get('pallet_code')
            pallet_name = request.POST.get('pallet_name')
            project_id = request.POST.get('project')
            section_id = request.POST.get('section')
            pallet_details = request.POST.get('pallet_details', '')
            required_date_str = request.POST.get('required_date')
            is_received = request.POST.get('is_received') == 'on'
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not project_id:
                raise ValueError("请选择所属项目")
            if not section_id:
                raise ValueError("请选择所属分段")
            
            # 获取关联对象
            project = Project.objects.get(id=project_id)
            section = Section.objects.get(id=section_id)
            
            # 转换日期
            from datetime import datetime
            required_date = datetime.strptime(required_date_str, '%Y-%m-%d').date() if required_date_str else None
            
            # 创建托盘
            pallet = Pallet.objects.create(
                pallet_code=pallet_code,
                pallet_name=pallet_name,
                project=project,
                section=section,
                pallet_details=pallet_details,
                required_date=required_date,
                is_received=is_received,
                is_active=is_active
            )
            
            # 重定向到托盘列表页面
            return redirect('drawings:pallet_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            projects = Project.objects.filter(is_active=True)
            sections = Section.objects.filter(is_active=True)
            return render(request, 'drawings/pallet/add.html', {
                'projects': projects,
                'sections': sections,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    projects = Project.objects.filter(is_active=True)
    sections = Section.objects.filter(is_active=True)
    return render(request, 'drawings/pallet/add.html', {
        'projects': projects,
        'sections': sections
    })


def pallet_edit(request, pallet_id):
    """编辑托盘"""
    pallet = get_object_or_404(Pallet, id=pallet_id)
    if request.method == 'POST':
        try:
            # 获取表单数据
            pallet_code = request.POST.get('pallet_code')
            pallet_name = request.POST.get('pallet_name')
            project_id = request.POST.get('project')
            section_id = request.POST.get('section')
            pallet_details = request.POST.get('pallet_details', '')
            required_date_str = request.POST.get('required_date')
            is_received = request.POST.get('is_received') == 'on'
            is_active = request.POST.get('is_active') == '1'
            
            # 验证必填字段
            if not project_id:
                raise ValueError("请选择所属项目")
            if not section_id:
                raise ValueError("请选择所属分段")
            
            # 获取关联对象
            project = Project.objects.get(id=project_id)
            section = Section.objects.get(id=section_id)
            
            # 转换日期
            from datetime import datetime
            required_date = datetime.strptime(required_date_str, '%Y-%m-%d').date() if required_date_str else None
            
            # 更新托盘
            pallet.pallet_code = pallet_code
            pallet.pallet_name = pallet_name
            pallet.project = project
            pallet.section = section
            pallet.pallet_details = pallet_details
            pallet.required_date = required_date
            pallet.is_received = is_received
            pallet.is_active = is_active
            pallet.save()
            
            # 重定向到托盘列表页面
            return redirect('drawings:pallet_list')
            
        except Exception as e:
            # 如果出现错误，返回错误信息
            projects = Project.objects.filter(is_active=True)
            sections = Section.objects.filter(is_active=True)
            return render(request, 'drawings/pallet/edit.html', {
                'pallet': pallet,
                'projects': projects,
                'sections': sections,
                'error_message': f'保存失败：{str(e)}'
            })
    
    # GET请求，显示表单
    projects = Project.objects.filter(is_active=True)
    sections = Section.objects.filter(is_active=True)
    return render(request, 'drawings/pallet/edit.html', {
        'pallet': pallet,
        'projects': projects,
        'sections': sections
    })


def pallet_delete(request, pallet_id):
    """删除托盘"""
    pallet = get_object_or_404(Pallet, id=pallet_id)
    if request.method == 'POST':
        pallet.delete()
        return redirect('drawings:pallet_list')
    return render(request, 'drawings/pallet/delete.html', {'pallet': pallet})


def pallet_import(request):
    """导入Excel文件"""
    if request.method == 'POST':
        try:
            # 处理Excel文件上传
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                raise ValueError("请选择要上传的Excel文件")
            
            # TODO: 实现Excel文件解析和导入逻辑
            # 这里需要根据具体的Excel格式来实现解析逻辑
            
            return redirect('drawings:pallet_list')
            
        except Exception as e:
            return render(request, 'drawings/pallet/import.html', {
                'error_message': f'导入失败：{str(e)}'
            })
    
    return render(request, 'drawings/pallet/import.html')

# 标准工艺流程相关视图
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import StandardProcessFlow, ProcessFlowStep, ShipType, TypicalSection, WorkProcess


def standard_process_flow_list(request):
    """标准工艺流程列表"""
    # 获取筛选参数
    ship_type_filter = request.GET.getlist('ship_type')
    typical_section_filter = request.GET.getlist('typical_section')
    search_query = request.GET.get('search', '')
    
    # 查询工艺流程
    queryset = StandardProcessFlow.objects.select_related('ship_type', 'typical_section').filter(is_active=True)
    
    # 应用筛选条件
    if ship_type_filter:
        queryset = queryset.filter(ship_type__id__in=ship_type_filter)
    if typical_section_filter:
        queryset = queryset.filter(typical_section__id__in=typical_section_filter)
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(ship_type__ship_type__icontains=search_query) |
            Q(typical_section__section_name__icontains=search_query)
        )
    
    # 分页
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # 获取筛选选项
    ship_types = ShipType.objects.all()
    typical_sections = TypicalSection.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'ship_types': ship_types,
        'typical_sections': typical_sections,
        'ship_type_filter': ship_type_filter,
        'typical_section_filter': typical_section_filter,
        'search_query': search_query,
    }
    
    return render(request, 'drawings/standard_process_flow/list.html', context)


def standard_process_flow_add(request):
    """新增标准工艺流程"""
    if request.method == 'POST':
        # 处理表单提交
        name = request.POST.get('name')
        ship_type_id = request.POST.get('ship_type')
        typical_section_id = request.POST.get('typical_section')
        description = request.POST.get('description')
        
        if name and ship_type_id and typical_section_id:
            try:
                ship_type = ShipType.objects.get(id=ship_type_id)
                typical_section = TypicalSection.objects.get(id=typical_section_id)
                
                process_flow = StandardProcessFlow.objects.create(
                    name=name,
                    ship_type=ship_type,
                    typical_section=typical_section,
                    description=description
                )
                
                messages.success(request, '标准工艺流程创建成功！')
                return redirect('drawings:standard_process_flow_edit', process_flow.id)
            except (ShipType.DoesNotExist, TypicalSection.DoesNotExist):
                messages.error(request, '选择的船型或典型分段不存在！')
        else:
            messages.error(request, '请填写所有必填字段！')
    
    # 获取选项数据
    ship_types = ShipType.objects.all()
    typical_sections = TypicalSection.objects.filter(is_active=True)
    
    context = {
        'ship_types': ship_types,
        'typical_sections': typical_sections,
    }
    
    return render(request, 'drawings/standard_process_flow/add.html', context)


def standard_process_flow_edit(request, process_flow_id):
    """编辑标准工艺流程"""
    process_flow = get_object_or_404(StandardProcessFlow, id=process_flow_id)
    
    if request.method == 'POST':
        # 处理基本信息更新
        if 'update_basic' in request.POST:
            name = request.POST.get('name')
            description = request.POST.get('description')
            
            if name:
                process_flow.name = name
                process_flow.description = description
                process_flow.save()
                messages.success(request, '基本信息更新成功！')
            else:
                messages.error(request, '工艺流程名称不能为空！')
        
        # 处理步骤更新
        elif 'update_steps' in request.POST:
            # 获取所有步骤数据
            step_ids = request.POST.getlist('step_id')
            step_names = request.POST.getlist('step_name')
            work_process_ids = request.POST.getlist('work_process_id')
            step_orders = request.POST.getlist('step_order')
            parallel_groups = request.POST.getlist('parallel_group')
            estimated_hours = request.POST.getlist('estimated_hours')
            descriptions = request.POST.getlist('description')
            
            # 删除现有步骤
            ProcessFlowStep.objects.filter(process_flow=process_flow).delete()
            
            # 创建新步骤
            for i in range(len(step_ids)):
                if step_names[i] and work_process_ids[i] and step_orders[i]:
                    try:
                        work_process = WorkProcess.objects.get(id=work_process_ids[i])
                        ProcessFlowStep.objects.create(
                            process_flow=process_flow,
                            work_process=work_process,
                            step_name=step_names[i],
                            step_order=int(step_orders[i]),
                            parallel_group=int(parallel_groups[i]) if parallel_groups[i] else 0,
                            estimated_hours=float(estimated_hours[i]) if estimated_hours[i] else 0,
                            description=descriptions[i]
                        )
                    except (WorkProcess.DoesNotExist, ValueError):
                        continue
            
            messages.success(request, '工艺流程步骤更新成功！')
            process_flow.save()  # 重新计算总工时
    
    # 获取步骤数据
    steps = ProcessFlowStep.objects.filter(process_flow=process_flow).order_by('step_order', 'parallel_group')
    
    # 获取可选的作业工序
    work_processes = WorkProcess.objects.filter(is_active=True).select_related('work_type')
    
    context = {
        'process_flow': process_flow,
        'steps': steps,
        'work_processes': work_processes,
    }
    
    return render(request, 'drawings/standard_process_flow/edit.html', context)


def standard_process_flow_delete(request, process_flow_id):
    """删除标准工艺流程"""
    process_flow = get_object_or_404(StandardProcessFlow, id=process_flow_id)
    
    if request.method == 'POST':
        process_flow.is_active = False
        process_flow.save()
        messages.success(request, '标准工艺流程删除成功！')
        return redirect('drawings:standard_process_flow_list')
    
    context = {
        'process_flow': process_flow,
    }
    
    return render(request, 'drawings/standard_process_flow/delete.html', context)


def standard_process_flow_detail(request, process_flow_id):
    """查看标准工艺流程详情"""
    process_flow = get_object_or_404(StandardProcessFlow, id=process_flow_id)
    steps = ProcessFlowStep.objects.filter(process_flow=process_flow).order_by('step_order', 'parallel_group')
    
    context = {
        'process_flow': process_flow,
        'steps': steps,
    }
    
    return render(request, 'drawings/standard_process_flow/detail.html', context)
