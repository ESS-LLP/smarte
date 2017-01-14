# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, cstr, getdate, get_time
from frappe import msgprint, _
import datetime
from datetime import timedelta
import calendar
from frappe.model.document import Document

class Document_Scheduler(Document):
	"""
		WIP - Generic class to schedule documents
		eg: appointments to physician/modalities/other resources, room allocation/booking etc.
		Extending Document should have fields start_dt, end_dt, token (if token generated)
		Resource to have schedule(work hours) table, else treated 24/7

	"""
	def save(self):
		#validate scheduled docs
		super(Document_Scheduler, self).save()

def check_availability(doctype, df, token, dt, dn, date):
	# params doctype: doc to schedule,
	#df: doctype relation(O2M) field name to resource,
	#token: boolean, token generated or not,
	#dt: resource doctype,
	#dn: resource docname,
	#date: date to check availability
	if not token:
		frappe.msgprint("Implementation Pending")
		return
	resource = frappe.get_doc(dt, dn)
	date = getdate(date)
	day = calendar.day_name[date.weekday()]
	is_available_on_date = False
	availability = []
	if resource.schedule:
		for line in resource.schedule:
			if (line.day == day):
				is_available_on_date = True
				start = datetime.datetime.combine(date, get_time(line.start))
				end = datetime.datetime.combine(date, get_time(line.end))
				if token:
					scheduled = frappe.db.sql("""select token, end_dt from `tab{0}` where {1}='{2}' and start_dt between '{3}' and '{4}' order by token desc""".format(doctype, df, dn, start, end))
					if(len(scheduled) < line.limit):
						if(len(scheduled) > 0):
							token = scheduled[0][0] +1
							time = scheduled[0][1]
						else:
							token = 1
							time = datetime.datetime.combine(date, get_time(line.start))
						#calc endtime
						duration = get_time(line.average)
						end_time = time + datetime.timedelta(hours = duration.hour, minutes=duration.minute, seconds= duration.second)
						availability.append({"start" : time, "end":end_time, "token": token})

		if not is_available_on_date:
			availability.append({"msg": _("{0} not available on {1}").format(dn, date)})

	else:
		#resource is available 24/7, schedule for given time, validate overlaps
		availability.append({"msg": _("No schedule for selected {0}. Please set consultation schedule for {1}").format(dt, dn)})

	return availability

@frappe.whitelist()
def check_availability_by_resource(doctype, df, token, dt, dn, date):
	data = {}
	data[dn] = check_availability(doctype, df, token, dt, dn, date)
	return data


@frappe.whitelist()
def check_availability_by_relation(doctype, df, token, dt, rdt, rdn, rdf, date):
	#params rdt: relation doctype
	#rdn: relation docname

	#get all resources related to rdn
	resources = frappe.db.sql(""" select name from `tab%s` where %s= '%s' """ %(dt, rdf, rdn))
	if resources:
		data = {}
		for res in resources:
			data[res[0]] = check_availability(doctype, df, token, dt, res[0], date)
		return data
	else:
		msgprint(_("No {0} for {1} {2}").format(dt, rdt, rdn))
