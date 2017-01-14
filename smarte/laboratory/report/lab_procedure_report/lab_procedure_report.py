# Copyright (c) 2016, ESS
# License: See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _

def execute(filters=None):
	if not filters: filters = {}

	lab_procedure_list = get_lab_procedure(filters)
	columns = get_columns()

	if not lab_procedure_list:
		msgprint(_("No record found"))
		return columns, lab_procedure_list

	data = []
	for lp in lab_procedure_list:
		status = "Draft"
		if(lp.docstatus == 1):
			status = "Submitted"
			if(lp.approval_status == "Approved"):
				status = "Approved"
		elif(lp.docstatus == 2):
			status = "Cancelled"
		row = [ lp.test_name, lp.patient, lp.physician, lp.invoice, status, lp.result_date, lp.lab_test_type]

		data.append(row)

	return columns, data


def get_columns():
	columns = [
		_("Test") + ":Data:120",
		_("Patient") + ":Link/Customer:180",
		_("Doctor") + ":Link/Physician:120",
		_("Invoice") + ":Link/Sales Invoice:120",
		_("Status") + ":Data:120",
		_("Result Date") + ":Date:120",
		_("Lab Test Type") + ":Data:120",
	]

	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("customer"): 
		conditions += "and patient = %(customer)s"
	if filters.get("from_date"): 
		conditions += "and result_date >= %(from_date)s"
	if filters.get("to_date"): 
		conditions += " and result_date <= %(to_date)s"
	if filters.get("lab_test_type"): 
		conditions += " and lab_test_type = %(lab_test_type)s"

	return conditions

def get_lab_procedure(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select name, patient, test_name, patient_name, docstatus, 			result_date, physician, invoice, lab_test_type
		from `tabLab Procedure`
		where docstatus<2 %s order by submitted_date desc, name desc""" %
		conditions, filters, as_dict=1)

