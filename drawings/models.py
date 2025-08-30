from django.db import models
from decimal import Decimal, InvalidOperation

# Create your models here.

class ShipType(models.Model):
    """船型表"""
    ship_type = models.CharField(max_length=50, verbose_name='船型', unique=True)
    ship_subtype = models.CharField(max_length=100, verbose_name='船型细分', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '船型'
        verbose_name_plural = '船型'
        ordering = ['ship_type']
    
    def __str__(self):
        return self.ship_type


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=50, verbose_name='角色名称', unique=True)
    description = models.TextField(verbose_name='角色描述', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Person(models.Model):
    """人员表"""
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    
    name = models.CharField(max_length=50, verbose_name='姓名')
    employee_id = models.CharField(max_length=20, verbose_name='工号', unique=True)
    department = models.CharField(max_length=100, verbose_name='部门')
    position = models.CharField(max_length=100, verbose_name='职位')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='电话', blank=True, null=True)
    email = models.EmailField(verbose_name='邮箱', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否在职')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '人员'
        verbose_name_plural = '人员'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.employee_id})"


class Permission(models.Model):
    """权限表"""
    MODULE_CHOICES = [
        ('ship_type', '船型管理'),
        ('project', '项目管理'),
        ('drawing_category', '图纸类别管理'),
        ('drawing', '图纸管理'),
        ('code_rule', '编码规则管理'),
        ('role', '角色管理'),
        ('person', '人员管理'),
        ('permission', '权限管理'),
    ]
    
    ACTION_CHOICES = [
        ('view', '查看'),
        ('add', '新增'),
        ('edit', '编辑'),
        ('delete', '删除'),
        ('export', '导出'),
        ('import', '导入'),
    ]
    
    module = models.CharField(max_length=50, choices=MODULE_CHOICES, verbose_name='模块')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作')
    description = models.CharField(max_length=200, verbose_name='权限描述')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'
        unique_together = ['module', 'action']
        ordering = ['module', 'action']
    
    def __str__(self):
        return f"{self.get_module_display()} - {self.get_action_display()}"


class RolePermission(models.Model):
    """角色权限关联表"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '角色权限'
        verbose_name_plural = '角色权限'
        unique_together = ['role', 'permission']
        ordering = ['role', 'permission']
    
    def __str__(self):
        return f"{self.role.name} - {self.permission}"


class PersonRole(models.Model):
    """人员角色关联表"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, verbose_name='人员')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '人员角色'
        verbose_name_plural = '人员角色'
        unique_together = ['person', 'role']
        ordering = ['person', 'role']

    def __str__(self):
        return f"{self.person.name} - {self.role.name}"


class TypicalSection(models.Model):
    """典型分段表"""
    ship_type = models.ForeignKey(ShipType, on_delete=models.CASCADE, verbose_name='船型')
    section_name = models.CharField(max_length=100, verbose_name='分段名称')
    section_code = models.CharField(max_length=50, verbose_name='分段编码', blank=True, null=True)
    description = models.TextField(verbose_name='分段描述', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '典型分段'
        verbose_name_plural = '典型分段'
        unique_together = ['ship_type', 'section_name']
        ordering = ['ship_type', 'section_name']

    def __str__(self):
        return f"{self.ship_type.ship_type} - {self.section_name}"


class WorkType(models.Model):
    """作业工种表"""
    work_type_name = models.CharField(max_length=100, verbose_name='作业工种名称', unique=True)
    work_type_code = models.CharField(max_length=20, verbose_name='作业工种编码', unique=True)
    standard_hours = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='标准作业工时')
    description = models.TextField(verbose_name='工种描述', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '作业工种'
        verbose_name_plural = '作业工种'
        ordering = ['work_type_name']

    def __str__(self):
        return f"{self.work_type_name} ({self.work_type_code})"


class WorkProcess(models.Model):
    """作业工序表"""
    process_name = models.CharField(max_length=100, verbose_name='工序名称', unique=True)
    process_code = models.CharField(max_length=20, verbose_name='工序编码', unique=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='关联工种', null=True, blank=True)
    coefficient = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='工时系数', default=1.00)
    work_hours = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='作业工时', blank=True, null=True)
    description = models.TextField(verbose_name='工序描述', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '作业工序'
        verbose_name_plural = '作业工序'
        ordering = ['work_type', 'process_name']

    def __str__(self):
        return f"{self.process_name} ({self.process_code})"

    def save(self, *args, **kwargs):
        # 自动计算作业工时 = 标准工时 * 系数
        if self.work_type and self.coefficient:
            try:
                # 确保 standard_hours 是 Decimal 类型，即使它被错误地保存为其他类型
                standard_hours_decimal = Decimal(str(self.work_type.standard_hours))
                
                # 执行乘法运算
                self.work_hours = standard_hours_decimal * self.coefficient

            except (InvalidOperation, TypeError, ValueError) as e:
                # 捕获可能的类型转换错误,Value:
              print(f"Error calculating work hours: {e}")
                # 可以在这里记录日志或者抛出更友好的异常
        self.work_hours = None # 或者设置为一个默认值

        super().save(*args, **kwargs)
