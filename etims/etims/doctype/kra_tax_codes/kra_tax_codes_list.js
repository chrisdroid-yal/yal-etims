frappe.listview_settings["KRA Tax Codes"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Sync from eTIMS"), function () {
			frappe.show_progress(__("Syncing Tax Codes"), 1, 2);

			frappe.call({
				method: "etims.etims.doctype.kra_tax_codes.kra_tax_codes.sync_from_etims",
				args: {},
				callback: function (r) {
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
					frappe.msgprint(
						__("Error syncing tax codes: ") + __(error.message || error),
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
