# -*- coding: utf-8 -*-
# Copyright (c) 2015, ESS LLP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class ServiceUnit(Document):
	def validate(self):
		for child in self.assigned_users:
			if child.user :
				validate_for_enabled_user(child.user)
				#fix issues  
				#validate_duplicate_user(child.user, self.name, child.name)

	def on_update(self):
		if self.zones:
			service_units_to_zone(self)
		for child in self.assigned_users:
			if child.user :
				frappe.permissions.add_user_permission("Service Unit", self.name, child.user)

def validate_for_enabled_user(user):
	enabled = frappe.db.get_value("User", user, "enabled")
	if enabled is None:
		frappe.throw(_("User {0} does not exist").format(user))
	if enabled == 0:
		frappe.throw(_("User {0} is disabled").format(user))

def validate_duplicate_user(user, parent):
	users = frappe.db.sql_list("""select name from `tabUser List` where
		user=%s and parent=%s""", (user, parent))
	if users:
		frappe.throw(_("Service Unit {0} is already assigned to User {1}").format(
			parent, user), frappe.DuplicateEntryError)
	
def service_units_to_zone(self):
	for z in self.zones:
		zone = frappe.get_doc("Zone", z.zone)
		for units in zone.service_units:
			if units.type == self.type :
				cur_unit = frappe.get_doc("Service Unit", units.service_unit)
				rm_zone_from_unit(z.zone, cur_unit.name)
				rm_unit_from_zone(units)

		add_unit_to_zone(zone, self)

def add_unit_to_zone(zone, self):
	unit_type = frappe.get_doc("Unit Type", self.type)
	unit = zone.append("service_units")
	unit.service_unit = self.name
	unit.type = self.type
	unit.nursing = unit_type.nursing
	unit.sample = unit_type.sample
	unit.procedure = unit_type.procedure
	unit.routine = unit_type.routine
	zone.save(ignore_permissions=True)

def rm_unit_from_zone(units):
	frappe.db.sql("""delete from `tabService Unit List` where name=%s""",(units.name))

def rm_zone_from_unit(zone, parent):
	frappe.db.sql("""delete from `tabZone List` where zone=%s and parent=%s""",(zone, parent))
