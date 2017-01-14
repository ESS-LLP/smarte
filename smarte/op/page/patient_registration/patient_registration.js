frappe.pages['patient-registration'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Registration Analytics',
		single_column: true
	});
	new erpnext.RegistrationAnalytics(wrapper);

	frappe.breadcrumbs.add("OP");

}


erpnext.RegistrationAnalytics = frappe.views.TreeGridReport.extend({
	init: function(wrapper) {
		this._super({
			title: __("Registration Analytics"),
			page: wrapper,
			parent: $(wrapper).find('.layout-main'),
			page: wrapper.page,
			doctypes: ["Customer", "User"],
			tree_grid: { show: true }
		});


		this.tree_grids = {
			"User": {
				label: __("User"),
				show: true,
				item_key: "owner",
				formatter: function(item) {
					return item.name;
				}
			},
		}
	},
	setup_columns: function() {
		this.tree_grid = this.tree_grids[this.tree_type];

		var std_columns = [
			{id: "_check", name: __("Plot"), field: "_check", width: 40,
				formatter: this.check_formatter},
			{id: "name", name: this.tree_grid.label, field: "name", width: 300,
				formatter: this.tree_formatter},
			{id: "total", name: "Total", field: "total", plot: false,
				formatter: this.currency_formatter}
		];

		this.make_date_range_columns();
		this.columns = std_columns.concat(this.columns);
	},
	filters: [
		{fieldtype:"Select", label: __("Tree Type"), fieldname: "tree_type",
			options:["User"], filter: function(val, item, opts, me) {
				return me.apply_zero_filter(val, item, opts, me);}},
		{fieldtype:"Select", label: __("User"), link:"User", fieldname: "filter_user",
			default_value: __("Select User..."), filter: function(val, item, opts) {
				return val == opts.default_value || item.name == val || item._show;
			}, link_formatter: {filter_input: "name"}},		
		{fieldtype:"Date", label: __("From Date"), fieldname: "from_date"},
		{fieldtype:"Date", label: __("To Date"), fieldname: "to_date"},
		{fieldtype:"Select", label: __("Range"), fieldname: "range",
			options:[{label: __("Daily"), value: "Daily"}, {label: __("Weekly"), value: "Weekly"},
				{label: __("Monthly"), value: "Monthly"}, {label: __("Quarterly"), value: "Quarterly"},
				{label: __("Yearly"), value: "Yearly"}]}
	],
	setup_filters: function() {
		var me = this;
		this._super();
		this.trigger_refresh_on_change(["tree_type", "filter_user"]);

		//this.show_zero_check()
		this.setup_chart_check();
	},
	init_filter_values: function() {
		this._super();
		this.filter_inputs.range.val('Quarterly');
	},
	prepare_data: function() {
		var me = this;
		if (!this.tl) {
			this.tl = frappe.report_dump.data["Customer"]
		}
		if(!this.data || me.item_type != me.tree_type) {
			if(me.tree_type=='User') {
				var items = frappe.report_dump.data["User"];
			}
			me.item_type = me.tree_type
			me.parent_map = {};
			me.item_by_name = {};
			me.data = [];

			$.each(items, function(i, v) {
				var d = copy_dict(v);

				me.data.push(d);
				me.item_by_name[d.name] = d;
				if(d[me.tree_grid.parent_field]) {
					me.parent_map[d.name] = d[me.tree_grid.parent_field];
				}
				me.reset_item_values(d);
			});

			this.set_indent();


		} else {
			// otherwise, only reset values
			$.each(this.data, function(i, d) {
				me.reset_item_values(d);
			});
		}
		this.prepare_balances();
		if(me.tree_grid.show) {
			this.set_totals(false);
			this.update_groups();
		} else {
			this.set_totals(true);
		}


	},
	prepare_balances: function() {
		var me = this;
		var from_date = dateutil.str_to_obj(this.from_date);
		status = this.status;
		type = this.type;
		var to_date = dateutil.str_to_obj(this.to_date);
		$.each(this.tl, function(i, tl) {
			//if (me.is_default('company') ? true : tl.company === me.company) {
				var date = dateutil.str_to_obj(tl.creation);
				d = tl.creation.split(" ")[0];
				if (date >= from_date && date <= to_date) {
					var item = me.item_by_name[tl[me.tree_grid.item_key]] ||
						me.item_by_name['Not Set'];
					item[me.column_map[d].field] += 1;
				}
			//}
		});
	},
	update_groups: function() {
		var me = this;

		$.each(this.data, function(i, item) {
			var parent = me.parent_map[item.name];
			while(parent) {
				var parent_group = me.item_by_name[parent];

				$.each(me.columns, function(c, col) {
					if (col.formatter == me.currency_formatter) {
						parent_group[col.field] =
							flt(parent_group[col.field])
							+ flt(item[col.field]);
					}
				});
				parent = me.parent_map[parent];
			}
		});
	},
	set_totals: function(sort) {
		var me = this;
		var checked = false;
		$.each(this.data, function(i, d) {
			d.total = 0.0;
			$.each(me.columns, function(i, col) {
				if(col.formatter==me.currency_formatter && !col.hidden && col.field!="total")
					d.total += d[col.field];
				if(d.checked) checked = true;
			})
		});

		if(sort)this.data = this.data.sort(function(a, b) { return b.total - a.total; });

		if(!this.checked) {
			this.data[0].checked = true;
		}
	}

})
