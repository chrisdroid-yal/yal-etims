# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from utils import Utils
import requests

@frappe.whitelist()
def sync_from_etims():

    device_init = frappe.get_doc("Device Initialization", {"default": 1})

    if not device_init:
        frappe.throw("Device not initialized")

    url = f"{device_init.url}GetNoticeListV2"
    params = {"date": "20210101120000"}
    headers = {
        "accept": "*/*",
        "key": device_init.api_key,
    }
    
    response = requests.get(url, headers=headers, params=params)

    if not response.json()['status']:
        frappe.throw(f"{response.json()['message']}")

    notices = response.json()['responseData']['noticeList']

    
    success_count = 0
    skip_count = 0
    
    for notice in notices:
        # Check if notice already exists using notice_no
        if frappe.db.exists("kra_notice_list", {"notice_no": notice['noticeNo']}):
            skip_count += 1
            continue
        
        try:
            notice_doc = frappe.get_doc({
                "doctype": "KRA Notice List",
                "notice_no": notice['noticeNo'],
                "title": notice['title'],
                "content": notice['cont'],
                "details_url": notice['dtlUrl'],
                "registration_name": notice['regrNm'],
                "registration_date": notice['regDt'],
            })
            notice_doc.insert()
            success_count += 1
        except Exception as e:
            frappe.log_error(f"Error syncing Notice {notice['noticeNo']}: {str(e)}", "ETIMS Notice Sync Error")
            continue

    return f"Sync completed: {success_count} Notices added, {skip_count} Notice skipped"


class KRANoticeList(Document):
	pass
