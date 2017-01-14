// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Discharge Summary', {
	refresh: function(frm) {
		frm.add_custom_button(__('View Inpatient'), function() { 
			frappe.set_route("Form", "InPatients", frm.doc.inpatient);			
		} );
	}
});

frappe.ui.form.on("Discharge Summary", "inpatient",
    function(frm) {
	if(frm.doc.inpatient){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "InPatients",
		        name: frm.doc.inpatient
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "patient", data.message.patient)
				frappe.model.set_value(frm.doctype,frm.docname, "physician", data.message.physician)
				frappe.model.set_value(frm.doctype,frm.docname, "admit_date", data.message.admit_date)
				frappe.model.set_value(frm.doctype,frm.docname, "discharge_date", data.message.discharge_date)
		    }
		})
	}
});

frappe.ui.form.on("Discharge Summary", "physician",
    function(frm) {
	if(frm.doc.physician){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Physician",
		        name: frm.doc.physician
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "visit_department",data.message.department)
		    }
		})
	}
});

frappe.ui.form.on("Discharge Summary", "patient",
    function(frm) {
        if(frm.doc.patient){
		frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Customer",
		        name: frm.doc.patient
		    },
		    callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "patient_age", data.message.age)
				frappe.model.set_value(frm.doctype,frm.docname, "patient_sex", data.message.sex)
		    }
		})
	}
});
