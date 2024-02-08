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
        try:
            hackathon = frappe.form_dict['hackathon']
        except KeyError:
            frappe.local.flags.redirect_location = '/hackathons'
            raise frappe.Redirect
        context.projects = get_hackathon_projects(hackathon)
        context.hackathon = hackathon
        context.talks = get_hackathon_talks(hackathon)
        context.updates = get_hackathon_updates(context.projects)

def get_hackathon_projects(hackathon):
    return frappe.get_all("Community Project", filters={"hackathon":hackathon}, fields=["name", "project_short_intro"])

def get_hackathon_talks(hackathon):
    return frappe.get_all("Community Talk", {"event": hackathon}, ["topic", "speaker", "date_and_time", "video_link"])

def get_hackathon_updates(projects):
    project_list = [project.name for project in projects]
    return frappe.get_all("Community Project Update", {"project": ["in", project_list]}, ["project", "`update` as project_update", "owner", "creation"])