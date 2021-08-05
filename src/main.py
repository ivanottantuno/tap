#!/usr/bin/env python3

# Modules
import os
import sys
import re

from functions.split_args             import  split_args             # REMOVE AT PACKAGING
from functions.arg_check              import  arg_check              # REMOVE AT PACKAGING
from functions.install_package        import  install_package        # REMOVE AT PACKAGING
from functions.update_package         import  update_package         # REMOVE AT PACKAGING
from functions.search_package         import  search_package         # REMOVE AT PACKAGING
from functions.list_packages          import  list_packages          # REMOVE AT PACKAGING

# Variables we need to function
application_name = "tap"
application_version = "git"
mpr_url = "mpr.hunterwittenborn.com"

# Argument check
argument_list = split_args(sys.argv[1:])
arg_check_results = arg_check(argument_list, application_name, application_version)

operation = arg_check_results[0]
packages = arg_check_results[1]
argument_options = arg_check_results[2]

# Run commands
if operation == "install":
	install_package(mpr_url, packages, "installed", application_name, application_version)

elif operation == "update":
	update_package(mpr_url, application_name, application_version)

elif operation == "search":
	search_package(mpr_url, packages, application_name, application_version, argument_options)

elif operation == "list-packages":
	list_packages(argument_options)
