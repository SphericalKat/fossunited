# Copyright (c) 2024, Frappe x FOSSUnited and Contributors
# See license.txt
import frappe
from frappe.tests.utils import FrappeTestCase

from fossunited.doctype_ids import FOSS_USER_PROFILE


class TestFOSSGlobalCFPReviewSettings(FrappeTestCase):
    def test_global_setting_creation(self):
        # Given a new FOSS Global CFP Review Settings document
        # When the document is inserted without any members
        settings = frappe.get_doc(
            {
                "doctype": "FOSS Global CFP Review Settings",
                "members": [],
            }
        )
        settings.insert()
        # Then the document should be created
        self.assertTrue(settings)

    def test_role_assign_on_member_addition(self):
        # Given a new FOSS Global CFP Review Settings document
        settings = frappe.get_doc(
            {
                "doctype": "FOSS Global CFP Review Settings",
                "members": [],
            }
        )
        settings.insert()

        test_profile = frappe.get_doc(
            FOSS_USER_PROFILE, {"user": "test1@example.com"}
        )

        # When a member is added to the members field
        settings.append("members", {"profile": test_profile.name})
        settings.save()

        test_user = frappe.get_doc("User", test_profile.user)
        # Then the user should have the 'CFP Reviewer' role
        self.assertTrue(
            frappe.db.exists(
                "Has Role",
                {"role": "CFP Reviewer", "parent": test_user.name},
            )
        )

    def test_role_unassign_on_member_removal(self):
        # Given a new FOSS Global CFP Review Settings document
        settings = frappe.get_doc(
            {
                "doctype": "FOSS Global CFP Review Settings",
                "members": [],
            }
        )
        settings.insert()

        test_profile = frappe.get_doc(
            FOSS_USER_PROFILE, {"user": "test2@example.com"}
        )
        settings.append("members", {"profile": test_profile.name})
        settings.save()

        test_user = frappe.get_doc("User", test_profile.user)
        self.assertTrue(
            frappe.db.exists(
                "Has Role",
                {"role": "CFP Reviewer", "parent": test_user.name},
            )
        )

        # When a member is removed from the members field
        settings.members = []
        settings.save()

        # Then the user should not have the 'CFP Reviewer' role
        self.assertFalse(
            frappe.db.exists(
                "Has Role",
                {"role": "CFP Reviewer", "parent": test_user.name},
            )
        )
