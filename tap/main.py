#!/usr/bin/env python3
from tap import cfg
from tap.apt_fetch_packages import apt_fetch_packages
from tap.arg_check import arg_check
from tap.autoremove import autoremove
from tap.install import install
from tap.list import list_pkg
from tap.message import message
from tap.read_config import read_config
from tap.read_mpr_cache import read_mpr_cache
from tap.remove import remove
from tap.root_check import root_check
from tap.run_loading_function import run_loading_function
from tap.search import search
from tap.update import update
from tap.upgrade import upgrade
from tap.read_dpkg_status_file import read_dpkg_status_file

import apt_pkg


def main():
    arg_check()
    read_config()

    if cfg.operation in cfg.requires_sudo:
        root_check()

    # Generate APT cache if we're going to need it.
    if cfg.operation in cfg.requires_apt_cache:
        apt_pkg.init()

        if "--quiet" not in cfg.options:
            msg = message.info("Reading APT cache...", value_return=True, newline=False)
            cfg.apt_cache = run_loading_function(msg, apt_pkg.Cache, None)
        else:
            cfg.apt_cache = apt_pkg.Cache(None)

        cfg.apt_depcache = apt_pkg.DepCache(cfg.apt_cache)
        cfg.apt_resolver = apt_pkg.ProblemResolver(cfg.apt_depcache)
        cfg.apt_pkgman = apt_pkg.PackageManager(cfg.apt_depcache)
        cfg.apt_acquire = apt_pkg.Acquire(apt_fetch_packages())
        cfg.apt_sourcelist = apt_pkg.SourceList()
        cfg.apt_sourcelist.read_main_list()
        cfg.apt_pkgrecords = apt_pkg.PackageRecords(cfg.apt_cache)
        read_dpkg_status_file()

    # Read MPR cache if we're going to need it.
    if cfg.operation in cfg.requires_mpr_cache:
        if "--quiet" not in cfg.options:
            msg = message.info("Reading MPR cache...", value_return=True, newline=False)
            cfg.mpr_cache = run_loading_function(msg, read_mpr_cache)
        else:
            cfg.mpr_cache = read_mpr_cache()

    # Run commands.
    if cfg.operation == "install":
        install()
    elif cfg.operation == "update":
        update()
    elif cfg.operation == "upgrade":
        upgrade()
    elif cfg.operation == "remove":
        remove()
    elif cfg.operation == "autoremove":
        autoremove()
    elif cfg.operation == "search":
        search()
    elif cfg.operation == "list":
        list_pkg()
