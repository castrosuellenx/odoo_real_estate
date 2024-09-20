from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_unique_tag_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]
