from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]