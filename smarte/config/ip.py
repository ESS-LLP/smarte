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
					"name": "InPatients",
					"label": _("InPatients"),
					"description": _("Inpatient Registration"),
				},
				{
					"type": "doctype",
					"name": "Consultation",
					"description": _("Consultation."),
				},
				{
					"type": "doctype",
					"name": "Customer",
					"label": _("Patients"),
					"description": _("Patients"),
				},
				{
					"type": "doctype",
					"name": "Physician",
					"description": _("Physician."),
				},
			]
		},
		{
			"label": _("Tasks"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Service Task",
					"label": _("Service Task"),
				}
			]
		},
		{
			"label": _("Infrastructure"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Floor",
					"label": _("Floor"),
					"description": _("Inpatient Registration"),
				},
				{
					"type": "doctype",
					"name": "Zone",
					"label": _("Zone"),

				},
				{
					"type": "doctype",
					"name": "Facility",
					"label": _("Facility"),

				},
				{
					"type": "doctype",
					"name": "Facility Type",
					"label": _("Facility Type"),

				},
				{
					"type": "doctype",
					"name": "Service Unit",
					"label": _("Service Unit"),

				},
				{
					"type": "doctype",
					"name": "Unit Type",
					"label": _("Service Unit Type"),

				}
			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "IP Settings",
					"description": _("Settings for IP Module")
				},
				{
					"type": "doctype",
					"name": "Routine Observations",
					"label": _("Routine Observations"),
				},
				{
					"type": "doctype",
					"name": "Duration",
					"description": _("Setting Drug Prescription Period")
				},
				{
					"type": "doctype",
					"name": "Dosage",
					"description": _("Setting Drug Prescription Dosage")
				},
				{
					"type": "doctype",
					"name": "PACS Settings",
					"description": _("Server Settings")
				},
			]
		}
	]
