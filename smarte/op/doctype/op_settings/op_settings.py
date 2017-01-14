# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from erpnext.setup.doctype.sms_settings.sms_settings import send_sms
class OPSettings(Document):
	pass


def generate_patient_id(doc, method):
	if (frappe.db.get_value("OP Settings", None, "patient_id")=='1'):
		pid = make_autoname(frappe.db.get_value("OP Settings", None, "id_series"), "", doc)
		doc.patient_id = pid
		doc.save()
	send_registration_sms(doc, method)

def send_registration_sms(doc, method):
	if (frappe.db.get_value("OP Settings", None, "reg_sms")=='1'):
		context = {"doc": doc, "alert": doc, "comments": None}
		if doc.get("_comments"):
			context["comments"] = json.loads(doc.get("_comments"))
		messages = frappe.db.get_value("OP Settings", None, "reg_msg")
		messages = frappe.render_template(messages, context)
		number = [doc.mobile]
		send_sms(number,messages)