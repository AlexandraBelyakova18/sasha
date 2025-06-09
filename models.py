from app import db
from sqlalchemy import func
from datetime import datetime

class MaterialType(db.Model):
    """Типы материалов"""
    __tablename__ = 'material_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    
    # Relationship to materials
    materials = db.relationship('Material', backref='material_type', lazy=True)
    
    def __repr__(self):
        return f'<MaterialType {self.name}>'

class Supplier(db.Model):
    """Поставщики"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    inn = db.Column(db.String(20))
    rating = db.Column(db.Integer, default=5)  # Рейтинг от 1 до 10
    start_date = db.Column(db.Date, default=datetime.utcnow)  # Дата начала работы
    contact_phone = db.Column(db.String(20))
    contact_email = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Supplier {self.name}>'

class Material(db.Model):
    """Материалы (сырье)"""
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('material_types.id'), nullable=False)
    description = db.Column(db.Text)
    unit_of_measure = db.Column(db.String(20), nullable=False)  # единица измерения
    quantity_in_package = db.Column(db.Integer, nullable=False, default=1)  # количество в упаковке
    quantity_in_stock = db.Column(db.Integer, nullable=False, default=0)  # количество на складе
    min_quantity = db.Column(db.Integer, nullable=False, default=0)  # минимальное количество
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False)  # цена за единицу
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Material {self.name}>'
    
    def calculate_min_purchase_cost(self):
        """Расчет стоимости минимально необходимой партии материала"""
        if self.quantity_in_stock >= self.min_quantity:
            return 0.0
        
        # Разность между минимальным количеством и текущим остатком
        shortage = self.min_quantity - self.quantity_in_stock
        
        # Количество упаковок, кратное quantity_in_package
        packages_needed = (shortage + self.quantity_in_package - 1) // self.quantity_in_package
        
        # Общее количество единиц для покупки
        total_units_to_buy = packages_needed * self.quantity_in_package
        
        # Стоимость покупки
        cost = float(total_units_to_buy * self.price_per_unit)
        
        return round(cost, 2)
    
    def get_shortage_info(self):
        """Получить информацию о нехватке материала"""
        if self.quantity_in_stock >= self.min_quantity:
            return {
                'has_shortage': False,
                'shortage_amount': 0,
                'packages_needed': 0,
                'total_units_to_buy': 0,
                'min_purchase_cost': 0.0
            }
        
        shortage = self.min_quantity - self.quantity_in_stock
        packages_needed = (shortage + self.quantity_in_package - 1) // self.quantity_in_package
        total_units_to_buy = packages_needed * self.quantity_in_package
        cost = self.calculate_min_purchase_cost()
        
        return {
            'has_shortage': True,
            'shortage_amount': shortage,
            'packages_needed': packages_needed,
            'total_units_to_buy': total_units_to_buy,
            'min_purchase_cost': cost
        }

class MaterialSupplier(db.Model):
    """Связь материалов и поставщиков"""
    __tablename__ = 'material_suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    supply_price = db.Column(db.Numeric(10, 2))  # цена поставки от конкретного поставщика
    last_delivery_date = db.Column(db.Date)  # дата последней поставки
    
    # Relationships
    material = db.relationship('Material', backref='material_suppliers')
    supplier = db.relationship('Supplier', backref='supplied_materials')
    
    def __repr__(self):
        return f'<MaterialSupplier Material:{self.material_id} Supplier:{self.supplier_id}>'
