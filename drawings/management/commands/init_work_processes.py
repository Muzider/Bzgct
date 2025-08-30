from django.core.management.base import BaseCommand
from drawings.models import WorkProcess, WorkType
from decimal import Decimal

class Command(BaseCommand):
    help = '初始化作业工序数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化作业工序数据...')

        # 获取工种
        work_types = {}
        for work_type in WorkType.objects.all():
            work_types[work_type.work_type_name] = work_type

        # 作业工序数据
        work_processes_data = [
            # 焊接工相关工序
            {'process_name': '拼板焊接', 'process_code': 'HB001', 'work_type_name': '焊接工', 'coefficient': Decimal('1.2'), 'description': '钢板拼板焊接工序，需要较高技能'},
            {'process_name': '组件焊接', 'process_code': 'HB002', 'work_type_name': '焊接工', 'coefficient': Decimal('1.0'), 'description': '组件焊接工序'},
            {'process_name': '立焊', 'process_code': 'HB003', 'work_type_name': '焊接工', 'coefficient': Decimal('1.5'), 'description': '立焊工序，难度较高'},
            {'process_name': '仰焊', 'process_code': 'HB004', 'work_type_name': '焊接工', 'coefficient': Decimal('1.8'), 'description': '仰焊工序，难度最高'},
            
            # 装配工相关工序
            {'process_name': '装配', 'process_code': 'AZ001', 'work_type_name': '装配工', 'coefficient': Decimal('1.0'), 'description': '结构件装配工序'},
            {'process_name': '划线', 'process_code': 'HX001', 'work_type_name': '装配工', 'coefficient': Decimal('0.8'), 'description': '划线标记工序'},
            {'process_name': '定位', 'process_code': 'DW001', 'work_type_name': '装配工', 'coefficient': Decimal('1.1'), 'description': '定位工序'},
            
            # 切割工相关工序
            {'process_name': '切割', 'process_code': 'QG001', 'work_type_name': '切割工', 'coefficient': Decimal('1.0'), 'description': '钢板切割工序'},
            {'process_name': '钻孔', 'process_code': 'ZK001', 'work_type_name': '切割工', 'coefficient': Decimal('0.9'), 'description': '钻孔工序'},
            {'process_name': '等离子切割', 'process_code': 'QG002', 'work_type_name': '切割工', 'coefficient': Decimal('1.3'), 'description': '等离子切割工序'},
            
            # 打磨工相关工序
            {'process_name': '打磨', 'process_code': 'DM001', 'work_type_name': '打磨工', 'coefficient': Decimal('1.0'), 'description': '表面打磨工序'},
            {'process_name': '抛光', 'process_code': 'DM002', 'work_type_name': '打磨工', 'coefficient': Decimal('1.2'), 'description': '表面抛光工序'},
            
            # 涂装工相关工序
            {'process_name': '涂装', 'process_code': 'TZ001', 'work_type_name': '涂装工', 'coefficient': Decimal('1.0'), 'description': '表面涂装工序'},
            {'process_name': '防腐处理', 'process_code': 'TZ002', 'work_type_name': '涂装工', 'coefficient': Decimal('1.4'), 'description': '防腐处理工序'},
            
            # 检验员相关工序
            {'process_name': '检验', 'process_code': 'JY001', 'work_type_name': '检验员', 'coefficient': Decimal('1.0'), 'description': '质量检验工序'},
            {'process_name': '无损检测', 'process_code': 'JY002', 'work_type_name': '检验员', 'coefficient': Decimal('1.5'), 'description': '无损检测工序'},
            
            # 搬运工相关工序
            {'process_name': '搬运', 'process_code': 'BY001', 'work_type_name': '搬运工', 'coefficient': Decimal('1.0'), 'description': '材料搬运工序'},
            {'process_name': '吊装', 'process_code': 'BY002', 'work_type_name': '搬运工', 'coefficient': Decimal('1.3'), 'description': '吊装工序'},
        ]

        created_count = 0
        for process_data in work_processes_data:
            try:
                work_type_name = process_data.pop('work_type_name')
                if work_type_name in work_types:
                    work_type = work_types[work_type_name]
                    process_data['work_type'] = work_type
                    
                    process, created = WorkProcess.objects.get_or_create(
                        process_name=process_data['process_name'],
                        defaults=process_data
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✓ 创建作业工序: {process_data["process_name"]} (关联工种: {work_type_name})'))
                        created_count += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠ 作业工序已存在: {process_data["process_name"]}'))
                else:
                    self.stdout.write(self.style.ERROR(f'✗ 工种不存在: {work_type_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ 创建作业工序失败: {process_data["process_name"]}, 错误: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'作业工序数据初始化完成！共创建 {created_count} 个新作业工序。'))
