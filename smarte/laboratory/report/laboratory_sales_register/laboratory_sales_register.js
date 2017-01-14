// Copyright (c) 2016, ESS LLP
// License: See license.txt

frappe.query_reports["Laboratory Sales Register"] = {
	"refresh":frappe.breadcrumbs.add("Laboratory"),
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
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		}
	]
}
