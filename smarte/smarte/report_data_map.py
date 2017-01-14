# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

# mappings for table dumps
# "remember to add indexes!"

data_map = {
	"Customer": {
		"columns": ["name", "creation", "owner", "if(customer_name=name, '', customer_name) as customer_name",
			"customer_group as parent_customer_group", "territory as parent_territory"],
		"conditions": ["docstatus < 2"],
		"order_by": "name",
		"links": {
			"parent_customer_group": ["Customer Group", "name"],
			"parent_territory": ["Territory", "name"],
			"owner" : ["User", "name"]
		}
	},
	"Customer Group": {
		"columns": ["name", "parent_customer_group"],
		"conditions": ["docstatus < 2"],
		"order_by": "lft"
	},
	"Territory": {
		"columns": ["name", "parent_territory"],
		"conditions": ["docstatus < 2"],
		"order_by": "lft"
	},
	"Appointment": {
		"columns": ["name", "appointment_type", "patient", "physician", "start_dt", "department", "status"],
		"order_by": "name",
		"links": {
			"physician": ["Physician", "name"],
			"appointment_type": ["Appointment Type", "name"]
		}
	},
	"Physician": {
		"columns": ["name", "department"],
		"order_by": "name",
		"links": {
			"department": ["Department", "name"],
		}
				
	},
	"Appointment Type": {
		"columns": ["name"],
		"order_by": "name"		
	},
	"Department": {
		"columns": ["name"],
		"order_by": "name"		
	},
	"User": {
		"columns": ["name"],
		"order_by": "name"		
	}
}
