from __future__ import unicode_literals

import frappe
import frappe.www.list
from frappe import _
from urllib.parse import urlencode

no_cache = 1

def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

		context.show_sidebar = True
	else:
		context.no_cache = 1
		context.hackathons = get_hackathons()

def get_hackathons():
	return frappe.get_all("Community Hackathon")