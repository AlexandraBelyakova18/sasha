from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError
from models import MaterialType

class MaterialForm(FlaskForm):
    """Форма для добавления/редактирования материала"""
    
    name = StringField('Наименование', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=1, max=200, message='Длина должна быть от 1 до 200 символов')
    ])
    
    type_id = SelectField('Тип материала', coerce=int, validators=[
        DataRequired(message='Выберите тип материала')
    ])
    
    description = TextAreaField('Описание')
    
    unit_of_measure = StringField('Единица измерения', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        Length(min=1, max=20, message='Длина должна быть от 1 до 20 символов')
    ])
    
    quantity_in_package = IntegerField('Количество в упаковке', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        NumberRange(min=1, message='Количество в упаковке должно быть больше 0')
    ])
    
    quantity_in_stock = IntegerField('Количество на складе', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        NumberRange(min=0, message='Количество на складе не может быть отрицательным')
    ])
    
    min_quantity = IntegerField('Минимальное количество', validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        NumberRange(min=0, message='Минимальное количество не может быть отрицательным')
    ])
    
    price_per_unit = DecimalField('Цена за единицу', places=2, validators=[
        DataRequired(message='Поле обязательно для заполнения'),
        NumberRange(min=0.01, message='Цена должна быть больше 0')
    ])
    
    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        # Заполняем choices для типов материалов
        self.type_id.choices = [
            (mt.id, mt.name) for mt in MaterialType.query.order_by(MaterialType.name).all()
        ]
        if not self.type_id.choices:
            self.type_id.choices = [(0, 'Нет доступных типов')]
    
    def validate_price_per_unit(self, field):
        """Валидация цены - не может быть отрицательной"""
        if field.data and field.data < 0:
            raise ValidationError('Цена не может быть отрицательной')
    
    def validate_min_quantity(self, field):
        """Валидация минимального количества - не может быть отрицательным"""
        if field.data and field.data < 0:
            raise ValidationError('Минимальное количество не может быть отрицательным')
