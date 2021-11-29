import apt_pkg

from apt_pkg import CURSTATE_INSTALLED, CURSTATE_HALF_INSTALLED, CURSTATE_HALF_CONFIGURED, CURSTATE_UNPACKED
from tap import cfg
from tap.run_transaction import _install_apt_packages
from tap.message import message

def remove():
    cfg.apt_packages = cfg.mpr_packages
    cfg.mpr_packages = []
    
    not_installed = []

    for i in cfg.apt_packages:
        try:
            cfg.apt_cache[i]
        except KeyError:
            not_installed += [i]
            continue

        if cfg.apt_cache[i].current_state in (CURSTATE_INSTALLED, CURSTATE_HALF_INSTALLED, CURSTATE_HALF_CONFIGURED, CURSTATE_UNPACKED):
            cfg.apt_depcache.mark_delete(cfg.apt_cache[i])
            cfg.apt_resolver.protect(cfg.apt_cache[i])
        else:
            not_installed += [i]

        # I (Hunter Wittenborn) can't think of any place where simply removing packages would create any kind of conflicting packages error, though I guess time will tell.
        cfg.apt_resolver.resolve()

    for i in not_installed:
        message.info(f"Package '{i}' isn't installed, so not removing.")

    _install_apt_packages()
