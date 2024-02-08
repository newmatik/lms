from __future__ import unicode_literals

import frappe
import frappe.www.list
from frappe import _

no_cache = 1

def get_context(context):
    if frappe.session.user == "Guest":
        frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)

        context.show_sidebar = True
    
    else:
        context.no_cache = 1

        try:
            course_name = frappe.form_dict["course"]
        except KeyError:
            frappe.local.flags.redirect_location = "/courses"
            raise frappe.Redirect

        course = frappe.get_doc("LMS Course", course_name)
        if course is None:
            frappe.local.flags.redirect_location = "/courses"
            raise frappe.Redirect

        context.course = course
        membership = course.get_membership(frappe.session.user)
        context.course.query_parameter = "?batch=" + membership.batch if membership and membership.batch else ""
        context.membership = membership
        if context.course.upcoming:
            context.is_user_interested = get_user_interest(context.course.name)
        context.metatags = {
            "title": course.title,
            "image": course.image,
            "description": course.short_introduction,
            "keywords": course.title
        }

def get_user_interest(course):
    return frappe.db.count("LMS Course Interest",
            {
                "course": course,
                "user": frappe.session.user
            })
