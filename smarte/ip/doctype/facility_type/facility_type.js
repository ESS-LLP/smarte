// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt
frappe.ui.form.on("Facility Type",{
		//Refernce item.js Ln90
	room_type: function(frm) {
	if(!frm.doc.item_code)
		frm.set_value("item_code", frm.doc.room_type);
	if(!frm.doc.description)
		frm.set_value("description", frm.doc.room_type);
	}
});

cur_frm.cscript.custom_refresh = function(doc) {
	// use the __islocal value of doc, to check if the doc is saved or not
	if(doc.item_code){
		cur_frm.set_df_property("item_code", "read_only", doc.__islocal ? 0 : 1);
	}
	if(!doc.__islocal) {
		if(doc.disabled == 1){
			cur_frm.add_custom_button(__('Enable'), function() {
				enable_facility_type(cur_frm);
			} );
		}
		else{
			cur_frm.add_custom_button(__('Disable'), function() {
				disable_facility_type(cur_frm);
			} );
		}
	}
}

var disable_facility_type = function(frm){
	var doc = frm.doc;
	frappe.call({
		method: 		"smarte.ip.doctype.facility_type.facility_type.disable_enable_facility_type",
		args: {status: 1, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		}
	});
}

var enable_facility_type = function(frm){
	var doc = frm.doc;
	frappe.call({
		method: 		"smarte.ip.doctype.facility_type.facility_type.disable_enable_facility_type",
		args: {status: 0, name: doc.name},
		callback: function(r){
			cur_frm.reload_doc();
		}
	});
}

frappe.ui.form.on("Facility Type", "rate", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Facility Type", "item_group", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});
frappe.ui.form.on("Facility Type", "description", function(frm,cdt,cdn){

	frm.doc.change_in_item = 1;

});