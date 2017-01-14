# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from smarte.smarte.scheduler import Document_Scheduler, check_availability_by_relation, check_availability_by_resource
import time
from frappe.utils import cint, flt, cstr, getdate, get_time
from frappe import msgprint, _
import datetime
from datetime import timedelta
import calendar
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms

class Appointment(Document_Scheduler):
	def on_update(self):
		today = datetime.date.today()
		appointment_date = getdate(self.appointment_date)
		#If appointment created for today set as open
		if(today == appointment_date):
			frappe.db.set_value("Appointment",self.name,"status","Open")
			self.reload()

	def validate(self):
		if not self.end_dt:
			frappe.throw(_("Please use Check Availabilty and Book"))

	def after_insert(self):
		confirm_sms(self)

@frappe.whitelist()
def check_available_by_dept(department, date):
	if not (department or date):
		frappe.msgprint(_("Please select Department and Date"))
	return check_availability_by_relation("Appointment", "physician", True, "Physician", "Department", department, "department", date)

@frappe.whitelist()
def check_available_on_date(physician, date):
	if not (physician or date):
		frappe.msgprint(_("Please select Doctor and Date"))
	return check_availability_by_resource("Appointment", "physician", True, "Physician", physician, date)

@frappe.whitelist()
def update_status(appointmentId, status):
	appointment = frappe.get_doc("Appointment",appointmentId)
	appointment.status = status;
	appointment.save()

@frappe.whitelist()
def set_open_appointments():
	today = time.strftime("%d/%m/%y %H:%M:%S")
	date = getdate(today)
	frappe.db.sql("""update `tabAppointment` set status='Open' where status = 'Scheduled' and appointment_date = %s""",(today))

def confirm_sms(doc):
	if (frappe.db.get_value("OP Settings", None, "app_con")=='1'):
		messages = frappe.db.get_value("OP Settings", None, "app_con_msg")
		send_message(doc, messages)

@frappe.whitelist()
def create_consultation_invoice(appointmentId):
	valid = False
	fee_validity = None
	appointment = frappe.get_doc("Appointment",appointmentId)

	validity_exist = frappe.db.exists({
			"doctype": "Fee Validity",
			"physician": appointment.physician,
			"patient": appointment.patient})

	if validity_exist :
		fee_validity = frappe.get_doc("Fee Validity",validity_exist[0][0])
		if((fee_validity.valid_till >= appointment.appointment_date) and (fee_validity.visited < fee_validity.max_visit)):
			visited = fee_validity.visited + 1
			frappe.db.set_value("Fee Validity",fee_validity.name,"visited",visited)
			if(fee_validity.ref_invoice):
				frappe.db.set_value("Appointment",appointmentId,"invoiced",True)
				frappe.db.set_value("Appointment",appointmentId,"invoice",fee_validity.ref_invoice)
			valid = True
		else:
			fee_validity = update_fee_validity(fee_validity, appointment)
			sales_invoice = make_consultation_invoice(appointment)
	else:
		fee_validity = create_fee_validity(appointment)
		sales_invoice = make_consultation_invoice(appointment)

	if (valid):
		frappe.msgprint(_("{0} has a validity till {1}").format(appointment.patient, fee_validity.valid_till))
		return None
	else:
		sales_invoice.save(ignore_permissions=True)
		frappe.db.set_value("Fee Validity",fee_validity.name,"ref_invoice",sales_invoice.name)
		frappe.db.set_value("Appointment",appointmentId,"invoiced",True)
		frappe.db.set_value("Appointment",appointmentId,"invoice",sales_invoice.name)
		return sales_invoice.as_dict()

def update_fee_validity(fee_validity, appointment):
	max_visit = frappe.db.get_value("OP Settings", None, "max_visit")
	valid_days = frappe.db.get_value("OP Settings", None, "valid_days")
	date = appointment.appointment_date
	valid_till = date + datetime.timedelta(days=int(valid_days))
	fee_validity.max_visit = max_visit
	fee_validity.visited = 1
	fee_validity.valid_till = valid_till
	fee_validity.save(ignore_permissions=True)
	return fee_validity

def create_fee_validity(appointment):
	fee_validity = frappe.new_doc("Fee Validity")
	fee_validity.physician = appointment.physician
	fee_validity.patient = appointment.patient
	fee_validity = update_fee_validity(fee_validity, appointment)
	return fee_validity

def make_consultation_invoice(appointment):
	physician = frappe.get_doc("Physician",appointment.physician)
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.customer = appointment.patient
	sales_invoice.physician = appointment.physician
	sales_invoice.ref_physician = appointment.ref_physician
	today = time.strftime("%d/%m/%y %H:%M:%S")
	sales_invoice.due_date = getdate(today)
	sales_invoice.territory = "India"
	sales_invoice.billed_in = "OP"

	item_line = sales_invoice.append("items")
	item_line.item_code = "Consulting Charges"
	item_line.item_name = "Consulting Charges"
	item_line.description = appointment.physician
	item_line.qty = 1
	item_line.rate = physician.op_consulting_charge
	item_line.amount = physician.op_consulting_charge
	sales_invoice.set_missing_values()
	return sales_invoice

@frappe.whitelist()
def create_consultation(appointment):
	appointment = frappe.get_doc("Appointment",appointment)
	consultation = frappe.new_doc("Consultation")
	consultation.appointment = appointment.name
	consultation.patient = appointment.patient
	consultation.physician = appointment.physician
	consultation.ref_physician = appointment.ref_physician
	consultation.visit_department = appointment.department
	consultation.patient_age = appointment.patient_age
	consultation.patient_sex = appointment.patient_sex
	consultation.consultation_date = appointment.appointment_date
	return consultation.as_dict()

def remind_appointment():
	if (frappe.db.get_value("OP Settings", None, "app_rem")=='1'):
		rem_before = datetime.datetime.strptime(frappe.get_value("OP Settings", None, "rem_before"), "%H:%M:%S")
		rem_dt = datetime.datetime.now() + datetime.timedelta(hours = rem_before.hour, minutes=rem_before.minute, seconds= rem_before.second)

		appointment_list = frappe.db.sql("select name from `tabAppointment` where start_dt between %s and %s and reminded = 0 ", (datetime.datetime.now(), rem_dt))

		for i in range (0,len(appointment_list)):
			doc = frappe.get_doc("Appointment", appointment_list[i][0])
			messages = frappe.db.get_value("OP Settings", None, "app_rem_msg")
			send_message(doc, messages)
			frappe.db.set_value("Appointment",doc.name,"reminded",1)

def send_message(doc, messages):
	patient = frappe.get_doc("Customer",doc.patient)
	if(patient.mobile):
		context = {"doc": doc, "alert": doc, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))
		#jinja to string convertion happens here
		messages = frappe.render_template(messages, context)
		number = [patient.mobile]
		send_sms(number,messages)

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Appointment", filters)
	data = frappe.db.sql("""select name, patient, physician, appointment_type, department, status, start_dt, end_dt
		from `tabAppointment`
		where (start_dt between %(start)s and %(end)s)
				and docstatus < 2
				{conditions}
		""".format(conditions=conditions), {
			"start": start,
			"end": end
		}, as_dict=True, update={"allDay": 0})
	return data
