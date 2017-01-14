# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import time
from frappe.utils import cstr

class LabProcedure(Document):
	def autoname(self):
		self.name = "-".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["test_name", "patient"]]))

		self.name = self.name + " (" + "/".join(filter(None,
			[cstr(self.get(f)).strip() for f in ["patient_age", "patient_sex"]])) + ")"

		self.name = self.name + "/" +cstr(self.get("invoice")).strip()

	def after_insert(self):
		create_new_lab_test_procedure_result(self)

	def on_submit(self):
		lab_test_procedure_result_status(self.name,"Submitted")
		frappe.db.set_value(self.doctype,self.name,"submitted_date",
					time.strftime("%y/%m/%d %H:%M:%S"))
		insert_lab_procedure_to_medical_record(self)
				
	def on_trash(self):
		frappe.throw("""Deletion is not permitted !""")

	def on_cancel(self):
		lab_test_procedure_result_status(self.name,"Cancelled")
		dlete_lab_procedure_from_medical_record(self)
		frappe.db.set_value("Lab Procedure",self.name,"approval_status",None)
		self.reload()
		
def lab_test_procedure_result_status(lab_procedure,status):
	frappe.db.sql("""update `tabLab Test Procedure Result` set workflow=%s where lab_procedure=%s""",(status, lab_procedure))

@frappe.whitelist()
def update_approval_status(status, name):
	frappe.db.set_value("Lab Procedure",name,"approval_status","Approved")
	frappe.db.set_value("Lab Procedure",name,"approved_date",time.strftime("%y/%m/%d %H:%M:%S"))
	lab_test_procedure_result_status(name,"Approved")

@frappe.whitelist()
def update_lab_procedure_print_sms_email_status(print_sms_email, name):
	frappe.db.set_value("Lab Procedure",name,print_sms_email,1)
	frappe.db.sql("""update `tabLab Test Procedure Result` set `%s`=1 where lab_procedure=%s"""\
	 	% (frappe.db.escape(print_sms_email), '%s'), (name))

def set_customer_age(doc):
	doc.customer_age = frappe.db.get_value("Customer", doc.customer, "age")
	frappe.db.set_value("Sales Invoice", doc.name, "customer_age", doc.customer_age)


def create_invoice_test_report(invoice):
	invoice_test_report = frappe.new_doc("Invoice Test Report")
	invoice_test_report.invoice = invoice.name
	invoice_test_report.patient = invoice.customer
	invoice_test_report.patient_age = invoice.customer_age
	invoice_test_report.patient_sex = invoice.customer_sex
	invoice_test_report.physician = invoice.physician
	invoice_test_report.ref_physician = invoice.ref_physician
	invoice_test_report.report_preference = invoice.report_preference
	return invoice_test_report

def create_lab_procedure(invoice, template):
	#create Test Result for template, copy vals from Invoice
	lab_procedure = frappe.new_doc("Lab Procedure")
	lab_procedure.invoice = invoice.name
	lab_procedure.patient = invoice.customer
	lab_procedure.patient_age = invoice.customer_age
	lab_procedure.patient_sex = invoice.customer_sex
	lab_procedure.physician = invoice.physician
	lab_procedure.ref_physician = invoice.ref_physician
	lab_procedure.lab_test_type = template.lab_test_type
	lab_procedure.internal_test = template.internal_test
	lab_procedure.lab_procedure_department = template.lab_procedure_department
	lab_procedure.test_name = template.test_name
	lab_procedure.test_group = template.test_group
	lab_procedure.result_date = time.strftime("%y/%m/%d")
	lab_procedure.report_preference = invoice.report_preference
	
	is_inpatient = frappe.db.get_value("Customer", invoice.customer, "inpatient")
	
	if is_inpatient:
		service_unit = get_service_unit(invoice.customer, "procedure")
		lab_procedure.service_unit = service_unit
	
	return lab_procedure

def create_normals(template, lab_procedure):
	lab_procedure.normal_toggle = "1"
	normal = lab_procedure.append("normal_test_items")
	normal.test_name = template.test_name
	normal.test_uom = template.test_uom
	normal.normal_range = template.test_normal_range
	normal.require_result_value = 1
	normal.template = template.name
	

def create_compounds(template, lab_procedure, is_group):
	lab_procedure.normal_toggle = "1"
	for normal_test_template in template.normal_test_templates:
		normal = lab_procedure.append("normal_test_items")
		if is_group:
			normal.test_event = normal_test_template.test_event
		else:
			normal.test_name = normal_test_template.test_event
		
		normal.test_uom = normal_test_template.test_uom
		normal.normal_range = normal_test_template.normal_range
		normal.require_result_value = 1
		normal.template = template.name
		
def create_specials(template, lab_procedure):
	lab_procedure.special_toggle = "1"
	if(template.sensitivity):
		lab_procedure.sensitivity_toggle = "1"
	for special_test_template in template.special_test_template:
		special = lab_procedure.append("special_test_items")
		special.test_particulars = special_test_template.particulars
		special.require_result_value = 1
		special.template = template.name

def create_sample_collection(template, invoice):
	if(template.sample):
		sample_exist = frappe.db.exists({
			"doctype": "Sample Collection",
			"invoice": invoice.name,
			"sample": template.sample})
		if sample_exist :
			#Update Sample Collection by adding quantity
			sample_collection = frappe.get_doc("Sample Collection",sample_exist[0][0])
			quantity = int(sample_collection.sample_quantity)+int(template.sample_quantity)
			if(template.sample_collection_details):
				sample_collection_details = sample_collection.sample_collection_details+"\n==============\n"+"Test :"+template.test_name+"\n"+"Collection Detials:\n\t"+template.sample_collection_details
				frappe.db.set_value("Sample Collection", sample_collection.name, 						"sample_collection_details",sample_collection_details)
			frappe.db.set_value("Sample Collection", sample_collection.name, 						"sample_quantity",quantity)
			
		else:
			#create Sample Collection for template, copy vals from Invoice
			sample_collection = frappe.new_doc("Sample Collection")
			sample_collection.invoice = invoice.name
			sample_collection.patient = invoice.customer
			sample_collection.patient_age = invoice.customer_age
			sample_collection.patient_sex = invoice.customer_sex
			sample_collection.sample = template.sample
			sample_collection.sample_uom = template.sample_uom
			sample_collection.sample_quantity = template.sample_quantity
			if(template.sample_collection_details):
				sample_collection.sample_collection_details = "Test :"+template.test_name+"\n"+"Collection Detials:\n\t"+template.sample_collection_details
			
			is_inpatient = frappe.db.get_value("Customer", invoice.customer, "inpatient")
			
			if is_inpatient:
				service_unit = get_service_unit(invoice.customer, "sample")
				sample_collection.service_unit = service_unit

			sample_collection.save()
	
		return sample_collection
		
def get_service_unit(customer, job_type):
	inpatient_id = frappe.db.get_value("Customer", customer, "inpatient_id")
	current_facility = frappe.get_value("InPatients", inpatient_id, "current_facility")
	zone = frappe.get_value("Facility", current_facility, "zone")
	service_unit = frappe.db.get_value("Service Unit List", {"parent": zone, job_type : 1}, "service_unit")
	return service_unit

# Call From hook to Create Test Result and Procedure.
@frappe.whitelist()
def create_lab_procedure_from_invoice_hook(doc, method):
	if(frappe.db.get_value("Laboratory Settings", None, "automate_lab_procedure_creation") == "1" and  doc.billed_in == 'Laboratory'):
		create_lab_procedure_from_invoice(doc)

# Call From Create From Invoice Btn to Create Test Result and Procedure.
@frappe.whitelist()
def create_lab_procedure_from_create_invoice_btn(invoice):
	invoice_doc = frappe.get_doc("Sales Invoice", invoice)
	create_lab_procedure_from_invoice(invoice_doc)

@frappe.whitelist()
def create_lab_procedure_from_invoice(doc):
	set_customer_age(doc)
	frappe.db.set_value("Sales Invoice", doc.name, "lab_procedure_created", 1)
	invoice_test_report = create_invoice_test_report(doc)
	
	customer_email = frappe.db.get_value("Customer", doc.customer, "email")
	customer_mobile = frappe.db.get_value("Customer", doc.customer, "mobile")
	
	invoice_test_report.email = customer_email
	invoice_test_report.mobile = customer_mobile

	collect_sample = 0;
	if(frappe.db.get_value("Laboratory Settings", None, "require_sample_collection") == "1"):
		collect_sample = 1
		
	for item_line in doc.items:
		item = frappe.get_doc("Item", item_line.item_code)
		#skip the loop if there is no test_template for Item
		if not (item.test_template):
			continue

		template = frappe.get_doc("Lab Test Template", item.test_template)

		lab_procedure = create_lab_procedure(doc, template)
		lab_procedure.email = customer_email
		lab_procedure.mobile = customer_mobile

		if(template.manually_submit_procedure == 1):

			if(collect_sample == 1):
				sample_collection = create_sample_collection(template, doc)
				if(sample_collection):
					lab_procedure.sample = sample_collection.name
		
				
			if(template.test_template_type == 'Single'):
				create_normals(template, lab_procedure)
		
			elif(template.test_template_type == 'Compound'):
				create_compounds(template, lab_procedure, False)

			elif(template.test_template_type == 'Descriptive'):
				create_specials(template, lab_procedure)


			elif(template.test_template_type == 'Grouped'):
				#iterate for each template in the group and create one result for all.
			
				for test_group in template.test_groups:
					#template_in_group = None
					if(test_group.test_template):
						template_in_group = frappe.get_doc("Lab Test Template", 
										test_group.test_template)

					if(template_in_group):
									
						if(template_in_group.test_template_type == 'Single'):
							create_normals(template_in_group, lab_procedure)
						

						elif(template_in_group.test_template_type == 'Compound'):
							normal_heading = lab_procedure.append("normal_test_items")
							normal_heading.test_name = template_in_group.test_name
							normal_heading.require_result_value = 0
							normal_heading.template = template_in_group.name
							create_compounds(template_in_group, lab_procedure, True)
						


						elif(template_in_group.test_template_type == 'Descriptive'):
							special_heading = lab_procedure.append("special_test_items")
							special_heading.test_name = template_in_group.test_name
							special_heading.require_result_value = 0
							special_heading.template = template_in_group.name
							create_specials(template_in_group, lab_procedure)
						
					else:
						normal = lab_procedure.append("normal_test_items")
						normal.test_name = test_group.group_event
						normal.test_uom = test_group.group_test_uom
						normal.normal_range = test_group.group_test_normal_range
						normal.require_result_value = 1
						normal.template = template.name

			lab_procedure.save(ignore_permissions=True) # insert the result
		else:
			lab_procedure.save(ignore_permissions=True) # insert the result
			lab_procedure.submit() # submit the result
		lab_test_procedure_result = invoice_test_report.append("lab_test_presult")
		lab_test_procedure_result.lab_procedure = lab_procedure.name
		if(template.manually_submit_procedure == 1):
			lab_test_procedure_result.workflow = "Draft"
		else:
			lab_test_procedure_result.workflow = "Submitted"
		lab_test_procedure_result.invoice = doc.name
		
	invoice_test_report.save(ignore_permissions=True)

# Call From hook to Create Test Result Procedure on Amend.
def create_new_lab_test_procedure_result(doc):
	if(doc.amended_from):
		invoice_test_report_id = frappe.db.sql("select name from `tabInvoice Test Report` where invoice=%s",(doc.invoice))
		invoice_test_report = frappe.get_doc("Invoice Test Report", invoice_test_report_id[0][0])
		lab_test_procedure_result = invoice_test_report.append("lab_test_presult")
		lab_test_procedure_result.lab_procedure = doc.name
		lab_test_procedure_result.workflow = "Draft"
		lab_test_procedure_result.invoice = doc.invoice
		invoice_test_report.save(ignore_permissions=True)

# Call From hook to Cancel All Related to Invoice.
@frappe.whitelist()
def invoice_cancel_hook(doc, method):
	#Change All Lab Porcedure status to Cancelled and Inv. Test Result status to Completed
	if(doc.lab_procedure_created==1):
		invoice_test_report_id = frappe.db.sql("select name from `tabInvoice Test Report` where invoice=%s",(doc.name))
		invoice_test_report = frappe.get_doc("Invoice Test Report", invoice_test_report_id[0][0])
		frappe.db.set_value("Invoice Test Report", invoice_test_report.name, "status", "Cancelled")	
		for inv_pro_linck in invoice_test_report.lab_test_presult :
			frappe.db.set_value("Lab Procedure", inv_pro_linck.lab_procedure, "docstatus", 2)
			lab_test_procedure_result_status(inv_pro_linck.lab_procedure, "Cancelled")
	
		sample_exist = frappe.db.exists({
		"doctype": "Sample Collection",
		"invoice": doc.name})
		if(sample_exist):
			frappe.db.sql("""update `tabSample Collection` set docstatus=2 where invoice=%s""",(doc.name))

@frappe.whitelist()
def get_employee_by_user_id(user_id):
	emp_id = frappe.db.get_value("Employee",{"user_id":user_id})
	employee = frappe.get_doc("Employee",emp_id)
	return employee


def insert_lab_procedure_to_medical_record(doc):
	subject = str(doc.test_name)
	if(doc.test_comment):
		subject += ", \n"+str(doc.test_comment)
	medical_record = frappe.new_doc("Patient Medical Record")
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = "Open"
	medical_record.communication_date = doc.result_date
	medical_record.reference_doctype = "Lab Procedure"
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)

def dlete_lab_procedure_from_medical_record(self):
	medical_record_id = frappe.db.sql("select name from `tabPatient Medical Record` where 			reference_name=%s",(self.name))
	
	if(medical_record_id[0][0]):
		frappe.delete_doc("Patient Medical Record", medical_record_id[0][0])




