#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This script based on [LatexMacro] [latex_macro]

Requirements:

 - [latex] [latex]
 - [dvipng] [dvipng]


[latex_macro]: http://trac-hacks.org/wiki/LatexMacro
[latex]: http://www.tug.org/texlive
[dvipng]: http://savannah.nongnu.org/projects/dvipng

"""

import hashlib
import os
import shutil
import tempfile

__all__ = [
    "latex2png"
]


tex_preamble = r'''
\documentclass{article}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amssymb}
\pagestyle{empty}
\begin{document}
\begin{equation*}
'''

tex_end = r'''
\end{equation*}
\end{document}
'''

def latex2png(text, save_to_prefix):
    if not text:
        return None

    filename = hashlib.md5(text).hexdigest()
    fullpath = os.path.join(save_to_prefix, filename)
    output_png_fullpath = os.path.join(save_to_prefix, "%s.png" % filename)

    if not os.access(fullpath, os.F_OK):
        tex_work_fullpath = tempfile.mkdtemp(prefix="latex_")        
        tex_fullpath = os.path.join(tex_work_fullpath, "foo.tex")

        f = open(tex_fullpath, "w+")
        tex_tpl = "%s\n%s\n%s" % (tex_preamble, text, tex_end)
        f.write(tex_tpl)
        f.close()

        # compile LaTeX document file to a DVI file
        compile_cmd = 'latex -output-directory %s -interaction nonstopmode %s >/dev/null 2>/dev/null' % \
                      (tex_work_fullpath, tex_fullpath)
        print "compile_cmd:", compile_cmd
        ret = os.system(compile_cmd)
        assert ret == 256
        
        dvi_fullpath = os.path.join(tex_work_fullpath, "foo.dvi")
        
        dvi_to_png_cmd = "dvipng -T tight -x 1200 -z 0 -bg Transparent -o %s %s 2>/dev/null 1>/dev/null" % \
                         (output_png_fullpath, dvi_fullpath)
        print "dvi_to_png_cmd:", dvi_to_png_cmd
        ret = os.system(dvi_to_png_cmd)
        assert ret == 0

        shutil.rmtree(tex_work_fullpath)

    return "%s.png" % filename


if __name__ == "__main__":
    save_to_prefix = "/tmp/latex2png"
    if not os.path.exists(save_to_prefix):
        os.makedirs(save_to_prefix)

    text = '\n$\x0crac{\x07lpha^{\x08eta^2}}{\\delta + \x07lpha}$\n'
    filename = latex2png(text=text, save_to_prefix=save_to_prefix)

    dst_path = os.path.join(save_to_prefix, filename)
    print "save_to:", dst_path
