frappe.listview_settings["KRA Codes"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Sync from eTIMS"), function () {
			let progress = 0;
			frappe.show_progress(__("Syncing from eTIMS..."), progress);

			let progressInterval = setInterval(function () {
				if (progress < 90) {
					progress += 5;
					frappe.show_progress(__("Syncing from eTIMS..."), progress);
				}
			}, 100);

			frappe.call({
				method: "etims.etims.doctype.kra_codes.kra_codes.sync_from_etims",
				args: {},
				callback: function (r) {
					clearInterval(progressInterval);
					frappe.hide_progress();

					if (r.message) {
						frappe.msgprint(`${[r.message]}`);
						frappe.set_route("List", "KRA Codes");
					}
				},
				error: function (error) {
					clearInterval(progressInterval);
					frappe.hide_progress();
					frappe.msgprint(__(error));
				},
				success: function () {
					clearInterval(progressInterval);
					frappe.hide_progress();
				},
			});
		});
	},
};
