# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Post(Document):
	def after_insert(self):
		if self.reply_to:
			frappe.publish_realtime('new_post_reply' + self.reply_to, self, after_commit=True)
		else:
			frappe.publish_realtime('new_post', self, after_commit=True)

@frappe.whitelist()
def toggle_like(post_name, user=None):
	liked_by = frappe.db.get_value('Post', post_name, 'liked_by')
	liked_by = liked_by.split('\n') if liked_by else []
	user = user or frappe.session.user

	if user in liked_by:
		liked_by.remove(user)
	else:
		liked_by.append(user)

	frappe.publish_realtime('update_liked_by' + post_name, frappe.session.user, after_commit=True)
	frappe.db.set_value('Post', post_name, 'liked_by', '\n'.join(liked_by))


