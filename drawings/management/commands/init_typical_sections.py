from django.core.management.base import BaseCommand
from drawings.models import ShipType, TypicalSection

class Command(BaseCommand):
    help = '初始化典型分段数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化典型分段数据...')

        # 获取船型
        ship_types = {}
        for ship_type in ShipType.objects.all():
            ship_types[ship_type.ship_type] = ship_type

        # 典型分段数据
        typical_sections_data = [
            # 散货船典型分段
            {'ship_type_name': '散货船', 'section_name': '双层底分段', 'section_code': 'DB001', 'description': '散货船双层底结构分段，包含内底板、外底板、纵骨等'},
            {'ship_type_name': '散货船', 'section_name': '甲板分段', 'section_code': 'DK001', 'description': '散货船甲板结构分段，包含甲板板、甲板纵骨、横梁等'},
            {'ship_type_name': '散货船', 'section_name': '槽型舱壁分段', 'section_code': 'CB001', 'description': '散货船槽型舱壁分段，用于分隔货舱'},
            {'ship_type_name': '散货船', 'section_name': '舷侧分段', 'section_code': 'SS001', 'description': '散货船舷侧结构分段，包含舷侧外板、肋骨等'},
            
            # 集装箱船典型分段
            {'ship_type_name': '集装箱船', 'section_name': '抗扭箱分段', 'section_code': 'TB001', 'description': '集装箱船抗扭箱结构分段，用于承受扭转载荷'},
            {'ship_type_name': '集装箱船', 'section_name': '绑扎桥分段', 'section_code': 'LB001', 'description': '集装箱船绑扎桥结构分段，用于集装箱绑扎'},
            {'ship_type_name': '集装箱船', 'section_name': '甲板分段', 'section_code': 'DK002', 'description': '集装箱船甲板结构分段，包含甲板板、甲板纵骨等'},
            {'ship_type_name': '集装箱船', 'section_name': '舷侧分段', 'section_code': 'SS002', 'description': '集装箱船舷侧结构分段，包含舷侧外板、肋骨等'},
            
            # 油船典型分段
            {'ship_type_name': '油船', 'section_name': '双层底分段', 'section_code': 'DB002', 'description': '油船双层底结构分段，用于保护船底'},
            {'ship_type_name': '油船', 'section_name': '甲板分段', 'section_code': 'DK003', 'description': '油船甲板结构分段，包含甲板板、甲板纵骨等'},
            {'ship_type_name': '油船', 'section_name': '舱壁分段', 'section_code': 'BW001', 'description': '油船舱壁分段，用于分隔油舱'},
            {'ship_type_name': '油船', 'section_name': '舷侧分段', 'section_code': 'SS003', 'description': '油船舷侧结构分段，包含舷侧外板、肋骨等'},
            
            # 液化气船典型分段
            {'ship_type_name': '液化气船', 'section_name': 'LNG舱分段', 'section_code': 'LNG001', 'description': '液化气船LNG舱结构分段，用于储存液化天然气'},
            {'ship_type_name': '液化气船', 'section_name': 'LPG舱分段', 'section_code': 'LPG001', 'description': '液化气船LPG舱结构分段，用于储存液化石油气'},
            {'ship_type_name': '液化气船', 'section_name': '甲板分段', 'section_code': 'DK004', 'description': '液化气船甲板结构分段，包含甲板板、甲板纵骨等'},
            
            # 化学品船典型分段
            {'ship_type_name': '化学品船', 'section_name': '化学品舱分段', 'section_code': 'CC001', 'description': '化学品船化学品舱结构分段，用于储存化学品'},
            {'ship_type_name': '化学品船', 'section_name': '甲板分段', 'section_code': 'DK005', 'description': '化学品船甲板结构分段，包含甲板板、甲板纵骨等'},
            {'ship_type_name': '化学品船', 'section_name': '舷侧分段', 'section_code': 'SS004', 'description': '化学品船舷侧结构分段，包含舷侧外板、肋骨等'},
        ]

        created_count = 0
        for section_data in typical_sections_data:
            ship_type_name = section_data['ship_type_name']
            if ship_type_name in ship_types:
                ship_type = ship_types[ship_type_name]
                try:
                    section, created = TypicalSection.objects.get_or_create(
                        ship_type=ship_type,
                        section_name=section_data['section_name'],
                        defaults=section_data
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'✓ 创建典型分段: {ship_type_name} - {section_data["section_name"]}'))
                        created_count += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'⚠ 典型分段已存在: {ship_type_name} - {section_data["section_name"]}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'✗ 创建典型分段失败: {ship_type_name} - {section_data["section_name"]}, 错误: {str(e)}'))
            else:
                self.stdout.write(self.style.ERROR(f'✗ 船型不存在: {ship_type_name}'))

        self.stdout.write(self.style.SUCCESS(f'典型分段数据初始化完成！共创建 {created_count} 个新典型分段。'))
