// Copyright (c) 2016, ESS LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Dosage', {
	dosage_morning: function(frm){
		set_values(frm)
	},
	dosage_noon: function(frm){
		set_values(frm)
	},
	dosage_evening: function(frm){
		set_values(frm)
	},
	refresh: function(frm){
		frm.set_df_property("dosage_morning", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("dosage_noon", "read_only", frm.doc.__islocal ? 0:1);
		frm.set_df_property("dosage_evening", "read_only", frm.doc.__islocal ? 0:1);
		if(!frm.doc.dosage_morning || frm.doc.dosage_morning <= 0){
			frm.set_df_property("morning_time", "read_only", frm.doc.__islocal ? 0:1);
		}
		if(!frm.doc.dosage_noon || frm.doc.dosage_noon <= 0){
			frm.set_df_property("noon_time", "read_only", frm.doc.__islocal ? 0:1);
		}
		if(!frm.doc.dosage_evening || frm.doc.dosage_evening <= 0){
			frm.set_df_property("eve_time", "read_only", frm.doc.__islocal ? 0:1);
		}
	}
});

var set_values = function(frm){
	cur_frm.set_value("dosage", create_name(frm.doc));
	cur_frm.set_value("dosage_number", set_dosage_number(frm.doc));
}

var create_name = function(doc){
	name = "";
	if(doc.dosage_morning !== undefined && doc.dosage_morning !== null) { name = doc.dosage_morning + "-" };
	if(doc.dosage_noon !== undefined && doc.dosage_noon !== null) { name += doc.dosage_noon + "-" };
	if(doc.dosage_evening !== undefined && doc.dosage_evening !== null) {name += doc.dosage_evening };
	name += " per Day"
	return name
}

var set_dosage_number = function(doc){
	dosage_number = 0
	if(doc.dosage_morning){
		dosage_number = dosage_number+doc.dosage_morning
	}
	if(doc.dosage_noon){
		dosage_number = dosage_number+doc.dosage_noon
	}
	if(doc.dosage_evening){
		dosage_number = dosage_number+doc.dosage_evening
	}
	dosage_number = Math.round(dosage_number)
	return dosage_number
}

