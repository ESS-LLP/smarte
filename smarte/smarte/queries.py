# Copyright (c) 2015, ESS. and Contributors
# License: ESS See license.txt

from __future__ import unicode_literals
import frappe
from frappe.desk.reportview import get_match_cond
from frappe.model.db_query import DatabaseQuery
from frappe.utils import nowdate

def get_filters_cond(doctype, filters, conditions):
	if filters:
		flt = filters
		if isinstance(filters, dict):
			filters = filters.items()
			flt = []
			for f in filters:
				if isinstance(f[1], basestring) and f[1][0] == '!':
					flt.append([doctype, f[0], '!=', f[1][1:]])
				else:
					flt.append([doctype, f[0], '=', f[1]])

		query = DatabaseQuery(doctype)
		query.filters = flt
		query.conditions = conditions
		query.build_filter_conditions(flt, conditions)

		cond = ' and ' + ' and '.join(query.conditions)
	else:
		cond = ''
	return cond


# Customer Query
def customer_query(doctype, txt, searchfield, start, page_len, filters):
	fields = ["name", "mobile", "sex", "age"]
	
	fields = ", ".join(fields)

	return frappe.db.sql("""select {fields} from `tabCustomer`
		where docstatus < 2
			and (   phone like %(txt)s
				or email like %(txt)s or mobile like%(txt)s
				or customer_name like %(txt)s) and disabled=0
			{mcond}
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			if(locate(%(_txt)s, customer_name), locate(%(_txt)s, customer_name), 99999),
			idx desc,
			name, customer_name
		limit %(start)s, %(page_len)s""".format(**{
			"fields": fields,
			"mcond": get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		})

