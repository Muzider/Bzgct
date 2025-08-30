from django.core.management.base import BaseCommand
from drawings.models import ShipType

class Command(BaseCommand):
    help = '初始化船型数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化船型数据...')

        # 船型数据
        ship_types_data = [
            {'ship_type': '散货船', 'ship_subtype': '巴拿马型'},
            {'ship_type': '散货船', 'ship_subtype': '好望角型'},
            {'ship_type': '散货船', 'ship_subtype': '苏伊士型'},
            {'ship_type': '集装箱船', 'ship_subtype': '超大型'},
            {'ship_type': '集装箱船', 'ship_subtype': '大型'},
            {'ship_type': '集装箱船', 'ship_subtype': '中型'},
            {'ship_type': '油船', 'ship_subtype': '超大型'},
            {'ship_type': '油船', 'ship_subtype': '大型'},
            {'ship_type': '油船', 'ship_subtype': '中型'},
            {'ship_type': '液化气船', 'ship_subtype': 'LNG船'},
            {'ship_type': '液化气船', 'ship_subtype': 'LPG船'},
            {'ship_type': '化学品船', 'ship_subtype': '专用型'},
            {'ship_type': '化学品船', 'ship_subtype': '通用型'},
        ]

        created_count = 0
        for ship_type_data in ship_types_data:
            try:
                ship_type, created = ShipType.objects.get_or_create(
                    ship_type=ship_type_data['ship_type'],
                    ship_subtype=ship_type_data['ship_subtype'],
                    defaults=ship_type_data
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ 创建船型: {ship_type.ship_type} - {ship_type.ship_subtype}'))
                    created_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f'⚠ 船型已存在: {ship_type.ship_type} - {ship_type.ship_subtype}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ 创建船型失败: {ship_type_data["ship_type"]} - {ship_type_data["ship_subtype"]}, 错误: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'船型数据初始化完成！共创建 {created_count} 个新船型。'))
