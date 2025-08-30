from django.core.management.base import BaseCommand
from drawings.models import Role, Permission, RolePermission

class Command(BaseCommand):
    help = '初始化权限管理数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化权限管理数据...')
        
        # 1. 创建角色
        roles_data = [
            {
                'name': '系统管理员',
                'description': '拥有系统所有权限，可以管理所有模块和用户'
            },
            {
                'name': '设计人员',
                'description': '负责图纸设计工作，可以查看和编辑图纸相关数据'
            },
            {
                'name': '生产管理人员',
                'description': '负责生产管理，可以查看项目和生产相关数据'
            },
            {
                'name': '生产人员',
                'description': '负责具体生产工作，可以查看生产相关数据'
            },
            {
                'name': '设计管理人员',
                'description': '负责设计团队管理，可以管理设计相关数据和人员'
            }
        ]
        
        created_roles = {}
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults=role_data
            )
            created_roles[role.name] = role
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 创建角色: {role.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ 角色已存在: {role.name}')
                )
        
        # 2. 创建权限
        permissions_data = [
            # 船型管理权限
            {'module': 'ship_type', 'action': 'view', 'description': '查看船型信息'},
            {'module': 'ship_type', 'action': 'add', 'description': '新增船型'},
            {'module': 'ship_type', 'action': 'edit', 'description': '编辑船型'},
            {'module': 'ship_type', 'action': 'delete', 'description': '删除船型'},
            
            # 项目管理权限
            {'module': 'project', 'action': 'view', 'description': '查看项目信息'},
            {'module': 'project', 'action': 'add', 'description': '新增项目'},
            {'module': 'project', 'action': 'edit', 'description': '编辑项目'},
            {'module': 'project', 'action': 'delete', 'description': '删除项目'},
            
            # 图纸类别管理权限
            {'module': 'drawing_category', 'action': 'view', 'description': '查看图纸类别'},
            {'module': 'drawing_category', 'action': 'add', 'description': '新增图纸类别'},
            {'module': 'drawing_category', 'action': 'edit', 'description': '编辑图纸类别'},
            {'module': 'drawing_category', 'action': 'delete', 'description': '删除图纸类别'},
            
            # 图纸管理权限
            {'module': 'drawing', 'action': 'view', 'description': '查看图纸'},
            {'module': 'drawing', 'action': 'add', 'description': '新增图纸'},
            {'module': 'drawing', 'action': 'edit', 'description': '编辑图纸'},
            {'module': 'drawing', 'action': 'delete', 'description': '删除图纸'},
            {'module': 'drawing', 'action': 'export', 'description': '导出图纸'},
            {'module': 'drawing', 'action': 'import', 'description': '导入图纸'},
            
            # 编码规则管理权限
            {'module': 'code_rule', 'action': 'view', 'description': '查看编码规则'},
            {'module': 'code_rule', 'action': 'add', 'description': '新增编码规则'},
            {'module': 'code_rule', 'action': 'edit', 'description': '编辑编码规则'},
            {'module': 'code_rule', 'action': 'delete', 'description': '删除编码规则'},
            
            # 角色管理权限
            {'module': 'role', 'action': 'view', 'description': '查看角色'},
            {'module': 'role', 'action': 'add', 'description': '新增角色'},
            {'module': 'role', 'action': 'edit', 'description': '编辑角色'},
            {'module': 'role', 'action': 'delete', 'description': '删除角色'},
            
            # 人员管理权限
            {'module': 'person', 'action': 'view', 'description': '查看人员'},
            {'module': 'person', 'action': 'add', 'description': '新增人员'},
            {'module': 'person', 'action': 'edit', 'description': '编辑人员'},
            {'module': 'person', 'action': 'delete', 'description': '删除人员'},
            
            # 权限管理权限
            {'module': 'permission', 'action': 'view', 'description': '查看权限'},
            {'module': 'permission', 'action': 'add', 'description': '新增权限'},
            {'module': 'permission', 'action': 'edit', 'description': '编辑权限'},
            {'module': 'permission', 'action': 'delete', 'description': '删除权限'},
        ]
        
        created_permissions = {}
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                module=perm_data['module'],
                action=perm_data['action'],
                defaults=perm_data
            )
            created_permissions[f"{perm_data['module']}_{perm_data['action']}"] = permission
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ 创建权限: {permission}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ 权限已存在: {permission}')
                )
        
        # 3. 为角色分配权限
        role_permissions = {
            '系统管理员': [
                # 所有权限
                'ship_type_view', 'ship_type_add', 'ship_type_edit', 'ship_type_delete',
                'project_view', 'project_add', 'project_edit', 'project_delete',
                'drawing_category_view', 'drawing_category_add', 'drawing_category_edit', 'drawing_category_delete',
                'drawing_view', 'drawing_add', 'drawing_edit', 'drawing_delete', 'drawing_export', 'drawing_import',
                'code_rule_view', 'code_rule_add', 'code_rule_edit', 'code_rule_delete',
                'role_view', 'role_add', 'role_edit', 'role_delete',
                'person_view', 'person_add', 'person_edit', 'person_delete',
                'permission_view', 'permission_add', 'permission_edit', 'permission_delete',
            ],
            '设计人员': [
                # 设计相关权限
                'ship_type_view',
                'project_view',
                'drawing_category_view',
                'drawing_view', 'drawing_add', 'drawing_edit', 'drawing_export',
                'code_rule_view',
            ],
            '生产管理人员': [
                # 生产管理相关权限
                'ship_type_view',
                'project_view', 'project_add', 'project_edit',
                'drawing_category_view',
                'drawing_view', 'drawing_export',
                'code_rule_view',
            ],
            '生产人员': [
                # 生产相关权限
                'ship_type_view',
                'project_view',
                'drawing_category_view',
                'drawing_view',
                'code_rule_view',
            ],
            '设计管理人员': [
                # 设计管理相关权限
                'ship_type_view', 'ship_type_add', 'ship_type_edit',
                'project_view', 'project_add', 'project_edit',
                'drawing_category_view', 'drawing_category_add', 'drawing_category_edit',
                'drawing_view', 'drawing_add', 'drawing_edit', 'drawing_export', 'drawing_import',
                'code_rule_view', 'code_rule_add', 'code_rule_edit',
                'person_view',
            ],
        }
        
        for role_name, permission_keys in role_permissions.items():
            role = created_roles.get(role_name)
            if role:
                for perm_key in permission_keys:
                    permission = created_permissions.get(perm_key)
                    if permission:
                        role_perm, created = RolePermission.objects.get_or_create(
                            role=role,
                            permission=permission
                        )
                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(f'✓ 为角色 {role.name} 分配权限: {permission}')
                            )
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'⚠ 角色 {role.name} 已有权限: {permission}')
                            )
        
        self.stdout.write(
            self.style.SUCCESS('权限管理数据初始化完成！')
        )
