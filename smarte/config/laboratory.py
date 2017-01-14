from __future__ import unicode_literals
from frappe import _

def get_data():

	return [
		{
			"label": _("Documents"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Customer",
					"label": _("Patient"),
					"description": _("Patient."),
				},
				{
					"type": "doctype",
					"name": "Physician",
					"description": _("Physician."),
				},
				{
					"type": "doctype",
					"name": "Lab Procedure",
					"description": _("Results"),
					"icon": "octicon octicon-clippy",
				},
				{
					"type": "doctype",
					"name": "Sample Collection",
					"description": _("Sample Collection."),
				},
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Invoice."),
				},

			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Laboratory Settings",
					"description": _("Settings for Laboratory Module")
				},
				{
					"type": "doctype",
					"name": "Lab Test Type",
					"description": _("Lab Test Type")
				},
				{
					"type": "doctype",
					"name": "Lab Test Template",
					"description": _("Lab Test Configurations.")
				},
				{
					"type": "doctype",
					"name": "Lab Test Samples",
					"description": _("Test Sample Master."),
				},
				{
					"type": "doctype",
					"name": "Lab Test UOM",
					"description": _("UOM Refer to Laboratory.")
				},
				{
					"type": "doctype",
					"name": "Antibiotics",
					"description": _("Antibiotics.")
				},
				{
					"type": "doctype",
					"name": "Sensitivity",
					"description": _("Sensitivity Naming.")
				},

			]
		},
		{
			"label": _("Standard Reports"),
			"icon": "icon-list",
			"items": [
				{
					"type": "doctype",
					"name": "Invoice Test Report",
					"description": _("Invoiced Results."),
					"icon": "octicon octicon-tasklist",
				},
				{
					"type": "report",
					"name": "Lab Procedure Report",
					"is_query_report": True,
					"doctype": "Lab Procedure"
				},
				{
					"type": "report",
					"name": "Laboratory Sales Register",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				}
			]
		},

	]
