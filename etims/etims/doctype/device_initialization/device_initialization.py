# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class DeviceInitialization(Document):
	
	def before_save(self):

		if not re.match(r"^[A|P|a|p]{1}[0-9]{9}[A-Za-z]{1}$", self.tin):
			frappe.throw("Invalid TIN")
		
