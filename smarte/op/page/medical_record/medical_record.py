# Copyright (c) 2015, ESS
# License: See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint

@frappe.whitelist()
def get_feed(limit_start, limit_page_length, name):
	"""get feed"""
	result = frappe.db.sql("""select name, owner, modified, creation,
			reference_doctype, reference_name, subject 
		from `tabPatient Medical Record`
		where patient=%(customer)s
		order by creation desc
		limit %(limit_start)s, %(limit_page_length)s""",
		{
			"limit_start": cint(limit_start),
			"limit_page_length": cint(limit_page_length),
			"customer": name
		}, as_dict=True)

	return result
