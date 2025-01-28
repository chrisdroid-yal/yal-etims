frappe.listview_settings["KRA Locale"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Sync from eTIMS"), function () {
			frappe.show_progress(__("Syncing KRA Locales"), 1, 2);

			frappe.call({
				method: "etims.etims.doctype.kra_locale.kra_locale.sync_from_etims",
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
						__("Error syncing KRA Locales: ") + __(error.message || error),
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
