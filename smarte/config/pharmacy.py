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
					"description": _("Patient Registration"),
				},
				{
					"type": "doctype",
					"name": "Physician",
					"description": _("Physician."),
				},
				{
					"type": "doctype",
					"name": "Consultation",
					"description": _("Patient Doctor Consulation"),
				},

			]
		},
		{
			"label": _("Transactions"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Sales Invoice",
					"description": _("Invoice."),
				},
				{
					"type": "doctype",
					"name": "Purchase Order",
					"description": _("Purchase Orders given to Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Purchase Invoice",
					"description": _("Purchase Invoice"),
				},
				{
					"type": "doctype",
					"name": "Purchase Receipt",
					"description": _("Goods received from Suppliers."),
				},
				{
					"type": "doctype",
					"name": "Material Request",
					"description": _("Requests for items."),
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"name": "Pharmacy Sales Register",
					"is_query_report": True,
					"doctype": "Sales Invoice"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ledger",
					"doctype": "Stock Ledger Entry",
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Balance",
					"doctype": "Stock Ledger Entry"
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Projected Qty",
					"doctype": "Item",
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Stock Ageing",
					"doctype": "Item",
				},
				{
					"type": "page",
					"name": "stock-analytics",
					"label": _("Stock Analytics"),
					"icon": "icon-bar-chart"
				},
			]
		},
		{
			"label": _("Items and Pricing"),
			"items": [
				{
					"type": "doctype",
					"name": "Item",
					"description": _("All Products or Services."),
				},
				{
					"type": "doctype",
					"name": "Price List",
					"description": _("Price List master.")
				},
				{
					"type": "page",
					"name": "Sales Browser",
					"icon": "icon-sitemap",
					"label": _("Item Group"),
					"link": "Sales Browser/Item Group",
					"description": _("Tree of Item Groups."),
					"doctype": "Item Group",
				},
				{
					"type": "doctype",
					"name": "Item Price",
					"description": _("Multiple Item prices."),
					"route": "Report/Item Price"
				},
				{
					"type": "doctype",
					"name": "Pricing Rule",
					"description": _("Rules for applying pricing and discount.")
				},

			]
		},
		{
			"label": _("Serial No and Batch"),
			"items": [
				{
					"type": "doctype",
					"name": "Serial No",
					"description": _("Single unit of an Item."),
				},
				{
					"type": "doctype",
					"name": "Batch",
					"description": _("Batch (lot) of an Item."),
				}
			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Stock Settings",
					"description": _("Default settings for stock transactions.")
				},
				{
					"type": "doctype",
					"name": "Warehouse",
					"description": _("Where items are stored."),
				},
				{
					"type": "doctype",
					"name": "UOM",
					"label": _("Unit of Measure") + " (UOM)",
					"description": _("e.g. Kg, Unit, Nos, m")
				},
				{
					"type": "doctype",
					"name": "Brand",
					"description": _("Brand master.")
				},
			]
		},
	]
