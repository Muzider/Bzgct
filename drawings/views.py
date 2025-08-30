from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db import models
from django.core.paginator import Paginator
from .models import Role, Person, Permission, RolePermission, PersonRole, ShipType, TypicalSection, WorkType, WorkProcess

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
