# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "Laboratory",
			"color": "#FF888B",
			"icon": "octicon octicon octicon-beaker",
			"type": "module",
			"label": _("Laboratory")
		},
		{
			"module_name": "OP",
			"color": "#FF888B",
			"icon": "octicon octicon octicon-plus",
			"type": "module",
			"label": _("OP")
		},
		{
			"module_name": "IP",
			"color": "#FF888B",
			"icon": "octicon octicon octicon-pulse",
			"type": "module",
			"label": _("IP")
		},
		{
			"module_name": "Pharmacy",
			"color": "#FF888B",
			"icon": "octicon octicon octicon-server",
			"type": "module",
			"label": _("Pharmacy")
		}
	]
