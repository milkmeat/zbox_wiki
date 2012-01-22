#!/usr/bin/env python
import os
import platform
import shutil
import sys


is_linux_distro = platform.linux_distribution()[0].lower()
if is_linux_distro not in ("ubuntu", "debian"):
    is_linux_distro = None
is_macosx = platform.mac_ver()[0].lower()


zwadmin_help_tpl = """
Usage:

    zwadmin.py create <path>
    zwadmin.py deploy <path>

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwadmin.py create <path>
    python zwadmin.py deploy <path>"

Please report bug to shuge.lee <AT> GMail.
"""

def print_help():
    sys.stdout.write(zwadmin_help_tpl)


zwd_ubuntu_help_tpl = """
start ZBox Wiki:
    zwd.py --path %s

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwd.py --path %s


If you want to run it as daemon/FCGI:

    sudo apt-get install nginx spawn-fcgi python-flup --no-install-recommends

    cd %s

    sudo cp nginx-debian.conf /etc/nginx/sites-available/zboxwiki
    sudo ln -sf /etc/nginx/sites-available/zboxwiki /etc/nginx/sites-enabled/zboxwiki
    sudo /etc/init.d/nginx restart

    sh start_fcgi.sh

Visit 
    http://localhost:8080

View its log:

    tail -f /var/log/nginx/error.log

Stop process:

    sh stop_fcgi.sh

Please report bug to shuge.lee <AT> GMail.
"""


zwd_macosx_help_tpl = """
start ZBox Wiki:
    zwd.py --path %s

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwd.py --path %s


If you want to run it as daemon/FCGI:

    sudo port install nginx py27-flup spawn-fcgi

    cd %s
    sudo cp /opt/local/etc/nginx/nginx.conf /opt/local/etc/nginx/nginx.conf.bak
    sudo cp nginx-macosx.conf /opt/local/etc/nginx/nginx.conf

    sudo nginx

    sh start_fcgi.sh

View its log:

    tail -f /opt/local/var/log/nginx/error.log

Please report bug to shuge.lee <AT> GMail.
"""

zwd_help_tpl = """
start ZBox Wiki:
    zwd.py --path %s

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwd.py --path %s


If you want to run it as daemon/FCGI,
visit http://webpy.org/cookbook/fastcgi-nginx for more information.

Please report bug to shuge.lee <AT> GMail.
"""

def print_zwd_help(proj_root_path):
    if is_linux_distro in ("ubuntu", "debian"):
        tpl = zwd_ubuntu_help_tpl
    elif is_macosx:
        tpl = zwd_macosx_help_tpl
    else:
        tpl = zwd_help_tpl

    msg = tpl % (proj_root_path, proj_root_path, proj_root_path)
    sys.stdout.write(msg)


def cp_fcgi_scripts(proj_root_path):
    import zbox_wiki
    zw_module_full_path = zbox_wiki.__path__[0]

    src = os.path.join(zw_module_full_path, "scripts", "fcgi_main.py")
    dst = os.path.join(proj_root_path, "fcgi_main.py")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0774)

    src = os.path.join(zw_module_full_path, "scripts", "start_fcgi.sh")
    dst = os.path.join(proj_root_path, "start_fcgi.sh")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0774)

    src = os.path.join(zw_module_full_path, "scripts", "stop_fcgi.sh")
    dst = os.path.join(proj_root_path, "stop_fcgi.sh")
    shutil.copyfile(src, dst)
    os.chmod(dst, 0774)


    if is_linux_distro or is_macosx:
        if is_linux_distro:
            conf_file_name = "nginx-debian.conf"
        else:
            conf_file_name = "nginx-macosx.conf"

        nginx_conf_tpl = os.path.join(proj_root_path, "pages", "zbox-wiki", conf_file_name)
        buf = file(nginx_conf_tpl).read()
        buf = buf.replace("/path/to/zw_instance", proj_root_path)
        nginx_conf_path = os.path.join(proj_root_path, conf_file_name)
        file(nginx_conf_path, "w").write(buf)


def action_create(proj_root_path):
    import zbox_wiki
    zw_module_full_path = zbox_wiki.__path__[0]


    for folder_name in ("static", "templates", "pages"):
        src = os.path.join(zw_module_full_path, folder_name)
        dst = os.path.join(proj_root_path, folder_name)

        if os.path.exists(dst):
            msg = "%s already exists, skip" % dst + "\n"
            sys.stdout.write(msg)
            continue
        shutil.copytree(src, dst)


    for folder_name in ("tmp", "sessions"):
        src_full_path = os.path.join(proj_root_path, folder_name)

        if os.path.exists(src_full_path):
            msg = "%s already exists, skip" % src_full_path + "\n"
            sys.stdout.write(msg)
            continue

        os.mkdir(src_full_path)


    src = os.path.join(zw_module_full_path, "default_conf.py")
    dst = os.path.join(proj_root_path, "conf.py")
    if os.path.exists(dst):
        msg = "%s already exists, skip" % dst_full_path + "\n"
        sys.stdout.write(msg)        
    else:
        shutil.copyfile(src, dst)


    cp_fcgi_scripts(proj_root_path)

    print_zwd_help(proj_root_path)


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]


    if len(args) != 2:
        print_help()
    else:
        action, option = args[0], args[1]
        assert action in ("create", )

        path = option
        proj_root_path = os.path.realpath(path)

        if not os.path.exists(path):
            os.makedirs(path)

        if action == "create":
            action_create(proj_root_path)

        else:
            print_help()
