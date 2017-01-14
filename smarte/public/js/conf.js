// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide('erpnext');

// add toolbar icon
$(document).bind('toolbar_setup', function() {
	frappe.app.name = "Smarte";

	frappe.help_feedback_link = '<p><a class="text-muted" \
		href="https://smartehis.com#contact">Feedback</a></p>'

	$('.navbar-home').html('<img class="erpnext-icon" src="'+
			frappe.urllib.get_base_url()+'/assets/smarte/images/smarte.png" />');
});

// preferred modules for breadcrumbs
$.extend(frappe.breadcrumbs.preferred, {
	"Customer": "OP"
});
