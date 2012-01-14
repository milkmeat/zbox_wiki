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

Please report bug to shuge.lee <AT> GMail.
"""

def print_help():
    sys.stdout.write(zwadmin_help_tpl)


zwd_help_tpl = """
start ZBox Wiki:
    zwd.py --path %s

If you are using VirtualENV, try:

    cd $(dirname `which python`)
    python zwd.py --path %s


If you want to run it as daemon/WSGI:

    sudo port install nginx
    sudo cp /opt/local/etc/nginx/nginx.conf /opt/local/etc/nginx/nginx.conf.bak

    sudo cp macosx-nginx.conf /opt/local/etc/nginx/nginx.conf
    sudo nginx
    chmod +x wsgi_index.py *.sh
    sh start_wsgi.sh

    tail -f /opt/local/var/log/nginx/error.log


Please report bug to shuge.lee <AT> GMail.
"""

def print_zwd_help(proj_root_path):
    msg = zwd_help_tpl % (proj_root_path, proj_root_path)
    sys.stdout.write(msg)


wsgi_idx_tpl = """#!/usr/bin/env python
import web
import conf
import zbox_wiki

if __name__ == "__main__":
    assert conf is not None

    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    zbox_wiki.app.run()
"""

start_wsgi_sh_tpl = """#!/bin/bash

spawn-fcgi -d `pwd`  -f `pwd`/wsgi_index.py -a 127.0.0.1 -p 9001 -u www-data -g www-data -P `pwd`/pid
"""

stop_wsgi_sh_tpl = """#!/bin/bash

# Install on Mac OS X via MacPorts, sudo port install proctools
# Install on Debian/Ubuntu via APT, sudo apt-get install procps

pgrep -f `pwd`/wsgi_index.py | xargs kill -s TERM
"""

def cp_wsgi_scripts(proj_root_path):
    idx_path = os.path.join(proj_root_path, "wsgi_index.py")
    file(idx_path, "w").write(wsgi_idx_tpl)
    os.chmod(idx_path, 0774)

    start_path = os.path.join(proj_root_path, "start_wsgi.sh")
    file(start_path, "w").write(start_wsgi_sh_tpl)
    os.chmod(start_path, 0774)

    stop_path = os.path.join(proj_root_path, "stop_wsgi.sh")
    file(stop_path, "w").write(stop_wsgi_sh_tpl)
    os.chmod(stop_path, 0774)


    nginx_conf_tpl = os.path.join(proj_root_path, "pages", "zbox-wiki", "nginx.conf")
    buf = file(nginx_conf_tpl).read()
    buf = buf.replace("/path/to/zw_instance", proj_root_path)
    nginx_conf_path = os.path.join(proj_root_path, "macosx-nginx.conf")
    file(nginx_conf_path, "w").write(buf)


def action_create(proj_root_path):
    import zbox_wiki
    zw_module_full_path = zbox_wiki.__path__[0]


    for folder_name in ("static", "templates", "pages"):
        src_full_path = os.path.join(zw_module_full_path, folder_name)
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


    conf_full_path = os.path.join(zw_module_full_path, "default_conf.py")
    dst_full_path = os.path.join(proj_root_path, "conf.py")
    if not os.path.exists(dst_full_path):
        shutil.copy(conf_full_path, dst_full_path)


    cp_wsgi_scripts(proj_root_path)


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
