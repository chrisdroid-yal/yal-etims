# Copyright (c) 2025, Your Apps Limited Kenya and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class UnitTestKRATaxCodes(UnitTestCase):
	"""
	Unit tests for KRATaxCodes.
	Use this class for testing individual functions and methods.
	"""

	pass


class IntegrationTestKRATaxCodes(IntegrationTestCase):
	"""
	Integration tests for KRATaxCodes.
	Use this class for testing interactions between multiple components.
	"""

	pass
