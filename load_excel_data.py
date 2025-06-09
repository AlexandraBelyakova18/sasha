import pandas as pd
import logging
from app import app, db
from models import MaterialType, Supplier, Material, MaterialSupplier
from datetime import datetime, date

def load_excel_data():
    """Загрузка данных из Excel файлов"""
    
    with app.app_context():
        # Очищаем базу данных
        MaterialSupplier.query.delete()
        Material.query.delete()
        Supplier.query.delete()
        MaterialType.query.delete()
        db.session.commit()
        
        # 1. Загружаем типы материалов
        df_types = pd.read_excel('attached_assets/Material_type_import_1749493566677.xlsx')
        print("Material Types:", df_types.columns.tolist())
        
        for _, row in df_types.iterrows():
            material_type = MaterialType(
                name=row['Тип материала'],
                description=f"Процент потери сырья: {row['Процент потери сырья  ']:.4f}"
            )
            db.session.add(material_type)
        
        db.session.commit()
        print(f"Загружено {MaterialType.query.count()} типов материалов")
        
        # 2. Загружаем поставщиков
        df_suppliers = pd.read_excel('attached_assets/Suppliers_import_1749493566679.xlsx')
        print("Suppliers:", df_suppliers.columns.tolist())
        
        for _, row in df_suppliers.iterrows():
            start_date = row['Дата начала работы с поставщиком']
            if pd.isna(start_date):
                start_date = date.today()
            elif hasattr(start_date, 'date'):
                start_date = start_date.date()
            else:
                start_date = pd.to_datetime(start_date).date()
            
            supplier = Supplier(
                name=row['Наименование поставщика'],
                inn=str(row['ИНН']) if not pd.isna(row['ИНН']) else None,
                rating=int(row['Рейтинг']) if not pd.isna(row['Рейтинг']) else 5,
                start_date=start_date
            )
            db.session.add(supplier)
        
        db.session.commit()
        print(f"Загружено {Supplier.query.count()} поставщиков")
        
        # 3. Загружаем материалы
        df_materials = pd.read_excel('attached_assets/Materials_import_1749493566678.xlsx')
        print("Materials:", df_materials.columns.tolist())
        
        for _, row in df_materials.iterrows():
            # Находим тип материала
            type_name = row['Тип материала']
            material_type = MaterialType.query.filter_by(name=type_name).first()
            if not material_type:
                material_type = MaterialType.query.first()  # Берем первый доступный
            
            if material_type:
                material = Material(
                    name=row['Наименование материала'],
                    type_id=material_type.id,
                    description=None,
                    unit_of_measure=row['Единица измерения'],
                    quantity_in_package=int(row['Количество в упаковке']),
                    quantity_in_stock=int(row['Количество на складе']),
                    min_quantity=int(row['Минимальное количество']),
                    price_per_unit=float(row['Цена единицы материала'])
                )
                db.session.add(material)
        
        db.session.commit()
        print(f"Загружено {Material.query.count()} материалов")
        
        # 4. Загружаем связи материалов и поставщиков
        df_ms = pd.read_excel('attached_assets/Material_suppliers_import_1749493566676.xlsx')
        print("Material Suppliers:", df_ms.columns.tolist())
        print("Sample data:")
        print(df_ms.head())
        
        # Проверим какие колонки есть в файле
        for col in df_ms.columns:
            print(f"Column: '{col}'")
        
        # Попробуем найти правильные названия колонок
        material_col = None
        supplier_col = None
        
        for col in df_ms.columns:
            if 'материал' in col.lower():
                material_col = col
            elif 'поставщик' in col.lower():
                supplier_col = col
        
        print(f"Material column: {material_col}")
        print(f"Supplier column: {supplier_col}")
        
        if material_col and supplier_col:
            for _, row in df_ms.iterrows():
                material_name = row[material_col]
                supplier_name = row[supplier_col]
                
                material = Material.query.filter_by(name=material_name).first()
                supplier = Supplier.query.filter_by(name=supplier_name).first()
                
                if material and supplier:
                    material_supplier = MaterialSupplier(
                        material_id=material.id,
                        supplier_id=supplier.id,
                        supply_price=None,
                        last_delivery_date=None
                    )
                    db.session.add(material_supplier)
        
        db.session.commit()
        print(f"Загружено {MaterialSupplier.query.count()} связей материал-поставщик")
        
        print("Загрузка данных завершена успешно!")

if __name__ == "__main__":
    load_excel_data()