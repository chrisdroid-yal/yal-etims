frappe.listview_settings["KRA Notice List"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Sync from eTIMS"), function () {
			frappe.call({
				method: "etims.etims.doctype.kra_notice_list.kra_notice_list.sync_from_etims",
				args: {},
				callback: function (r) {
					frappe.hide_progress();

					if (r.message) {
						frappe.msgprint(`${[r.message]}`);
						frappe.set_route("List", "KRA Notice List");
					}
				},
				error: function (error) {
					frappe.hide_progress();
					frappe.msgprint(__(error));
				},
				success: function () {
					frappe.hide_progress();
				},
			});
		});
	},
};
