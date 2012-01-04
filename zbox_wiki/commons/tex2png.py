#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script is inspire by Trac LatexMacro.

This script requires

 * latex
 * dvipng

"""
import os
import shutil
import tempfile
import sys

__all__ = [
    "tex_text2png"
]


DEBUG = False


TEX_PREAMBLE = r'''
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\pagestyle{empty}
\begin{document}
\begin{equation*}
'''

TEX_END = r'''
\end{equation*}
\end{document}
'''

def tex_text2png(text, save_to_prefix):
    text = text.strip()

    filename = str(hash(text)).replace("-", "")
    fullname = filename + ".png"
    png_full_path = os.path.join(save_to_prefix, fullname)

    if os.path.exists(png_full_path):
        return fullname

#    print "generating ..."
    
    tex_work_full_path = tempfile.mkdtemp(prefix="latex_")
    tex_full_path = os.path.join(tex_work_full_path, filename + ".tex")

    f = open(tex_full_path, "w+")
    tex_tpl = "%s\n%s\n%s" % (TEX_PREAMBLE, text, TEX_END)
    f.write(tex_tpl)
    f.close()


    compile_cmd = 'latex -output-directory %s -interaction nonstopmode %s ' % \
                  (tex_work_full_path, tex_full_path)

    if DEBUG:
        msg = compile_cmd
        sys.stdout.write("\n" + msg + "\n")
    else:
        disabled_debug_ouptut = " > /dev/null 2>/dev/null"        
        compile_cmd += disabled_debug_ouptut
        
    assert os.system(compile_cmd) == 256


    dvi_full_path = os.path.join(tex_work_full_path, filename + ".dvi")
    compile_cmd = "dvipng -T tight -x 1200 -z 0 -bg Transparent -o %s %s " % \
                     (png_full_path, dvi_full_path)

    if DEBUG:
        msg = compile_cmd
        sys.stdout.write("\n" + msg + "\n")
    else:
        disabled_debug_ouptut = " 2>/dev/null 1>/dev/null"
        compile_cmd += disabled_debug_ouptut
        
    assert os.system(compile_cmd) == 0

    shutil.rmtree(tex_work_full_path)

    return fullname


if __name__ == "__main__":
    save_to_prefix = "/tmp/zbox_wiki_tex_demo"
    if not os.path.exists(save_to_prefix):
        os.makedirs(save_to_prefix)

    test_text = "\n$\x0crac{\x07lpha^{\x08eta^2}}{\\delta + \x07lpha}$\n"
    filename = tex_text2png(text = test_text, save_to_prefix = save_to_prefix)

    dst_path = os.path.join(save_to_prefix, filename)
    msg = "save to: " + dst_path
    print msg
