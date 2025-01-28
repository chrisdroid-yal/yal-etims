frappe.listview_settings["KRA Currency"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Sync from eTIMS"), function () {
			frappe.show_progress(__("Syncing KRA Currencies"), 1, 2);

			frappe.call({
				method: "etims.etims.doctype.kra_currency.kra_currency.sync_from_etims",
				args: {},
				callback: function (r) {
					frappe.hide_progress();

					if (r.message) {
						const { success_count, skip_count } = r.message;
						frappe.msgprint(
							__(`Sync completed successfully!\n
                            Records created: ${success_count}\n
                            Records skipped: ${skip_count}`),
							__("Success")
						);
						listview.refresh();
					}
				},
				error: function (error) {
					frappe.hide_progress();
					frappe.msgprint(
						__("Error syncing KRA Currencies: ") + __(error.message || error),
						__("Error")
					);
				},
				always: function () {
					frappe.hide_progress();
				},
			});
		});
	},
};
