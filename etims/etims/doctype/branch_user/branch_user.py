# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from utils import Utils
import requests


class BranchUser(Document):
	
	def before_save(self):

		device_init = frappe.get_doc("Device Initialization", {"default": 1})

		if not device_init:
			frappe.throw("Device not initialized")

		payload = {
			"branchUserId": self.id,
			"branchUserName": self.name1,
			"password": self.password,
			"address": self.address,
			"contactNo": self.contact_no,
			"authenticationCode": self.authentication_code,
			"isUsed": True,
			"remark": self.remark,
		}

		url = f"{device_init.url}AddBranchUserV2"
		headers = {
			"accept": "*/*",
			"key": device_init.api_key,
		}
		
		response = requests.post(url, headers=headers, json=payload)
		data = response.json()['status']

		if not data:
			frappe.throw(f"{response.json()['message']}")
