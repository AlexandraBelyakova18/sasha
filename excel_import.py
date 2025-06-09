import pandas as pd
import logging
from app import db
from models import MaterialType, Supplier, Material, MaterialSupplier
from datetime import datetime, date
import os

def read_excel_files():
    """Чтение всех Excel файлов и вывод их содержимого"""
    
    excel_files = {
        'material_types': 'attached_assets/Material_type_import_1749493566677.xlsx',
        'suppliers': 'attached_assets/Suppliers_import_1749493566679.xlsx', 
        'materials': 'attached_assets/Materials_import_1749493566678.xlsx',
        'material_suppliers': 'attached_assets/Material_suppliers_import_1749493566676.xlsx',
        'product_types': 'attached_assets/Product_type_import_1749493566678.xlsx'
    }
    
    data = {}
    
    for key, file_path in excel_files.items():
        if os.path.exists(file_path):
            try:
                df = pd.read_excel(file_path)
                data[key] = df
                print(f"\n=== {key.upper()} ({file_path}) ===")
                print(f"Columns: {list(df.columns)}")
                print(f"Shape: {df.shape}")
                print("Data:")
                print(df.to_string())
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        else:
            print(f"File not found: {file_path}")
    
    return data

def import_data_from_excel():
    """Импорт данных из Excel файлов в базу данных"""
    
    # Очищаем существующие данные
    MaterialSupplier.query.delete()
    Material.query.delete()
    Supplier.query.delete()
    MaterialType.query.delete()
    db.session.commit()
    
    excel_files = {
        'material_types': 'attached_assets/Material_type_import_1749493566677.xlsx',
        'suppliers': 'attached_assets/Suppliers_import_1749493566679.xlsx', 
        'materials': 'attached_assets/Materials_import_1749493566678.xlsx',
        'material_suppliers': 'attached_assets/Material_suppliers_import_1749493566676.xlsx'
    }
    
    try:
        # 1. Импорт типов материалов
        if os.path.exists(excel_files['material_types']):
            df_types = pd.read_excel(excel_files['material_types'])
            print("Material Types columns:", list(df_types.columns))
            print("Material Types data:")
            print(df_types.head())
            
            for _, row in df_types.iterrows():
                # Попробуем различные варианты названий колонок
                name = None
                description = None
                
                for col in df_types.columns:
                    col_lower = col.lower()
                    if any(keyword in col_lower for keyword in ['name', 'наименование', 'название', 'тип']):
                        if pd.notna(row[col]):
                            name = str(row[col]).strip()
                    elif any(keyword in col_lower for keyword in ['description', 'описание', 'desc']):
                        if pd.notna(row[col]):
                            description = str(row[col]).strip()
                
                if name:
                    material_type = MaterialType(
                        name=name,
                        description=description
                    )
                    db.session.add(material_type)
            
            db.session.commit()
            print(f"Imported {MaterialType.query.count()} material types")
        
        # 2. Импорт поставщиков
        if os.path.exists(excel_files['suppliers']):
            df_suppliers = pd.read_excel(excel_files['suppliers'])
            print("Suppliers columns:", list(df_suppliers.columns))
            print("Suppliers data:")
            print(df_suppliers.head())
            
            for _, row in df_suppliers.iterrows():
                # Парсим данные поставщика
                name = None
                inn = None
                rating = 5
                start_date = None
                contact_phone = None
                contact_email = None
                
                for col in df_suppliers.columns:
                    col_lower = col.lower()
                    if pd.notna(row[col]):
                        value = str(row[col]).strip()
                        
                        if any(keyword in col_lower for keyword in ['name', 'наименование', 'название', 'компания']):
                            name = value
                        elif any(keyword in col_lower for keyword in ['inn', 'инн']):
                            inn = value
                        elif any(keyword in col_lower for keyword in ['rating', 'рейтинг']):
                            try:
                                rating = int(float(value))
                            except:
                                rating = 5
                        elif any(keyword in col_lower for keyword in ['phone', 'телефон', 'тел']):
                            contact_phone = value
                        elif any(keyword in col_lower for keyword in ['email', 'почта', 'e-mail']):
                            contact_email = value
                        elif any(keyword in col_lower for keyword in ['date', 'дата', 'начало']):
                            try:
                                if isinstance(row[col], datetime):
                                    start_date = row[col].date()
                                elif isinstance(row[col], date):
                                    start_date = row[col]
                                else:
                                    # Попробуем парсить строку
                                    start_date = pd.to_datetime(value).date()
                            except:
                                start_date = date.today()
                
                if name:
                    supplier = Supplier(
                        name=name,
                        inn=inn,
                        rating=rating,
                        start_date=start_date or date.today(),
                        contact_phone=contact_phone,
                        contact_email=contact_email
                    )
                    db.session.add(supplier)
            
            db.session.commit()
            print(f"Imported {Supplier.query.count()} suppliers")
        
        # 3. Импорт материалов
        if os.path.exists(excel_files['materials']):
            df_materials = pd.read_excel(excel_files['materials'])
            print("Materials columns:", list(df_materials.columns))
            print("Materials data:")
            print(df_materials.head())
            
            for _, row in df_materials.iterrows():
                # Парсим данные материала
                name = None
                type_name = None
                description = None
                unit_of_measure = 'шт'
                quantity_in_package = 1
                quantity_in_stock = 0
                min_quantity = 0
                price_per_unit = 0.0
                
                for col in df_materials.columns:
                    col_lower = col.lower()
                    if pd.notna(row[col]):
                        value = str(row[col]).strip()
                        
                        if any(keyword in col_lower for keyword in ['name', 'наименование', 'название', 'материал']):
                            name = value
                        elif any(keyword in col_lower for keyword in ['type', 'тип']):
                            type_name = value
                        elif any(keyword in col_lower for keyword in ['description', 'описание']):
                            description = value
                        elif any(keyword in col_lower for keyword in ['unit', 'единица', 'измерение']):
                            unit_of_measure = value
                        elif any(keyword in col_lower for keyword in ['package', 'упаковка', 'упак']):
                            try:
                                quantity_in_package = int(float(value))
                            except:
                                quantity_in_package = 1
                        elif any(keyword in col_lower for keyword in ['stock', 'склад', 'остаток']):
                            try:
                                quantity_in_stock = int(float(value))
                            except:
                                quantity_in_stock = 0
                        elif any(keyword in col_lower for keyword in ['min', 'минимум', 'минимальн']):
                            try:
                                min_quantity = int(float(value))
                            except:
                                min_quantity = 0
                        elif any(keyword in col_lower for keyword in ['price', 'цена', 'стоимость']):
                            try:
                                price_per_unit = float(value)
                            except:
                                price_per_unit = 0.0
                
                if name:
                    # Найдем тип материала
                    material_type = None
                    if type_name:
                        material_type = MaterialType.query.filter_by(name=type_name).first()
                    
                    if not material_type:
                        material_type = MaterialType.query.first()
                    
                    if material_type:
                        material = Material(
                            name=name,
                            type_id=material_type.id,
                            description=description,
                            unit_of_measure=unit_of_measure,
                            quantity_in_package=max(1, quantity_in_package),
                            quantity_in_stock=max(0, quantity_in_stock),
                            min_quantity=max(0, min_quantity),
                            price_per_unit=max(0.01, price_per_unit)
                        )
                        db.session.add(material)
            
            db.session.commit()
            print(f"Imported {Material.query.count()} materials")
        
        # 4. Импорт связей материалов и поставщиков
        if os.path.exists(excel_files['material_suppliers']):
            df_ms = pd.read_excel(excel_files['material_suppliers'])
            print("Material Suppliers columns:", list(df_ms.columns))
            print("Material Suppliers data:")
            print(df_ms.head())
            
            for _, row in df_ms.iterrows():
                material_name = None
                supplier_name = None
                supply_price = None
                last_delivery_date = None
                
                for col in df_ms.columns:
                    col_lower = col.lower()
                    if pd.notna(row[col]):
                        value = str(row[col]).strip()
                        
                        if any(keyword in col_lower for keyword in ['material', 'материал']):
                            material_name = value
                        elif any(keyword in col_lower for keyword in ['supplier', 'поставщик']):
                            supplier_name = value
                        elif any(keyword in col_lower for keyword in ['price', 'цена', 'стоимость']):
                            try:
                                supply_price = float(value)
                            except:
                                supply_price = None
                        elif any(keyword in col_lower for keyword in ['date', 'дата', 'поставка']):
                            try:
                                if isinstance(row[col], datetime):
                                    last_delivery_date = row[col].date()
                                elif isinstance(row[col], date):
                                    last_delivery_date = row[col]
                                else:
                                    last_delivery_date = pd.to_datetime(value).date()
                            except:
                                last_delivery_date = None
                
                if material_name and supplier_name:
                    material = Material.query.filter(Material.name.ilike(f'%{material_name}%')).first()
                    supplier = Supplier.query.filter(Supplier.name.ilike(f'%{supplier_name}%')).first()
                    
                    if material and supplier:
                        material_supplier = MaterialSupplier(
                            material_id=material.id,
                            supplier_id=supplier.id,
                            supply_price=supply_price,
                            last_delivery_date=last_delivery_date
                        )
                        db.session.add(material_supplier)
            
            db.session.commit()
            print(f"Imported {MaterialSupplier.query.count()} material-supplier relationships")
        
        logging.info("Successfully imported data from Excel files")
        return True
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error importing Excel data: {e}")
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Reading Excel files...")
    data = read_excel_files()