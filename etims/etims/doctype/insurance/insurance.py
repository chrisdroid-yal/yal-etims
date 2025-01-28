# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from utils import Utils
import requests


class Insurance(Document):

	
	def before_save(self):

		device_init = frappe.get_doc("Device Initialization", {"default": 1})

		if not device_init:
			frappe.throw("Device not Initialized")

		used = True if self.used else False

		url = f"{device_init.url}AddInsuranceV2"
		payload = {
			"insuranceCode": self.code,
			"insuranceName": self.name1,
			"premiumRate": self.rate,
			"isUsed": used,
		}
		headers = {
			"accept": "*/*",
			"key": device_init.api_key,
		}

		try:
			requests.post(url, headers=headers, data=payload)
		except Exception as e:
			frappe.throw(f"Failed to sync insurance {self.name1} to ETIMS: {str(e)}")
