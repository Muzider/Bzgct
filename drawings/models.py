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


class Project(models.Model):
    """项目信息表"""
    project_name = models.CharField(max_length=200, verbose_name='项目名称', unique=True)
    ship_type = models.ForeignKey(ShipType, on_delete=models.CASCADE, verbose_name='所属船型')
    classification_society = models.CharField(max_length=100, verbose_name='所属船级社')
    delivery_date = models.DateField(verbose_name='交船日期')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '项目信息'
        verbose_name_plural = '项目信息'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.project_name} - {self.ship_type.ship_type}"

    @property
    def delivery_year(self):
        """获取交船年份"""
        return self.delivery_date.year if self.delivery_date else None


class Section(models.Model):
    """分段管理表"""
    section_number = models.CharField(max_length=50, verbose_name='分段号', unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    section_type = models.ForeignKey(TypicalSection, on_delete=models.CASCADE, verbose_name='分段类型')
    planned_start_date = models.DateField(verbose_name='计划开始时间')
    on_block_date = models.DateField(verbose_name='上胎日期')
    off_block_date = models.DateField(verbose_name='下胎日期')
    end_date = models.DateField(verbose_name='结束时间')
    block_number = models.CharField(max_length=20, verbose_name='胎架号')
    model_received = models.BooleanField(default=False, verbose_name='模型接收')
    bom_received = models.BooleanField(default=False, verbose_name='BOM接收')
    start_conditions_met = models.BooleanField(default=False, verbose_name='满足开工条件')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '分段管理'
        verbose_name_plural = '分段管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.section_number} - {self.project.project_name}"

    @property
    def on_block_cycle(self):
        """计算在胎周期（天数）"""
        if self.on_block_date and self.off_block_date:
            return (self.off_block_date - self.on_block_date).days
        return 0


class Pallet(models.Model):
    """托盘管理表"""
    pallet_code = models.CharField(max_length=50, verbose_name='托盘编码', unique=True)
    pallet_name = models.CharField(max_length=100, verbose_name='托盘名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='所属分段')
    pallet_details = models.TextField(verbose_name='托盘明细', help_text='例如：零部件c1、c2、b1、b2等，或舾装件条目')
    required_date = models.DateField(verbose_name='需求日期', blank=True, null=True)
    is_received = models.BooleanField(default=False, verbose_name='是否接收')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '托盘管理'
        verbose_name_plural = '托盘管理'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.pallet_name} - {self.project.project_name}"


class StandardProcessFlow(models.Model):
    """标准工艺流程表"""
    name = models.CharField(max_length=200, verbose_name='工艺流程名称')
    ship_type = models.ForeignKey(ShipType, on_delete=models.CASCADE, verbose_name='船型')
    typical_section = models.ForeignKey(TypicalSection, on_delete=models.CASCADE, verbose_name='典型分段')
    description = models.TextField(verbose_name='工艺流程描述', blank=True, null=True)
    estimated_total_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='预估总工时', default=0)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '标准工艺流程'
        verbose_name_plural = '标准工艺流程'
        unique_together = ['ship_type', 'typical_section', 'name']
        ordering = ['ship_type', 'typical_section', 'name']

    def __str__(self):
        return f"{self.ship_type.ship_type} - {self.typical_section.section_name} - {self.name}"

    def save(self, *args, **kwargs):
        # 自动计算预估总工时
        total_hours = sum(
            step.estimated_hours for step in self.processflowstep_set.all()
        )
        self.estimated_total_hours = total_hours
        super().save(*args, **kwargs)


class ProcessFlowStep(models.Model):
    """工艺流程步骤表"""
    PARALLEL_TYPE_CHOICES = [
        ('sequential', '顺序执行'),
        ('parallel', '并行执行'),
    ]
    
    process_flow = models.ForeignKey(StandardProcessFlow, on_delete=models.CASCADE, verbose_name='所属工艺流程')
    work_process = models.ForeignKey(WorkProcess, on_delete=models.CASCADE, verbose_name='作业工序')
    step_name = models.CharField(max_length=100, verbose_name='步骤名称')
    step_order = models.PositiveIntegerField(verbose_name='步骤顺序')
    parallel_group = models.PositiveIntegerField(verbose_name='并行组号', default=0, 
                                               help_text='相同组号的步骤可以并行执行，0表示顺序执行')
    estimated_hours = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='预估工时')
    prerequisites = models.ManyToManyField('self', blank=True, verbose_name='前置步骤',
                                         help_text='必须在此步骤之前完成的步骤')
    description = models.TextField(verbose_name='步骤描述', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '工艺流程步骤'
        verbose_name_plural = '工艺流程步骤'
        unique_together = ['process_flow', 'step_order']
        ordering = ['process_flow', 'step_order', 'parallel_group']

    def __str__(self):
        return f"{self.process_flow.name} - 步骤{self.step_order}: {self.step_name}"

    def save(self, *args, **kwargs):
        # 如果没有设置预估工时，使用作业工序的工时
        if not self.estimated_hours and self.work_process.work_hours:
            self.estimated_hours = self.work_process.work_hours
        super().save(*args, **kwargs)
