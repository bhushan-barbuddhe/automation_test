"""
Utility functions for the test module.
"""

import frappe
from datetime import datetime, timedelta


def get_current_timestamp():
	"""Get current timestamp in ISO format."""
	return datetime.now().isoformat()


def format_date(date_obj, format_str="%Y-%m-%d"):
	"""Format date object to string."""
	if isinstance(date_obj, str):
		return date_obj
	return date_obj.strftime(format_str)


def calculate_days_difference(start_date, end_date):
	"""Calculate difference in days between two dates."""
	if isinstance(start_date, str):
		start_date = datetime.fromisoformat(start_date)
	if isinstance(end_date, str):
		end_date = datetime.fromisoformat(end_date)
	
	return (end_date - start_date).days


class DataProcessor:
	"""Simple data processor class."""
	
	def __init__(self):
		self.processed_count = 0
	
	def process_item(self, item):
		"""Process a single item."""
		self.processed_count += 1
		return {
			"processed_at": get_current_timestamp(),
			"data": item,
			"id": self.processed_count
		}
	
	def get_stats(self):
		"""Get processing statistics."""
		return {
			"total_processed": self.processed_count,
			"last_processed_at": get_current_timestamp()
		}
