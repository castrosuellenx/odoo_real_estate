{
  'name': 'Real Estate',
  'application': True,
  'license': 'LGPL-3',
  'data': [
    'security/ir.model.access.csv',

    'views/estate_menus.xml',
    'views/estate_property_views.xml'
  ],

  'assets': {
    'web.assets_backend': [
      'estate/static/src/css/estate_styles.css',
    ],
  },
}