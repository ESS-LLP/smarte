# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import datetime
import time
from frappe.utils import getdate, get_time

class InPatients(Document):
	pass

@frappe.whitelist()
def admit_and_allocate_patient(patient, inpatient, date_in, time_in, bed, facility_type, facility, expected_discharge):
	allocate_facility(patient,inpatient,date_in,time_in,bed,facility_type, facility, expected_discharge,"Occupied",True)
	update_customer(patient, inpatient, True)
	update_bed(bed, patient, True)
	update_facility(facility, patient, True)
	frappe.db.set_value("InPatients",inpatient,"status","Admitted")
	frappe.db.set_value("InPatients",inpatient,"admit_date",date_in)

@frappe.whitelist()
def facility_transfer_allocation(patient,inpatient,bed_number,facility_type, facility_name, expected_discharge, old_facility_name):
	allocate_facility(patient, inpatient, datetime.date.today(), datetime.datetime.now(), bed_number, facility_type, facility_name, expected_discharge, "Occupied", True)
	update_bed(bed_number, patient, False)
	#New facility update
	update_facility(facility_name, patient, True)
	#Old facility update
	update_facility(old_facility_name, patient, False)
	
@frappe.whitelist()
def discharge_patient(patient,inpatient):
	update_customer(patient, inpatient, False)
	disallocate_facility_bed(inpatient)
	inpatients = frappe.get_doc("InPatients",inpatient)
	update_facility(inpatients.current_facility, patient, False)
	update_bed(None, patient, False)
	frappe.db.set_value("InPatients",inpatient,"status","Discharged")

@frappe.whitelist()
def queue_discharge_patient(patient,inpatient):
	frappe.db.set_value("InPatients",inpatient,"status","Queued")
	frappe.db.set_value("InPatients",inpatient,"discharge_date",datetime.date.today())

@frappe.whitelist()
def cancel_scheduled_inpatient(inpatient):
	frappe.db.set_value("InPatients",inpatient,"status","Cancelled")

@frappe.whitelist()	
def allocate_facility(patient,inpatient,date_in,time_in,bed,facility_type, facility, expected_discharge,status,occupied):
	inpatients = frappe.get_doc("InPatients",inpatient)
	#Validate the facility already occupied,leaved the previous patient when schedule and admit the patient to the facility
	if(inpatients.facility_alloc):
		for allocations in inpatients.facility_alloc:
			allocations.status = "Left" #All other allocated facility marked as Left in inpatients
	if(inpatients.facility_alloc and inpatients.status == "Scheduled"):
		allocation = inpatients.facility_alloc[0]
	else:
		allocation = inpatients.append("facility_alloc")
	inpatients.current_facility = facility
	allocation.bed = bed
	allocation.facility_type = facility_type
	allocation.facility = facility
	allocation.expected_discharge = expected_discharge
	if (occupied): #On Scheduled Status it may be occupied by any other patient
		allocation.patient_occupied = occupied #Done Admit : set to it True
	allocation.date_in = date_in
	allocation.time_in = time_in
	allocation.status = status
	allocation.facility_leaved = False
	inpatients.save()

@frappe.whitelist()
def create_consultation(patient,inpatient):
	inpatients = frappe.get_doc("InPatients",inpatient)
	consultation = frappe.new_doc("Consultation")
	consultation.patient = inpatients.patient
	consultation.physician = inpatients.physician
	consultation.visit_department = inpatients.visit_department
	consultation.patient_age = inpatients.patient_age
	consultation.patient_sex = inpatients.patient_sex
	consultation.symptoms = inpatients.complaints
	consultation.vitals = inpatients.vitals
	consultation.diagnosis = inpatients.diagnosis
	consultation.inpatient = True
	consultation.inpatient_id = inpatient
	return consultation.as_dict()

@frappe.whitelist()
def create_inv_for_facility_used(patient,inpatient):
	inpatients = frappe.get_doc("InPatients",inpatient)
	sales_invoice = frappe.new_doc("Sales Invoice")
	sales_invoice.customer = inpatients.patient
	sales_invoice.physician = inpatients.physician
	sales_invoice.due_date = time.strftime("%m/%d/%Y")
	sales_invoice.territory = "India"
	sales_invoice.billed_in = "IP"
	
	#Iterate for item and pass to the method
	for item_line in inpatients.facility_alloc:
		item = frappe.get_doc("Item", item_line.facility_type)
		facility_type = frappe.get_doc("Facility Type", item_line.facility_type)
		day_hours = facility_type.per
		
		period_start = getdate(item_line.date_in)
		if(item_line.expected_discharge):
			period_end = getdate(item_line.expected_discharge)		
		else:
			today = time.strftime("%d/%m/%y %H:%M:%S")
			period_end = getdate(today)
		no_of_days = (period_end-period_start).days +1
		if(day_hours == "Day"):
			qty = no_of_days
		else:
			qty = no_of_days*24	
		
		
		price_list = frappe.db.get ("Item Price",{"item_code":item.item_code})
		rate = price_list.price_list_rate

		create_sales_invoice_item_lines(item, sales_invoice, qty, rate)

	#income_account and cost_center in itemlines - by set_missing_values()
	sales_invoice.set_missing_values()
	return sales_invoice.as_dict()
	
def create_sales_invoice_item_lines(item, sales_invoice, qty, rate):
	sales_invoice_line = sales_invoice.append("items")
	sales_invoice_line.item_code = item.item_code
	sales_invoice_line.item_name =  item.item_name
	sales_invoice_line.qty = qty
	sales_invoice_line.rate = rate
	sales_invoice_line.description = item.description

@frappe.whitelist()
def create_discharge_summary(inpatient):
	inpatients = frappe.get_doc("InPatients",inpatient)
	ds = frappe.new_doc("Discharge Summary")
	ds.patient = inpatients.patient
	ds.physician = inpatients.physician
	ds.visit_department = inpatients.visit_department
	ds.patient_age = inpatients.patient_age
	ds.patient_sex = inpatients.patient_sex
	ds.inpatient = inpatient
	ds.admit_date = inpatients.admit_date
	ds.discharge_date = inpatients.discharge_date
	ds.save(ignore_permissions=True)
	frappe.db.set_value("InPatients", inpatient, "created_ds", True)

def disallocate_facility_bed(inpatient):
	inpatients = frappe.get_doc("InPatients",inpatient)
	for allocation in inpatients.facility_alloc:
		allocation.status = "Left" 
	inpatients.save()

def update_customer(patient, inpatient, admit):
	if(admit):
		frappe.db.sql("""update `tabCustomer` set inpatient=%s, inpatient_id=%s where name=%s""",(True,inpatient,patient))
	else:
		frappe.db.sql("""update `tabCustomer` set inpatient=%s, inpatient_id=%s where name=%s""",(False,None,patient))

def update_bed(bed, patient, admit):
	if(not admit):
		frappe.db.sql("""update `tabBed` set occupied=%s, patient=%s where patient=%s""",(False,None,patient))
	if(bed):
		frappe.db.sql("""update `tabBed` set occupied=%s, patient=%s where name=%s""",(True,patient,bed))

def update_facility(facility, patient, admit):
	if(facility):
		facility = frappe.get_doc("Facility",facility)
		if(admit):
			num_occupied = facility.num_occupied+1
		else:
			num_occupied = facility.num_occupied-1
		
		if(num_occupied == facility.num_beds):
			occupied = True
		else:
			occupied = False
		
		frappe.db.sql("""update `tabFacility` set num_occupied=%s, occupied=%s where name=%s""",(num_occupied,occupied,facility.name))
	