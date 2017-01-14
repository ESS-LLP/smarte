# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime, time
class ServiceTask(Document):
	pass

def create_task_from_schedule():
	if(frappe.get_value("IP Settings", None, "auto_tasks") == '1'):
		open_before = datetime.datetime.strptime(frappe.get_value("IP Settings", None, "open_task_before"), "%H:%M:%S")
		open_dt = datetime.datetime.now() + datetime.timedelta(hours = open_before.hour, minutes=open_before.minute, seconds= open_before.second)

		schedule_list = frappe.db.sql("select name from `tabTask Schedule` where task_datetime between %s and %s and open=1 ", (datetime.datetime.now(), open_dt))

		for i in range (0,len(schedule_list)):
			schedule = frappe.get_doc("Task Schedule", schedule_list[i][0])
			if not frappe.db.exists(schedule.dt, schedule.dn):
				continue
			if(schedule.dt == "Drug Prescription"):
				job_type = "nursing"
			elif(schedule.dt == "IP Routine Observation"):
				job_type = "routine"
			if(schedule.inpatient):
				facility, patient = frappe.get_value("InPatients", {"name": schedule.inpatient}, ["current_facility", "patient"])
				zone = frappe.get_value("Facility", {"name": facility}, ["zone"])
				service_unit, unit_type = frappe.db.get_value("Service Unit List", {"parent": zone, job_type : 1}, ("service_unit", "type"))
				line = frappe.get_doc(schedule.dt, schedule.dn)
				if (line.doctype == "Drug Prescription"):
					comment = str(line.comment) if line.comment else ""
					message = str(line.drug_name) + "\t\t" + str(line.dosage) + "\t\t" + comment
				if (line.doctype == "IP Routine Observation"):
					comment = str(line.comment) if line.comment else ""
					message = str(line.routine_observation) + "\t\t" + str(line.dosage) + "\t\t" +  comment
				service_task = frappe.new_doc("Service Task")
				service_task.patient = patient
				service_task.facility = facility
				service_task.dt = schedule.dt
				service_task.dn = schedule.dn
				service_task.parent = schedule.parent_id
				service_task.service_unit = service_unit
				service_task.type = unit_type
				service_task.comment = message
				service_task.status = "Open"
				service_task.date = schedule.task_datetime.date()
				service_task.time = schedule.task_datetime.time()
				service_task.save(ignore_permissions=True)
			schedule.open = 0
			schedule.save(ignore_permissions=True)
