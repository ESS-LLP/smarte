/*
(c) ESS 2015-16
*/
frappe.listview_settings['Lab Procedure'] = {
	add_fields: ["name", "approval_status", "invoice"],
	filters:[["docstatus","!=","1"]],
	get_indicator: function(doc) {
		if(doc.approval_status=="Approved"){
        		return [__("Approved"), "green", "approval_status,=,Approved"];
        	}
	},
	onload: function(me){
	if(!frappe.defaults.get_default("automate_lab_procedure_creation")){
		me.page.set_primary_action(__("Create Result From Invoice"),function(){
		var d = new frappe.ui.Dialog({
			title: __("Select Invoice"),
			fields: [{
					"fieldtype": "Link",
					"label": "Sales Invoice",
					"fieldname": "Sales Invoice",
					"options": "Sales Invoice",
					"get_query": {'lab_procedure_created' : 0, 'docstatus' : 1, 'billed_in': 'Laboratory'},
					"reqd": 1
				}],
			primary_action_label: __("Create Procedures"),
			primary_action : function(){
					var values = d.get_values();
					if(!values)
						return;
					create_test_from_template(values["Sales Invoice"]);
					d.hide();
				}
		})
		d.show();

		var create_test_from_template = function(sale_invoice){
			frappe.call({
				"method": "smarte.laboratory.doctype.lab_procedure.lab_procedure.create_lab_procedure_from_create_invoice_btn",
				"args": {invoice : sale_invoice},           
			    callback: function (data) {
				if(!data.exc){
					frappe.route_options = {"invoice": sale_invoice}
					frappe.set_route("List", "Lab Procedure");
				}
			    }
			})
		}

		},"icon-file-alt");
	}
	}

};



