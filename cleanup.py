# -*- coding: utf-8 -*-
import os
import re

def get_icons_from_xml_text(filepath):
	icons = set()
	try:
		with open(filepath, 'r', encoding='utf-8') as f:
			content = f.read()
		
		# Finds all icon="values", regardless of whether they are commented out
		found = re.findall(r'icon="([^"]+)"', content)
		for icon in found:
			icons.add(f"{icon.lower()}.png")
				
	except Exception as e:
		print(f"Error: {filepath}: {e}")
		
	return icons

def clean_directory(directory_path, allowed_icons):
	if not os.path.exists(directory_path):
		print(f"Path not found: {directory_path}")
		return 0, 0

	deleted = 0
	kept = 0
	
	for filename in os.listdir(directory_path):
		if filename.lower().endswith(".png"):
			if filename.lower() in allowed_icons:
				kept += 1
			else:
				file_path = os.path.join(directory_path, filename)
				try:
					os.remove(file_path)
					print(f"Deleted in {os.path.basename(directory_path)}: {filename}")
					deleted += 1
				except Exception as e:
					print(f"Error: {filename}: {e}")
	return deleted, kept

def clean_icons():
	current_dir = os.path.dirname(os.path.abspath(__file__))
	
	all_allowed_icons = set()
	xml_files_found = []
	
	for filename in os.listdir(current_dir):
		if filename.startswith("additions") and filename.endswith(".xml"):
			xml_files_found.append(filename)
			file_path = os.path.join(current_dir, filename)
			print(f"Reading (including comments): {filename}")
			
			icons_from_file = get_icons_from_xml_text(file_path)
			all_allowed_icons.update(icons_from_file)

	if not xml_files_found:
		print("No additions*.xml files found in directory.")
		return

	if not all_allowed_icons:
		print("No icons found in XML files. Aborting.")
		return

	print(f"Found icon names: {len(all_allowed_icons)}")
	print("-" * 30)

	total_deleted = 0
	total_kept = 0

	for sub_dir in ["icons", "logos"]:
		target_path = os.path.join(current_dir, sub_dir)
		print(f"Cleaning directory: {sub_dir}")
		d, k = clean_directory(target_path, all_allowed_icons)
		total_deleted += d
		total_kept += k

	print("-" * 30)
	print(f"Sources: {len(xml_files_found)}")
	print(f"Total kept:    {total_kept}")
	print(f"Total deleted: {total_deleted}")

if __name__ == "__main__":
	clean_icons()