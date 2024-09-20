from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char('Title',required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From',copy=False,default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(
      string='Garden Orientation',
      selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
      ],
      help="The orientation of the garden"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        help="The status of the property"
    )
    total_area = fields.Integer(string='Total Area (sqm)', compute='_compute_total_area')
    best_price = fields.Float(compute="_compute_best_price")
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    _sql_constraints = [
        ('check_property_expected_price', 'CHECK(expected_price > 0)',
         'The expected price must be strictly positive.'),
        ('check_property_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be strictly positive.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0:
                    raise UserError("The selling price must be at least 90% of the expected price.")

    def action_set_property_as_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("You cannot set a canceled property as sold.")
            else:
                record.state = 'sold'
        return True

    def action_set_property_as_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("You cannot set a sold property as canceled.")
            else:
                record.state = 'canceled'
        return True
