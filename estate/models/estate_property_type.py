from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order property types. Lower means more used.')
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]