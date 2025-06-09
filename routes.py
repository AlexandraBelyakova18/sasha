from flask import render_template, request, redirect, url_for, flash, abort
from app import app, db
from models import Material, MaterialType, Supplier, MaterialSupplier
from forms import MaterialForm
import logging

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/materials')
def materials():
    """Список материалов"""
    try:
        materials_list = Material.query.join(MaterialType).all()
        
        # Добавляем информацию о стоимости минимальной партии для каждого материала
        materials_with_costs = []
        for material in materials_list:
            material_data = {
                'material': material,
                'shortage_info': material.get_shortage_info()
            }
            materials_with_costs.append(material_data)
        
        return render_template('materials.html', materials=materials_with_costs)
    except Exception as e:
        logging.error(f"Error loading materials: {e}")
        flash('Ошибка при загрузке списка материалов', 'error')
        return render_template('error.html', error="Не удалось загрузить список материалов")

@app.route('/material/add', methods=['GET', 'POST'])
def add_material():
    """Добавление нового материала"""
    form = MaterialForm()
    
    if form.validate_on_submit():
        try:
            material = Material(
                name=form.name.data,
                type_id=form.type_id.data,
                description=form.description.data,
                unit_of_measure=form.unit_of_measure.data,
                quantity_in_package=form.quantity_in_package.data,
                quantity_in_stock=form.quantity_in_stock.data,
                min_quantity=form.min_quantity.data,
                price_per_unit=form.price_per_unit.data
            )
            
            db.session.add(material)
            db.session.commit()
            
            flash('Материал успешно добавлен', 'success')
            return redirect(url_for('materials'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding material: {e}")
            flash('Ошибка при добавлении материала', 'error')
    
    return render_template('material_form.html', form=form, title='Добавление материала')

@app.route('/material/edit/<int:id>', methods=['GET', 'POST'])
def edit_material(id):
    """Редактирование материала"""
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    
    if form.validate_on_submit():
        try:
            material.name = form.name.data
            material.type_id = form.type_id.data
            material.description = form.description.data
            material.unit_of_measure = form.unit_of_measure.data
            material.quantity_in_package = form.quantity_in_package.data
            material.quantity_in_stock = form.quantity_in_stock.data
            material.min_quantity = form.min_quantity.data
            material.price_per_unit = form.price_per_unit.data
            
            db.session.commit()
            
            flash('Материал успешно обновлен', 'success')
            return redirect(url_for('materials'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating material: {e}")
            flash('Ошибка при обновлении материала', 'error')
    
    return render_template('material_form.html', form=form, title='Редактирование материала', material=material)

@app.route('/material/<int:id>/suppliers')
def material_suppliers(id):
    """Список поставщиков для конкретного материала"""
    try:
        material = Material.query.get_or_404(id)
        
        # Получаем всех поставщиков для данного материала
        suppliers_query = db.session.query(Supplier, MaterialSupplier).join(
            MaterialSupplier, Supplier.id == MaterialSupplier.supplier_id
        ).filter(MaterialSupplier.material_id == id).all()
        
        suppliers_data = []
        for supplier, material_supplier in suppliers_query:
            suppliers_data.append({
                'supplier': supplier,
                'material_supplier': material_supplier
            })
        
        return render_template('suppliers.html', 
                             material=material, 
                             suppliers=suppliers_data)
    except Exception as e:
        logging.error(f"Error loading suppliers for material {id}: {e}")
        flash('Ошибка при загрузке списка поставщиков', 'error')
        return render_template('error.html', error="Не удалось загрузить список поставщиков")

@app.route('/suppliers')
def all_suppliers():
    """Список всех поставщиков"""
    try:
        suppliers = Supplier.query.all()
        return render_template('suppliers.html', suppliers=suppliers, show_all=True)
    except Exception as e:
        logging.error(f"Error loading all suppliers: {e}")
        flash('Ошибка при загрузке списка поставщиков', 'error')
        return render_template('error.html', error="Не удалось загрузить список поставщиков")

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error="Страница не найдена"), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error="Внутренняя ошибка сервера"), 500
