# Copyright (c) 2025, Your Apps Limited Kenya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from utils import Utils
import requests

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
    country_codes = [d for d in kra_codes if d.get("cdCls") == "05"]

    if not country_codes:
        frappe.log_error("No country codes found with cdCls = 05", "ETIMS KRA Country Code Sync Error")
        return

    # Get the first matching country code dictionary since filter returns a list
    country_code_data = country_codes[0]
    
    if 'dtlList' not in country_code_data:
        frappe.log_error("No dtlList found in country code data", "ETIMS KRA Country Code Sync Error")
        return

    success_count = 0
    skip_count = 0

    for country in country_code_data['dtlList']:
        if frappe.db.exists("KRA Country Codes", {"code": country['cd']}):
            skip_count += 1
            continue

        used = 1 if country['useYn'] == 'Y' else 0

        try:
            country_doc = frappe.get_doc({
                "doctype": "KRA Country Codes",
                "code_class": country_code_data['cdCls'],
                "code": country['cd'],
                "name1": country['cdNm'],
                "description": country['cdDesc'],
                "used": used,
                "sort_order": country['srtOrd'],
                "user_defined_code_1": country['userDfnCd1'],
                "user_defined_code_2": country['userDfnCd2'],
                "user_defined_code_3": country['userDfnCd3'],
            })
            country_doc.insert()
            success_count += 1
        except Exception as e:
            frappe.log_error(
                f"Error syncing KRA Country Code {country.get('cd', 'Unknown')}: {str(e)}", 
                "ETIMS KRA Country Code Sync Error"
            )
            continue

    return {
        "success_count": success_count,
        "skip_count": skip_count
    }

class KRACountryCodes(Document):
	pass
