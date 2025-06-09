import logging
from app import db
from models import MaterialType, Supplier, Material, MaterialSupplier
from datetime import datetime, date

def import_initial_data():
    """Импорт начальных данных в базу данных"""
    
    # Проверяем, есть ли уже данные в базе
    if MaterialType.query.first() is not None:
        logging.info("Database already contains data, skipping import")
        return
    
    try:
        # Добавляем типы материалов
        material_types_data = [
            {'name': 'Глина', 'description': 'Основное сырье для керамической плитки'},
            {'name': 'Песок', 'description': 'Кварцевый песок для производства'},
            {'name': 'Красители', 'description': 'Пигменты для окрашивания плитки'},
            {'name': 'Глазурь', 'description': 'Покрытие для финишной обработки'},
            {'name': 'Каолин', 'description': 'White clay для высококачественной керамики'},
        ]
        
        material_types = []
        for mt_data in material_types_data:
            mt = MaterialType(**mt_data)
            db.session.add(mt)
            material_types.append(mt)
        
        db.session.flush()  # Получаем ID типов материалов
        
        # Добавляем поставщиков
        suppliers_data = [
            {
                'name': 'ООО "Керамические материалы"',
                'inn': '7701234567',
                'rating': 8,
                'start_date': date(2020, 1, 15),
                'contact_phone': '+7(495)123-45-67',
                'contact_email': 'info@ceramat.ru'
            },
            {
                'name': 'АО "СтройСнаб"',
                'inn': '7702345678',
                'rating': 7,
                'start_date': date(2019, 6, 10),
                'contact_phone': '+7(495)234-56-78',
                'contact_email': 'orders@stroysnab.ru'
            },
            {
                'name': 'ИП Иванов А.С.',
                'inn': '772312345678',
                'rating': 6,
                'start_date': date(2021, 3, 20),
                'contact_phone': '+7(926)345-67-89',
                'contact_email': 'ivanov@colors.ru'
            },
            {
                'name': 'ООО "ПроИмпорт"',
                'inn': '7703456789',
                'rating': 9,
                'start_date': date(2018, 11, 5),
                'contact_phone': '+7(495)456-78-90',
                'contact_email': 'sales@proimport.ru'
            },
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
            suppliers.append(supplier)
        
        db.session.flush()  # Получаем ID поставщиков
        
        # Добавляем материалы
        materials_data = [
            {
                'name': 'Глина красная',
                'type_id': material_types[0].id,
                'description': 'Красная глина высокого качества для керамики',
                'unit_of_measure': 'кг',
                'quantity_in_package': 25,
                'quantity_in_stock': 150,
                'min_quantity': 200,
                'price_per_unit': 45.50
            },
            {
                'name': 'Песок кварцевый',
                'type_id': material_types[1].id,
                'description': 'Кварцевый песок мелкой фракции',
                'unit_of_measure': 'кг',
                'quantity_in_package': 50,
                'quantity_in_stock': 800,
                'min_quantity': 500,
                'price_per_unit': 12.30
            },
            {
                'name': 'Пигмент синий',
                'type_id': material_types[2].id,
                'description': 'Синий керамический пигмент',
                'unit_of_measure': 'кг',
                'quantity_in_package': 5,
                'quantity_in_stock': 15,
                'min_quantity': 25,
                'price_per_unit': 280.00
            },
            {
                'name': 'Глазурь прозрачная',
                'type_id': material_types[3].id,
                'description': 'Прозрачная глазурь для финишного покрытия',
                'unit_of_measure': 'л',
                'quantity_in_package': 10,
                'quantity_in_stock': 45,
                'min_quantity': 50,
                'price_per_unit': 125.00
            },
            {
                'name': 'Каолин белый',
                'type_id': material_types[4].id,
                'description': 'Белый каолин высшего сорта',
                'unit_of_measure': 'кг',
                'quantity_in_package': 20,
                'quantity_in_stock': 80,
                'min_quantity': 100,
                'price_per_unit': 95.75
            },
        ]
        
        materials = []
        for material_data in materials_data:
            material = Material(**material_data)
            db.session.add(material)
            materials.append(material)
        
        db.session.flush()  # Получаем ID материалов
        
        # Связываем материалы с поставщиками
        material_supplier_data = [
            # Глина красная - поставщики 0 и 1
            {'material_id': materials[0].id, 'supplier_id': suppliers[0].id, 'supply_price': 43.00, 'last_delivery_date': date(2024, 10, 15)},
            {'material_id': materials[0].id, 'supplier_id': suppliers[1].id, 'supply_price': 47.50, 'last_delivery_date': date(2024, 9, 20)},
            
            # Песок кварцевый - поставщики 1 и 3
            {'material_id': materials[1].id, 'supplier_id': suppliers[1].id, 'supply_price': 11.80, 'last_delivery_date': date(2024, 11, 1)},
            {'material_id': materials[1].id, 'supplier_id': suppliers[3].id, 'supply_price': 12.90, 'last_delivery_date': date(2024, 10, 25)},
            
            # Пигмент синий - поставщик 2
            {'material_id': materials[2].id, 'supplier_id': suppliers[2].id, 'supply_price': 275.00, 'last_delivery_date': date(2024, 8, 10)},
            
            # Глазурь прозрачная - поставщики 0 и 3
            {'material_id': materials[3].id, 'supplier_id': suppliers[0].id, 'supply_price': 120.00, 'last_delivery_date': date(2024, 10, 5)},
            {'material_id': materials[3].id, 'supplier_id': suppliers[3].id, 'supply_price': 130.00, 'last_delivery_date': date(2024, 9, 15)},
            
            # Каолин белый - поставщики 0 и 3
            {'material_id': materials[4].id, 'supplier_id': suppliers[0].id, 'supply_price': 92.50, 'last_delivery_date': date(2024, 11, 3)},
            {'material_id': materials[4].id, 'supplier_id': suppliers[3].id, 'supply_price': 98.00, 'last_delivery_date': date(2024, 10, 18)},
        ]
        
        for ms_data in material_supplier_data:
            material_supplier = MaterialSupplier(**ms_data)
            db.session.add(material_supplier)
        
        # Сохраняем все изменения
        db.session.commit()
        logging.info("Initial data imported successfully")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error importing initial data: {e}")
        raise e
