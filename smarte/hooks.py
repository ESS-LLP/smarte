# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "smarte"
app_title = "Smarte"
app_publisher = "ESS LLP"
app_description = "Frappe Modules for Healthcare Management"
app_icon = "octicon octicon-pulse"
app_color = "#FF888B"
app_email = "info@earthianslive.com"
app_license = "GNU GENERAL PUBLIC LICENSE (v3)"

fixtures = ["Custom Field", "Custom Script", "Print Format"]

error_report_email = "support@smartehis.com"

app_include_js = "assets/js/smarte.min.js"

required_apps = ["erpnext"]

#boot_session = "smarte.boot.boot_session"
notification_config = "smarte.smarte.notifications.get_notification_config"

dump_report_map = "smarte.smarte.report_data_map.data_map"

standard_queries = {
	"Customer": "smarte.smarte.queries.customer_query",
}


website_context = {
	"favicon": 	"/assets/smarte/images/favicon.png",
	"splash_image": "/assets/smarte/images/smarte.png"
}

doc_events = {
	"Sales Invoice": {
		"on_submit": "smarte.laboratory.doctype.lab_procedure.lab_procedure.create_lab_procedure_from_invoice_hook",
		"on_cancel": "smarte.laboratory.doctype.lab_procedure.lab_procedure.invoice_cancel_hook",
	},
	"Customer": {
		"after_insert": "smarte.op.doctype.op_settings.op_settings.generate_patient_id"
	}
}

scheduler_events = {
	"all": [
 		"smarte.ip.doctype.service_task.service_task.create_task_from_schedule",
 		"smarte.op.doctype.appointment.appointment.remind_appointment"
 	],
 	"daily": [
 		"smarte.op.doctype.appointment.appointment.set_open_appointments"
 	]
}

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/smarte/css/smarte.css"
# app_include_js = "/assets/smarte/js/smarte.js"

# include js, css files in header of web template
# web_include_css = "/assets/smarte/css/smarte.css"
# web_include_js = "/assets/smarte/js/smarte.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "smarte.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "smarte.install.before_install"
# after_install = "smarte.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "smarte.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"smarte.tasks.all"
# 	],
# 	"daily": [
# 		"smarte.tasks.daily"
# 	],
# 	"hourly": [
# 		"smarte.tasks.hourly"
# 	],
# 	"weekly": [
# 		"smarte.tasks.weekly"
# 	]
# 	"monthly": [
# 		"smarte.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "smarte.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "smarte.event.get_events"
# }
