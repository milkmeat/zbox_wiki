#!/usr/bin/env python
import os
import shutil
import sys


zwadmin_help_tpl = """
Usage:

    zwadmin.py create <path>
    zwadmin.py deploy <path>

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwadmin.py create <path>
    python zwadmin.py deploy <path>"

"""

def print_help():
    sys.stdout.write(zwadmin_help_tpl)


zwd_help_tpl = """
start ZBox Wiki:
    zwd.py --path %s

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwd.py --path %s

"""

def print_zwd_help(proj_root_path):
    msg = zwd_help_tpl % (proj_root_path, proj_root_path)
    sys.stdout.write(msg)


def action_create(proj_root_path):
    import zbox_wiki
    zw_path = zbox_wiki.__path__[0]

    for folder_name in ("static", "templates", "pages"):
        src_full_path = os.path.join(zw_path, folder_name)
        dst_full_path = os.path.join(proj_root_path, folder_name)

        if os.path.exists(dst_full_path):
            msg = "%s already exists, skip" % dst_full_path + "\n"
            sys.stdout.write(msg)
            continue
        shutil.copytree(src_full_path, dst_full_path)


    for folder_name in ("tmp", "sessions"):
        src_full_path = os.path.join(proj_root_path, folder_name)

        if os.path.exists(src_full_path):
            msg = "%s already exists, skip" % src_full_path + "\n"
            sys.stdout.write(msg)
            continue

        os.mkdir(src_full_path)


    conf_full_path = os.path.join(zw_path, "default_conf.py")
    dst_full_path = os.path.join(proj_root_path, "conf.py")
    if not os.path.exists(dst_full_path):
        shutil.copy(conf_full_path, dst_full_path)


    print_zwd_help(proj_root_path)


def action_deploy(proj_root_path):
    pass


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]


    if len(args) != 2:
        print_help()
    else:
        action, option = args[0], args[1]
        assert action in ("create", "deploy")

        path = option
        proj_root_path = os.path.realpath(path)

        if not os.path.exists(path):
            os.makedirs(path)

        if action == "create":
            action_create(proj_root_path)

        elif action == "deploy":
            action_deploy(proj_root_path)

        else:
            print_help()
