#!/usr/bin/env python3
"""
Test module for Frappe workflow automation.

This module contains sample functions to test:
- Code quality checks
- Linting and formatting
- Security scanning
- Release automation
"""

import frappe
from typing import Dict, List, Optional


def get_user_data(user_id: str) -> Optional[Dict]:
	"""
	Get user data from database.
	
	Args:
		user_id (str): The user ID to fetch data for
		
	Returns:
		Optional[Dict]: User data if found, None otherwise
	"""
	if not user_id:
		frappe.throw(_("User ID is required"))
	
	try:
		user = frappe.get_doc("User", user_id)
		return {
			"name": user.name,
			"email": user.email,
			"full_name": user.full_name,
			"enabled": user.enabled
		}
	except frappe.DoesNotExistError:
		return None


def validate_email(email: str) -> bool:
	"""
	Validate email address format.
	
	Args:
		email (str): Email address to validate
		
	Returns:
		bool: True if valid, False otherwise
	"""
	import re
	
	pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
	return bool(re.match(pattern, email))


def process_user_list(users: List[Dict]) -> List[Dict]:
	"""
	Process a list of users and return filtered data.
	
	Args:
		users (List[Dict]): List of user dictionaries
		
	Returns:
		List[Dict]: Processed user data
	"""
	processed_users = []
	
	for user in users:
		if user.get("enabled") and validate_email(user.get("email", "")):
			processed_users.append({
				"id": user.get("name"),
				"email": user.get("email"),
				"display_name": user.get("full_name") or user.get("name")
			})
	
	return processed_users


def create_notification(user_id: str, message: str, priority: str = "medium") -> str:
	"""
	Create a notification for a user.
	
	Args:
		user_id (str): Target user ID
		message (str): Notification message
		priority (str): Priority level (low, medium, high)
		
	Returns:
		str: Notification ID
	"""
	if priority not in ["low", "medium", "high"]:
		priority = "medium"
	
	notification = frappe.get_doc({
		"doctype": "Notification Log",
		"for_user": user_id,
		"subject": _("System Notification"),
		"email_content": message,
		"type": "Alert",
		"document_type": "User",
		"document_name": user_id
	})
	
	notification.insert(ignore_permissions=True)
	return notification.name
