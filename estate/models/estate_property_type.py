from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = 'Real Estate Property Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help='Used to order property types. Lower means more used.')
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count', string="Offers")

    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        for property_type in self:
            property_type.offer_count = len(property_type.property_ids.offer_ids)

    def action_view_offers(self):
        self.ensure_one()
        return {
            'name': 'Property Offers',
            'view_mode': 'tree,form',
            'res_model': 'estate.property.offer',
            'type': 'ir.actions.act_window',
            'domain': [('property_id.property_type_id', '=', self.id)],
        }