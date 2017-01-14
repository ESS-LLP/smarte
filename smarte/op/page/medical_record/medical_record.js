/*
ESS
*/
frappe.provide("frappe.medical_record");
frappe.pages['medical_record'].on_page_load = function(wrapper) {
	var me = this;

	//frappe.require('assets/frappe/js/lib/flot/jquery.flot.js');
	//frappe.require('assets/frappe/js/lib/flot/jquery.flot.downsample.js');

	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Medical Record',
	});

	frappe.breadcrumbs.add("OP");


	page.main.html(frappe.render_template("customer_select", {}));
	var customer = frappe.ui.form.make_control({
		parent: page.main.find(".customer"),
		df: {
			fieldtype: "Link",
			options: "Customer",
			fieldname: "customer",
			change: function(){
				//frappe-list is the class of div in the html page.
				page.main.find(".frappe-list").html("");
				show_patient_info(customer.get_value(), me);
				draw_page(customer.get_value(), me);
			}
		},
		only_input: true,
	});
	customer.refresh();


	this.page.main.on("click", ".medical_record-message", function() {
		var	doctype = $(this).attr("data-doctype"),
			docname = $(this).attr("data-docname");

		if (doctype && docname) {
			frappe.route_options = {
				scroll_to: { "doctype": doctype, "name": docname }
			}
			frappe.set_route(["Form", doctype, docname]);
		}
	});

	this.page.sidebar.on("click", ".edit-details", function() {
		patient = customer.get_value();
		if (patient) {
			frappe.set_route(["Form", "Customer", patient]);
		}
	});

}

frappe.pages['medical_record'].refresh = function(wrapper) {
	var me = this;

	if(frappe.route_options) {
		if(frappe.route_options.patient){
			me.page.main.find(".frappe-list").html("");
			customer = frappe.route_options.patient;
			show_patient_info(customer, me);
			draw_page(customer,me);
			me.page.main.find("[data-fieldname='customer']").val(customer);
			frappe.route_options = null;
		}
	}
}
var show_patient_info = function(customer, me){
	frappe.call({
		    "method": "frappe.client.get",
		    args: {
		        doctype: "Customer",
		        name: customer
		    },
		    callback: function (data) {
					var details = "<div style='padding-left:10px;'></br><b>Patient Details</b><br>";
					if(data.message.age) details += "<br><b>Age :</b> " + data.message.age;
					if(data.message.sex) details += "<br><b>Gender :</b> " + data.message.sex;
					if(data.message.email) details += "<br><b>Email :</b> " + data.message.email;
					if(data.message.mobile) details += "<br><b>Mobile :</b> " + data.message.mobile;
					if(data.message.occupation) details += "<br><b>Occupation :</b> " + data.message.occupation;
					if(data.message.blood_group) details += "<br><b>Blood group : </b>" + data.message.blood_group;
					if(data.message.allergies) details +=  "<br><br><b>Allergies : </b>"+  data.message.allergies;
					if(data.message.medication) details +=  "<br><b>Medication : </b>"+  data.message.medication;
					if(data.message.alcohol_current_use) details +=  "<br><br><b>Alcohol use : </b>"+  data.message.alcohol_current_use;
					if(data.message.alcohol_past_use) details +=  "<br><b>Alcohol past use : </b>"+  data.message.alcohol_past_use;
					if(data.message.tobacco_current_use) details +=  "<br><b>Tobacco use : </b>"+  data.message.tobacco_current_use;
					if(data.message.tobacco_past_use) details +=  "<br><b>Tobacco past use : </b>"+  data.message.tobacco_past_use;
					if(data.message.medical_history) details +=  "<br><br><b>Medical history : </b>"+  data.message.medical_history;
					if(data.message.surgical_history) details +=  "<br><b>Surgical history : </b>"+  data.message.surgical_history;
					if(data.message.surrounding_factors) details +=  "<br><br><b>Occupational hazards : </b>"+  data.message.surrounding_factors;
					if(data.message.other_risk_factors) details += "<br><b>Other risk factors : </b>" + data.message.other_risk_factors;
					if(data.message.customer_details) details += "<br><br><b>More info : </b>" + data.message.customer_details;
					if(details !== "") details += "<br><br><a class='btn btn-default btn-sm edit-details'>Edit Details</a></b> </div>"
					me.page.sidebar.addClass("col-sm-3");
					me.page.sidebar.html(details);
					me.page.wrapper.find(".layout-main-section-wrapper").addClass("col-sm-9");
		    }
		})
}
var draw_page = function(customer,me){
	frappe.model.with_doctype("Patient Medical Record", function() {
		me.page.list = new frappe.ui.Listing({
			hide_refresh: true,
			page: me.page,
			method: 'smarte.op.page.medical_record.medical_record.get_feed',
			args: {name: customer},
			parent: $("<div></div>").appendTo(me.page.main),
			render_row: function(row, data) {
				new frappe.medical_record.Feed(row, data);
			},
			show_filters: true,
			doctype: "Patient Medical Record",
		});

		me.page.list.run();

	});

}

frappe.medical_record.last_feed_date = false;
frappe.medical_record.Feed = Class.extend({
	init: function(row, data) {
		this.scrub_data(data);
		this.add_date_separator(row, data);
		if(!data.add_class)
			data.add_class = "label-default";

		data.link = "";
		if (data.reference_doctype && data.reference_name) {
			data.link = frappe.format(data.reference_name, {fieldtype: "Link", options: data.reference_doctype},
				{label: __(data.reference_doctype)});
		}

		$(row)
			.append(frappe.render_template("medical_record_row", data))
			.find("a").addClass("grey");
	},
	scrub_data: function(data) {
		data.by = frappe.user.full_name(data.owner);
		data.imgsrc = frappe.utils.get_file_link(frappe.user_info(data.owner).image);

		data.icon = "icon-flag";
	},
	add_date_separator: function(row, data) {
		var date = dateutil.str_to_obj(data.creation);
		var last = frappe.medical_record.last_feed_date;

		if((last && dateutil.obj_to_str(last) != dateutil.obj_to_str(date)) || (!last)) {
			var diff = dateutil.get_day_diff(dateutil.get_today(), dateutil.obj_to_str(date));
			if(diff < 1) {
				pdate = 'Today';
			} else if(diff < 2) {
				pdate = 'Yesterday';
			} else {
				pdate = dateutil.global_date_format(date);
			}
			data.date_sep = pdate;
			data.date_class = pdate=='Today' ? "date-indicator blue" : "date-indicator";
		} else {
			data.date_sep = null;
			data.date_class = "";
		}
		frappe.medical_record.last_feed_date = date;
	}
});
