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
        context.live_courses, context.upcoming_courses = get_courses()
        context.metatags = {
            "title": "All Courses",
            "image": frappe.db.get_single_value("Website Settings", "banner_image"),
            "description": "This page lists all the courses published on our website",
            "keywords": "All Courses, Courses, Learn"
        }

def get_courses():
    course_names = frappe.get_all("LMS Course",
                                filters={"is_published": True},
                                fields=["name", "upcoming"])

    live_courses, upcoming_courses = [], []
    for course in course_names:
        if course.upcoming:
            upcoming_courses.append(frappe.get_doc("LMS Course", course.name))
        else:
            live_courses.append(frappe.get_doc("LMS Course", course.name))
    return live_courses, upcoming_courses
