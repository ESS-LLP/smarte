# Copyright (c) 2015, ESS. and Contributors
# License: ESS See license.txt

from __future__ import unicode_literals

def get_notification_config():
	return { "for_doctype":
		{
			"Lab Procedure": {"docstatus": 0},
			"Sample Collection": {"docstatus": 0},
			"Appointment": {"status": "Open"},
			"Service Task": {"status": "Open"},
			"Consultation": {"docstatus": 0}
		}
	}
