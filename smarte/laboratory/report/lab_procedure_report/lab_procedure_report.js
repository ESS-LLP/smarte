// Copyright (c) 2016, ESS
// License: See license.txt

frappe.query_reports["Lab Procedure Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": get_today(),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": get_today()
		},
		{
			"fieldname":"customer",
			"label": __("Patient"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname":"lab_test_type",
			"label": __("Lab Test Type"),
			"fieldtype": "Link",
			"options": "Lab Test Type"
		}
	]
}
