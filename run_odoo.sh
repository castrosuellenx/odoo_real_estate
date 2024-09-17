#!/bin/bash

MY_ODOO_ADDONS="$(pwd)"
/usr/bin/odoo --addons-path="/usr/lib/python3/dist-packages/odoo/addons,$MY_ODOO_ADDONS" -d rd-demo -u estate --http-port=8070 --dev=all
