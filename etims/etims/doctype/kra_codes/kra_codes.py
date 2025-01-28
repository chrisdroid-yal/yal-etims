# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from utils import Utils
import requests

@frappe.whitelist()
@frappe.whitelist()
def sync_from_etims():

    device_init = frappe.get_doc("Device Initialization", {"default": 1})

    if not device_init:
        frappe.throw("Device not initialized")

    url = f"{device_init.url}GetCodeListV2"
    params = {"date": "20210101120000"}
    headers = {
        "accept": "*/*",
        "key": device_init.api_key,
    }
    
    response = requests.get(url, headers=headers, params=params)
    kra_codes = response.json()['responseData']['clsList']
    
    success_count = 0
    skip_count = 0
    
    for kra_code in kra_codes:
        
        # Check if code already exists using code_class_id
        if frappe.db.exists("KRA Codes", {"code_class_id": kra_code['cdCls']}):
            skip_count += 1
            continue
            
        used = 1 if kra_code['useYn'] == 'Y' else 0
        
        try:
            kra_code_doc = frappe.get_doc({
                "doctype": "KRA Codes",
                "code_class_id": kra_code['cdCls'],
                "code_class_name": kra_code['cdClsNm'],
                "code_class_description": kra_code['cdClsDesc'],
                "used": used,
                "user_defined_name_1": kra_code['userDfnNm1'],
                "user_defined_name_2": kra_code['userDfnNm2'],
                "user_defined_name_3": kra_code['userDfnNm3'],
            })
            kra_code_doc.insert()
            success_count += 1
        except Exception as e:
            frappe.log_error(f"Error syncing KRA Code {kra_code['cdCls']}: {str(e)}", "ETIMS KRA Code Sync Error")
            continue

    return f"Sync completed: {success_count} KRA Codes added, {skip_count} KRA Codes skipped"

class KRACodes(Document):
	pass
