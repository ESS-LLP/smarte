// Copyright (c) 2016, ESS and contributors
// For license information, please see license.txt


// Display the result entry portion of Test Result (invoice having the type of results)
cur_frm.cscript.custom_refresh = function(doc) {
	cur_frm.toggle_display("sb_sensitivity", doc.sensitivity_toggle=="1");
	cur_frm.toggle_display("sb_special", doc.special_toggle=="1");
	cur_frm.toggle_display("sb_normal", doc.normal_toggle=="1");
	if(frappe.defaults.get_default("require_sample_collection")){
		cur_frm.set_df_property("sample", "hidden", 0);
	}else { cur_frm.set_df_property("sample", "hidden", 1); }
	/* set readonly by js
	cur_frm.toggle_enable('normal_test_items', false)
	cur_frm.toggle_enable('special_test_items', false)
	cur_frm.toggle_enable('sensitivity_test_items', false)
	*/
}


frappe.ui.form.on('Lab Procedure', {
	setup: function(frm) {
		frm.get_field('normal_test_items').grid.editable_fields = [
			{fieldname: 'test_name', columns: 3},
			{fieldname: 'test_event', columns: 2},
			{fieldname: 'result_value', columns: 2},
			{fieldname: 'test_uom', columns: 1},
			{fieldname: 'normal_range', columns: 2}
		];
		frm.get_field('special_test_items').grid.editable_fields = [
			{fieldname: 'test_particulars', columns: 3},
			{fieldname: 'result_value', columns: 7}
		];
	},
	refresh :  function(frm){
		refresh_field('normal_test_items');
		refresh_field('special_test_items');
		if(frm.doc.docstatus==1 && frm.doc.approval_status!='Approved' &&
		    frappe.defaults.get_default("require_test_result_approval") &&
			frappe.user.has_role("Procedure Approver")){
			frm.add_custom_button(__('Approve'), function() {
				status_update(frm);
			 } );
		}
		if(frm.doc.docstatus==1 && frm.doc.sms_sent==0){
			frm.add_custom_button(__('Send SMS'), function() {
			       make_dialog(frm);
			} );
		}

	},
	onload: function (frm) {
		frm.set_value("user",frappe.user.name);
		if(frm.doc.employee){
			frappe.call({
				method: "frappe.client.get",
				args:{
					doctype: "Employee",
					name: frm.doc.employee
				},
				callback: function(arg){
					frappe.model.set_value(frm.doctype,frm.docname,"employee_name", arg.message.employee_name);
					frappe.model.set_value(frm.doctype,frm.docname,"employee_designation", arg.message.designation);
				}
			})
		}
   	},

})

//Child row deleteion cath here
frappe.ui.form.on('Normal Test Items', {
    normal_test_items_remove: function(frm) {
        msgprint("Deletion is not permitted !");
        cur_frm.reload_doc();
    }
});

//Child row deleteion cath here
frappe.ui.form.on('Special Test Items', {
    special_test_items_remove: function(frm) {
        msgprint("Deletion is not permitted !");
        cur_frm.reload_doc();
    }
});

//Child row deleteion cath here
frappe.ui.form.on('Sensitivity Test Items', {
    sensitivity_test_items_remove: function(frm) {
        msgprint("Deletion is not permitted !");
        cur_frm.reload_doc();
    }
});

var status_update = function(frm){
	var doc = frm.doc;
	frappe.call({
		method: 		"smarte.laboratory.doctype.lab_procedure.lab_procedure.update_approval_status",
		args: {status: "Approved", name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		}
	});
}

cur_frm.cscript.custom_before_submit =  function(doc) {
	if(doc.normal_test_items){
		for(result in doc.normal_test_items){
			if(!doc.normal_test_items[result].result_value &&
					doc.normal_test_items[result].require_result_value == 1){
				msgprint("Please fill all required Result Value(s)");
				throw("Error");
			}
		}
	}
	if(doc.special_test_items){
		for(result in doc.special_test_items){
			if(!doc.special_test_items[result].result_value &&
					doc.special_test_items[result].require_result_value == 1){
				msgprint("Please fill all required Result Value(s)")
				throw("Error");
			}
		}
	}
}

// Filter for sales invoice field, fetch only invoices for which results are not created
cur_frm.fields_dict['invoice'].get_query = function(doc, cdt, cdn) {
	return{
		//docstatus :0 - invoice not submitted
		//docstatus :1 - submitted invoice
		filters : {"docstatus" : 1}
	}
}


var make_dialog = function(frm) {
	var number = frm.doc.mobile;
	var company  = frappe.defaults.get_user_default("company")
	var emailed = 	"Hello, "+ frm.doc.patient + "\nYour "+ frm.doc.test_name + " result has been emailed to " + frm.doc.email + ".\nThank You, \n"+company ;
	var printed = 	"Hello, " + frm.doc.patient + "\nYour "+ frm.doc.test_name + " result is ready with "+company+". \nThank You, Good Day";

	var dialog = new frappe.ui.Dialog({
		title: 'Send SMS',
		width: 400,
		fields: [
			{fieldname:'sms_type', fieldtype:'Select', label:'Type', options:
				['Emailed','Printed']},
			{fieldname:'number', fieldtype:'Data', label:'Mobile Number', reqd:1},
			{fieldname:'messages_label', fieldtype:'HTML'},
			{fieldname:'messages', fieldtype:'HTML', reqd:1}
		],
		primary_action_label: __("Send"),
		primary_action : function(){
				var values = dialog.fields_dict;
				if(!values){
					return;
				}
				send_sms(values,frm);
				dialog.hide();
			}
	})
	if(frm.doc.report_preference == "Email"){
		dialog.set_values({
			'sms_type': "Emailed",
			'number': number
		})
		dialog.fields_dict.messages_label.html("Message".bold())
		dialog.fields_dict.messages.html(printed)
	}else{
		dialog.set_values({
			'sms_type': "Printed",
			'number': number
		})
		dialog.fields_dict.messages_label.html("Message".bold())
		dialog.fields_dict.messages.html(printed)
	}
	var fd = dialog.fields_dict;
	$(fd.sms_type.input).change(function(){
		if(dialog.get_value('sms_type') == 'Emailed'){
			dialog.set_values({
				'number': number
			});
			fd.messages_label.html("Message".bold())
			fd.messages.html(emailed)
		}else{
			dialog.set_values({
				'number': number
			})
			fd.messages_label.html("Message".bold())
			fd.messages.html(printed)
		}
	})
	dialog.show();
}

var send_sms = function(v,frm){
	var doc = frm.doc;
	number = v.number.last_value
	messages = v.messages.wrapper.innerText
	frappe.call({
		method: "erpnext.setup.doctype.sms_settings.sms_settings.send_sms",
		args: {
			receiver_list: [number],
			msg: messages
		},
		callback: function(r) {
			if(r.exc) {msgprint(r.exc); return; }
			else{
				frappe.call({
					method: "smarte.laboratory.doctype.lab_procedure.lab_procedure.update_lab_procedure_print_sms_email_status",
					args: {print_sms_email: "sms_sent", name: doc.name},
					callback: function(r){
						cur_frm.reload_doc();
					}
				});
			}
		}
	});
}
