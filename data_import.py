import logging
import pandas as pd
import os
from app import db
from models import MaterialType, Supplier, Material, MaterialSupplier
from datetime import datetime, date

def import_initial_data():
    """Импорт данных из Excel файлов в базу данных"""
    
    # Проверяем, есть ли уже данные в базе
    if MaterialType.query.first() is not None:
        logging.info("Database already contains data, skipping import")
        return
    
    # Пытаемся импортировать данные из Excel файлов
    if import_data_from_excel():
        logging.info("Successfully imported data from Excel files")
        return
    
    # Если не удалось импортировать из Excel, используем тестовые данные
    logging.info("Importing fallback test data")
    import_test_data()

def import_data_from_excel():
    """Импорт данных из Excel файлов"""
    
    excel_files = {
        'material_types': 'attached_assets/Material_type_import_1749493566677.xlsx',
        'suppliers': 'attached_assets/Suppliers_import_1749493566679.xlsx', 
        'materials': 'attached_assets/Materials_import_1749493566678.xlsx',
        'material_suppliers': 'attached_assets/Material_suppliers_import_1749493566676.xlsx'
    }
    
    # Проверяем наличие файлов
    for file_path in excel_files.values():
        if not os.path.exists(file_path):
            logging.warning(f"Excel file not found: {file_path}")
            return False
    
    try:
        # 1. Импорт типов материалов
        df_types = pd.read_excel(excel_files['material_types'])
        material_types = []
        
        for _, row in df_types.iterrows():
            if pd.notna(row['Тип материала']):
                material_type = MaterialType(
                    name=str(row['Тип материала']).strip(),
                    description=f"Процент потери сырья: {row['Процент потери сырья  ']:.4f}" if pd.notna(row['Процент потери сырья  ']) else None
                )
                db.session.add(material_type)
                material_types.append(material_type)
        
        db.session.flush()
        logging.info(f"Imported {len(material_types)} material types")
        
        # 2. Импорт поставщиков
        df_suppliers = pd.read_excel(excel_files['suppliers'])
        suppliers = []
        
        for _, row in df_suppliers.iterrows():
            if pd.notna(row['Наименование поставщика']):
                start_date_val = row['Дата начала работы с поставщиком']
                if pd.notna(start_date_val):
                    if hasattr(start_date_val, 'date'):
                        start_date = start_date_val.date()
                    else:
                        start_date = pd.to_datetime(start_date_val).date()
                else:
                    start_date = date.today()
                
                supplier = Supplier(
                    name=str(row['Наименование поставщика']).strip(),
                    inn=str(row['ИНН']).strip() if pd.notna(row['ИНН']) else None,
                    rating=int(row['Рейтинг']) if pd.notna(row['Рейтинг']) else 5,
                    start_date=start_date
                )
                db.session.add(supplier)
                suppliers.append(supplier)
        
        db.session.flush()
        logging.info(f"Imported {len(suppliers)} suppliers")
        
        # 3. Импорт материалов
        df_materials = pd.read_excel(excel_files['materials'])
        materials = []
        
        for _, row in df_materials.iterrows():
            if pd.notna(row['Наименование материала']):
                # Найдем соответствующий тип материала
                material_type = None
                if pd.notna(row['Тип материала']):
                    type_name = str(row['Тип материала']).strip()
                    for mt in material_types:
                        if mt.name == type_name:
                            material_type = mt
                            break
                
                if not material_type and material_types:
                    material_type = material_types[0]  # Используем первый тип по умолчанию
                
                if material_type:
                    material = Material(
                        name=str(row['Наименование материала']).strip(),
                        type_id=material_type.id,
                        description=None,
                        unit_of_measure=str(row['Единица измерения']).strip() if pd.notna(row['Единица измерения']) else 'шт',
                        quantity_in_package=int(row['Количество в упаковке']) if pd.notna(row['Количество в упаковке']) else 1,
                        quantity_in_stock=int(row['Количество на складе']) if pd.notna(row['Количество на складе']) else 0,
                        min_quantity=int(row['Минимальное количество']) if pd.notna(row['Минимальное количество']) else 0,
                        price_per_unit=float(row['Цена единицы материала']) if pd.notna(row['Цена единицы материала']) else 0.01
                    )
                    db.session.add(material)
                    materials.append(material)
        
        db.session.flush()
        logging.info(f"Imported {len(materials)} materials")
        
        # 4. Импорт связей материалов и поставщиков
        df_ms = pd.read_excel(excel_files['material_suppliers'])
        material_suppliers_count = 0
        
        for _, row in df_ms.iterrows():
            if pd.notna(row['Наименование материала']) and pd.notna(row['Наименование поставщика']):
                material_name = str(row['Наименование материала']).strip()
                supplier_name = str(row['Наименование поставщика']).strip()
                
                # Найдем материал и поставщика
                material = None
                supplier = None
                
                for m in materials:
                    if m.name == material_name:
                        material = m
                        break
                
                for s in suppliers:
                    if s.name == supplier_name:
                        supplier = s
                        break
                
                if material and supplier:
                    last_delivery_date = None
                    if pd.notna(row.get('Дата последней поставки')):
                        delivery_date_val = row['Дата последней поставки']
                        if hasattr(delivery_date_val, 'date'):
                            last_delivery_date = delivery_date_val.date()
                        else:
                            last_delivery_date = pd.to_datetime(delivery_date_val).date()
                    
                    material_supplier = MaterialSupplier(
                        material_id=material.id,
                        supplier_id=supplier.id,
                        supply_price=float(row['Цена поставки']) if pd.notna(row.get('Цена поставки')) else None,
                        last_delivery_date=last_delivery_date
                    )
                    db.session.add(material_supplier)
                    material_suppliers_count += 1
        
        db.session.commit()
        logging.info(f"Imported {material_suppliers_count} material-supplier relationships")
        return True
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error importing Excel data: {e}")
        return False

def import_test_data():
    """Импорт тестовых данных как резервный вариант"""
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
        
        db.session.flush()
        
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
        ]
        
        suppliers = []
        for supplier_data in suppliers_data:
            supplier = Supplier(**supplier_data)
            db.session.add(supplier)
            suppliers.append(supplier)
        
        db.session.flush()
        
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
        ]
        
        materials = []
        for material_data in materials_data:
            material = Material(**material_data)
            db.session.add(material)
            materials.append(material)
        
        db.session.flush()
        
        # Связываем материалы с поставщиками
        material_supplier_data = [
            {'material_id': materials[0].id, 'supplier_id': suppliers[0].id, 'supply_price': 43.00, 'last_delivery_date': date(2024, 10, 15)},
            {'material_id': materials[1].id, 'supplier_id': suppliers[1].id, 'supply_price': 11.80, 'last_delivery_date': date(2024, 11, 1)},
        ]
        
        for ms_data in material_supplier_data:
            material_supplier = MaterialSupplier(**ms_data)
            db.session.add(material_supplier)
        
        db.session.commit()
        logging.info("Test data imported successfully")
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error importing test data: {e}")
        raise e
