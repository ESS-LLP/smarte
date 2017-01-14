from __future__ import unicode_literals
from frappe import _
import frappe
import datetime as dt
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
					"description": _("Patient Registration"),
				},
				{
					"type": "doctype",
					"name": "Physician",
					"description": _("Physician."),
				},
				{
					"type": "doctype",
					"name": "Appointment",
					"description": _("Patient Appointment"),
				},
				{
					"type": "doctype",
					"name": "Consultation",
					"description": _("Patient Doctor Consulation"),
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
					"name": "OP Settings",
					"label": _("OP Settings"),
				},
				{
					"type": "doctype",
					"name": "Referring Physician",
					"description": _("Referring Physician."),
				},
				{
					"type": "doctype",
					"name": "Appointment Type",
					"description": _("Appointment Type Master"),
				},
				{
					"type": "doctype",
					"name": "Duration",
					"description": _("Drug Prescription Period")
				},
				{
					"type": "doctype",
					"name": "Dosage",
					"description": _("Drug Prescription Dosage")
				},
			]
		},
		{
			"label": _("Standard Reports"),
			"icon": "icon-list",
			"items": [
				{
					"type": "doctype",
					"name": "Appointment",
					"description": _("Patient Appointment"),
					"label": _("Today's Appoinment"),
					"route_options": {"appointment_date": dt.date.today()}
				},
				{
					"type": "page",
					"name": "medical_record",
					"label": _("Patient Medical Records"),
					"icon": "icon-bar-chart",
				},
				{
					"type": "page",
					"name": "appointment-analytic",
					"label": _("Appointment Analytics"),
					"icon": "icon-bar-chart",
				},
				{
					"type": "page",
					"name": "patient-registration",
					"label": _("Patient Registration Analytics"),
					"icon": "icon-bar-chart",
				},

			]
		},

	]
