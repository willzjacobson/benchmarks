
Instructions for using add_config_sections.py
---------------------------------------------

This module can be used to add new sections for building, tenant or the default section to the forecasting configuration file, config.ini.

Usage: $python add_config_sections.py <points_list> <config file> [<building_xml> [<tenant_xml> [default_section_xml]]]

	1. points_list  : Excel file for the building for which the configuration is being modified
	
	2. config_file  : Config file to modify
	
	3. building_xml : XML file with details of settings needed for a building
	
	4. tenant_xml   : XML file with details of settings needed for a tenant
	
	5. default_section_xml : XML file with details of settings needed for the DEFAULT section of the config file.
			The DEFAULT section is set of settings common to all building/tenants in the

Default XML files are available for building, tenant and default sections.


WARNING:
-------
It is recommended that a backup copy of the existing configuration file be kept at hand before using the program.
The program will read in the configuration file and re-write it with new/updated settings/sections removing comments and or formatting in the process.

Key features:
-------------

1. Reads in as many settings as possible from the points list automatically.

2. Creates as many TPO output tables as possible.

3. Prompts user for settings that it is unable to set on its own

4. Enables user to skip creating sections. This may be useful if updated were made to the points like like a new tenant was added

5. Warns user if the section name specified is in use.


Limitations:
------------

1. Sections can't be partially updated at this time.

2. Alarm codes or sig codes may not be set correctly if building and tenats of the building are not added in the same run.