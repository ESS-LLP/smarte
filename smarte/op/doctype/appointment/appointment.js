// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt
frappe.provide("erpnext.queries");
frappe.ui.form.on('Appointment', {
	refresh: function(frm) {
		if(frm.doc.patient && (frappe.user.has_role("IP Physician")||frappe.user.has_role("OP Physician"))){
			frm.add_custom_button(__('History'), function() {
				frappe.route_options = {"patient": frm.doc.patient}
				frappe.set_route("medical_record");
			 },__("View") );
		};
		if(frm.doc.status == "Open" && (frappe.user.has_role("IP Physician")||frappe.user.has_role("OP Physician"))){
			frm.add_custom_button(__('Mark Closed'), function() {
				btn_update_status(frm, "Closed");
			 } );
			frm.add_custom_button(__('Mark Pending'), function() {
				btn_update_status(frm, "Pending");
			 } );
		};
		if(frm.doc.status == "Pending"){
			frm.add_custom_button(__('Set Open'), function() {
				btn_update_status(frm, "Open");
			 } );
		};
		if(!frm.doc.__islocal && frappe.user.has_role("IP Physician") && frm.doc.status == "Open"){
			frm.add_custom_button(__("Consultation"),function(){
				btn_create_consultation(frm);
			},"Create");
		}
		if(!frm.doc.__islocal && (frappe.user.has_role("OP Manager") || frappe.user.has_role("OP User"))){
			if(frm.doc.invoiced == '1'){
				frm.add_custom_button(__('Invoice'), function() {
					frappe.set_route("Form", "Sales Invoice", frm.doc.invoice);
				 },__("View") );
			}
			else{
				frm.add_custom_button(__('Invoice'), function() {
					btn_invoice_consultation(frm);
				 },__("Create") );
			}
		};
		if(frm.doc.__islocal){
			frm.add_custom_button(__('By Physician'), function() {
				check_availability_on_date(frm);
			 },__("Check Availability") );
			frm.add_custom_button(__('By Department'), function() {
				check_availability_by_dept(frm);
			 },__("Check Availability") );
		};
		frm.set_df_property("patient", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("token", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("appointment_type", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("physician", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("ref_physician", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("department", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("appointment_date", "read_only", frm.doc.__islocal ? 0:1);
	},
	onload:function(frm){
		if(frm.doc.__islocal){
			frappe.model.set_value(frm.doctype,frm.docname,"department", "Clinic");
			frappe.model.set_value(frm.doctype,frm.docname,"appointment_time", null);
		}

	},
	appointment_date: function(frm){
		frappe.model.set_value(frm.doctype,frm.docname, 'start_dt', new Date(frm.doc.appointment_date + ' ' + frm.doc.appointment_time))
	},
	appointment_time: function(frm){
		frappe.model.set_value(frm.doctype,frm.docname, 'start_dt', new Date(frm.doc.appointment_date + ' ' + frm.doc.appointment_time))
	},
});

var btn_create_consultation = function(frm){
	var doc = frm.doc;
	frappe.call({
		method:"smarte.op.doctype.appointment.appointment.create_consultation",
		args: {appointment: doc.name},
		callback: function(data){
			if(!data.exc){
				var doclist = frappe.model.sync(data.message);
				frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
			}
		}
	});
}

var check_availability_by_dept = function(frm){
	if(frm.doc.department && frm.doc.appointment_date){
		frappe.call({
			method:
			"smarte.op.doctype.appointment.appointment.check_available_by_dept",
			args: {department: frm.doc.department, date: frm.doc.appointment_date},
			callback: function(r){
				if(r.message) show_availability(frm, r.message)
				else msgprint("Booking not available");
			}
		});
	}else{
		msgprint("Please select Department and Start Date");
	}
}

var check_availability_on_date = function(frm){
	if(frm.doc.physician && frm.doc.appointment_date){
		frappe.call({
			method:
			"smarte.op.doctype.appointment.appointment.check_available_on_date",
			args: {physician: frm.doc.physician, date: frm.doc.appointment_date},
			callback: function(r){
				show_availability(frm, r.message)
			}
		});
	}else{
		msgprint("Please select Physician, Start Date");
	}
}


var show_availability = function(frm, result){
	var d = new frappe.ui.Dialog({
		title: __("Appointment Availability (Time - Token)"),
		fields: [
			{
				fieldtype: "HTML", fieldname: "availability"
			}
		]
	});
	var html_field = d.fields_dict.availability.$wrapper;
	html_field.empty();

	var list = ''
	$.each(result, function(i, v) {
		if(v[0]["msg"]){
			var message = $(repl('<div class="col-xs-12" style="padding-top:20px;" >%(msg)s</div></div>', {msg: v[0]["msg"]})).appendTo(html_field);
			return
		}
		$(repl('<div class="col-xs-12" style="padding-top:20px;"><b> %(physician)s</b></div>', {physician: i})).appendTo(html_field);
		$.each(result[i], function(x, y){
			var row = $(repl('<div class="col-xs-12" style="padding-top:12px; text-align:center;" ><div class="col-xs-4"> %(start)s </div><div class="col-xs-4"> %(token)s </div><div class="col-xs-4"><button class="btn btn-default btn-xs"> <a data-start="%(start)s" data-end="%(end)s" data-token="%(token)s" data-physician="%(physician)s"  href="#">Book</a></button></div></div>', {start: y["start"], end: y["end"], token: y["token"], physician: i})).appendTo(html_field);
			row.find("a").click(function() {
				app_datetime = new Date($(this).attr("data-start"));
				/*hours = app_datetime.getHours();
				minutes = app_datetime.getMinutes();
				seconds = app_datetime.getSeconds();
				appointment_time = hours + ":" + minutes + ":" + seconds;*/
				appointment_time = app_datetime.toLocaleTimeString();
				frm.doc.appointment_time = appointment_time
				frm.doc.physician = $(this).attr("data-physician");
				frm.doc.start_dt = $(this).attr("data-start");
				frm.doc.end_dt = $(this).attr("data-end");
				frm.doc.token = $(this).attr("data-token");
				refresh_field("physician");refresh_field("token");refresh_field("start_dt");
				refresh_field("appointment_time");refresh_field("end_dt")
				d.hide();
				return false;
			});
		})

	});
	d.show();
}

var btn_update_status = function(frm, status){
	var doc = frm.doc;
	frappe.call({
		method:
		"smarte.op.doctype.appointment.appointment.update_status",
		args: {appointmentId: doc.name, status:status},
		callback: function(data){
			if(!data.exc){
				cur_frm.reload_doc();
			}
		}
	});
}

var btn_invoice_consultation = function(frm){
	var doc = frm.doc;
	frappe.call({
		method:
		"smarte.op.doctype.appointment.appointment.create_consultation_invoice",
		args: {appointmentId: doc.name},
		callback: function(data){
			if(!data.exc){
				if(data.message){
					var doclist = frappe.model.sync(data.message);
					frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
				}
				cur_frm.reload_doc();
			}
		}
	});
}

frappe.ui.form.on("Appointment", "physician",
    function(frm) {
	if(frm.doc.physician){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Physician",
		        name: frm.doc.physician
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "department",data.message.department)
		    }
		})
	}
});
