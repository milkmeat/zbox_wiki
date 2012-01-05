#!/usr/bin/env python
import os
import argparse
import sys


parser = argparse.ArgumentParser(description = "run ZBox Wiki instance")
parser.add_argument("--ip", help = "the IP address to bind to")
parser.add_argument("--port", type = int, help = "the port number to bind to")
parser.add_argument("--path", help = "instance full path")


def run_instance():
    args = parser.parse_args()

    if not args.path:
        parser.print_help()
        exit(0)

    proj_root_full_path = os.path.realpath(args.path)
    port = args.port or 8080
    ip = args.ip or "0.0.0.0"

    # custom web.py listen IP address and port
    # http://jarln.net/archives/972
    script_name = sys.argv[0]
    listen_ip_port = "%s:%d" % (ip, port)
    fake_argv = [script_name, listen_ip_port]
    sys.argv = fake_argv


    sys.path.insert(0, proj_root_full_path)
    import conf


    src_full_path = os.path.join(proj_root_full_path, "pages")
    dst_full_path = os.path.join(proj_root_full_path, "static", "pages")

    # remove invalid symlink
    dst_real_full_path = os.path.realpath(dst_full_path)
    if os.path.exists(dst_full_path) and not os.path.exists(dst_real_full_path):
        os.remove(dst_full_path)

    if not os.path.exists(dst_full_path):
        os.symlink(src_full_path, dst_full_path)

    
    import zbox_wiki
    zbox_wiki.start()

if __name__ == "__main__":
    run_instance()
