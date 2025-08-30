from django.core.management.base import BaseCommand
from drawings.models import WorkType, WorkProcess

class Command(BaseCommand):
    help = '初始化作业工种数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化作业工种数据...')

        # 获取工序
        processes = {}
        for process in WorkProcess.objects.all():
            processes[process.process_name] = process

        # 作业工种数据
        work_types_data = [
            {
                'work_type_name': '焊接工',
                'work_type_code': 'W',
                'standard_hours': 8.0,
                'related_process_names': ['拼板焊接', '组件焊接'],
                'description': '负责各种焊接作业，包括拼板焊接、组件焊接等'
            },
            {
                'work_type_name': '装配工',
                'work_type_code': 'A',
                'standard_hours': 8.0,
                'related_process_names': ['装配', '划线'],
                'description': '负责结构件装配和划线标记工作'
            },
            {
                'work_type_name': '切割工',
                'work_type_code': 'C',
                'standard_hours': 8.0,
                'related_process_names': ['切割', '钻孔'],
                'description': '负责钢板切割和钻孔作业'
            },
            {
                'work_type_name': '打磨工',
                'work_type_code': 'G',
                'standard_hours': 8.0,
                'related_process_names': ['打磨'],
                'description': '负责表面打磨和抛光作业'
            },
            {
                'work_type_name': '涂装工',
                'work_type_code': 'T',
                'standard_hours': 8.0,
                'related_process_names': ['涂装'],
                'description': '负责表面涂装和防腐处理'
            },
            {
                'work_type_name': '检验员',
                'work_type_code': 'I',
                'standard_hours': 8.0,
                'related_process_names': ['检验'],
                'description': '负责质量检验和检测工作'
            },
            {
                'work_type_name': '搬运工',
                'work_type_code': 'B',
                'standard_hours': 8.0,
                'related_process_names': ['搬运'],
                'description': '负责材料搬运和运输工作'
            },
        ]

        created_count = 0
        for work_type_data in work_types_data:
            try:
                # 提取关联工序名称
                related_process_names = work_type_data.pop('related_process_names')
                
                # 创建或获取作业工种
                work_type, created = WorkType.objects.get_or_create(
                    work_type_name=work_type_data['work_type_name'],
                    defaults=work_type_data
                )
                
                if created:
                    # 添加关联工序
                    for process_name in related_process_names:
                        if process_name in processes:
                            work_type.related_processes.add(processes[process_name])
                    
                    self.stdout.write(self.style.SUCCESS(f'✓ 创建作业工种: {work_type_data["work_type_name"]}'))
                    created_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ 作业工种已存在: {work_type_data["work_type_name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ 创建作业工种失败: {work_type_data["work_type_name"]}, 错误: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'作业工种数据初始化完成！共创建 {created_count} 个新作业工种。'))
