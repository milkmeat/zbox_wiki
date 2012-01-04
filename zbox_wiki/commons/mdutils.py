#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import re
import sys

try:
    import dot2png
except ImportError:
    dot2png = None
    pass

try:
    import tex2png
except ImportError:
    tex2png = None
    pass

import md_table
import markdown

__all__ = [
    "text_path2btns_path",
    "md2html",
]


def trac_wiki_code_block_to_md_code(text):
    """ This API deprecated in the future. """
    alias_p = '[a-zA-Z0-9#\-\+ \.]'
    shebang_p = '(?P<shebang_line>[\s]*#!%s{1,21}[\s]*?)' % alias_p

    code_p = '(?P<code>[^\f\v]+?)'

    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        buf = "\n    ".join(code.split(os.linesep))
        buf = "    %s" % buf
        return buf

    return code_block_p_obj.sub(code_repl, text)

def code_block_to_md_code(text):
    alias_p = '[a-zA-Z0-9#\-\+ \.]'
    shebang_p = '(?P<shebang_line>[\s]*#!%s{1,21}[\s]*?)' % alias_p

    code_p = '(?P<code>[^\f\v]+?)'

    code_block_p = "^```[\s]*%s*%s[\s]*```" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        buf = "\n    ".join(code.split(os.linesep))
        buf = "    %s" % buf
        return buf

    return code_block_p_obj.sub(code_repl, text)

def trac_wiki_tex2md(text, save_to_prefix):
    shebang_p = "#!tex"
    code_p = '(?P<code>[^\f\v]+?)'
    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        png_filename = tex2png.tex_text2png(text=code, save_to_prefix=save_to_prefix)

        return "![%s](%s)" % (png_filename, png_filename)

    return code_block_p_obj.sub(code_repl, text)

def trac_wiki_dot2md(text, save_to_prefix):
    shebang_p = "#!dot"
    code_p = '(?P<code>[^\f\v]+?)'
    code_block_p = "^\{\{\{[\s]*%s*%s[\s]*\}\}\}" % (shebang_p, code_p)
    code_block_p_obj = re.compile(code_block_p, re.MULTILINE)

    def code_repl(match_obj):
        code = match_obj.group('code')
        dst_path = dot2png.dot_text2png(text = code, png_path = save_to_prefix)
        png_filename = os.path.basename(dst_path)

        return "![%s](%s)" % (png_filename, png_filename)

    return code_block_p_obj.sub(code_repl, text)


def _fix_img_url(text, static_file_prefix = None):
    """
        >>> text = '![blah blah](20100426-400x339.png)'
        >>> static_file_prefix = '/static/files/'
        >>> _fix_img_url(text, static_file_prefix)
        '![blah blah](/static/files/20100426-400x339.png)'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group("img_alt")
        img_url = match_obj.group("img_url")
        if static_file_prefix:
            fixed_img_url = os.path.join(static_file_prefix, img_url)
            return '![%s](%s)' % (img_alt, fixed_img_url)
        else:
            return '![%s](%s)' % (img_alt, img_url)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def _fix_img_url_with_option(text, static_file_prefix = None):
    """
        >>> text = '![blah blah](20100426-400x339.png "png title")'
        >>> static_file_prefix = '/static/files/'
        >>> _fix_img_url_with_option(text, static_file_prefix)
        '![blah blah](/static/files/20100426-400x339.png "png title")'
    """
    def img_url_repl(match_obj):
        img_alt = match_obj.group('img_alt')
        img_url = match_obj.group('img_url')
        img_title = match_obj.group('img_title')
        if static_file_prefix:
            fixed_img_url = os.path.join(static_file_prefix, img_url)
            return '![%s](%s "%s")' % (img_alt, fixed_img_url, img_title)
        else:
            return '![%s](%s "%s")' % (img_alt, img_url, img_title)

    img_url_p = r"!\[(?P<img_alt>.+?)\]\((?P<img_url>[^\s]+?)\s\"(?P<img_title>.+?)\"\)"
    img_url_p_obj = re.compile(img_url_p, re.MULTILINE)
    return img_url_p_obj.sub(img_url_repl, text)

def uri2html_link(text):
    """ References:

     - http://stackoverflow.com/questions/6718633/python-regular-expression-again-match-url
     - http://daringfireball.net/2010/07/improved_regex_for_matching_urls
    """
    p = r'''(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))'''
    p_obj = re.compile(p, re.UNICODE | re.MULTILINE)

    def repl(match_obj):
        url = match_obj.groups()[0]
        return '<a href="%s">%s</a>' % (url, url)

    return p_obj.sub(repl, text)

def convert_static_file_url(text, static_file_prefix):
    text = _fix_img_url(text, static_file_prefix)
    text = _fix_img_url_with_option(text, static_file_prefix)
    return text


def path2hierarchy(path):
    """ Parse path and return hierarchy name and link pairs,
    inspired by [GNOME Nautilus](http://library.gnome.org/users/user-guide/2.32/nautilus-location-bar.html.en)
    and [Trac Wiki](http://trac.edgewall.org/browser/trunk/trac/wiki/web_ui.py) .

        >>> path = '/shugelab/users/lee'
        >>> t1 = [('shugelab', '/shugelab'), ('users', '/shugelab/users'), ('lee', '/shugelab/users/lee')]
        >>> path2hierarchy(path) == t1
        True
        >>> path2hierarchy('/') == [('index', '/~index')]
        True
    """
    caches = []

    if "/" == path:
        return [("index", "/~index")]
    elif "/" in path:
        parts = path.split('/')
        start = len(parts) - 2
        stop = -1
        step = -1
        for i in range(start, stop, step):
            name = parts[i + 1]
            links = "/%s" % "/".join(parts[1 : i + 2])
            if name == '':
                continue
            caches.append((name, links))

    caches.reverse()

    return caches

def text_path2btns_path(path):
    buf = path2hierarchy(path)
    IS_ONLY_ONE_LEVEL = len(buf) == 1
    button_path = " / ".join(["[%s](%s/)" % (i[0], i[1]) for i in buf[:-1]])

    latest_level = buf[-1]
    path_name = latest_level[0]

    if IS_ONLY_ONE_LEVEL:
        button_path = path_name
    else:
        button_path = "%s / %s" % (button_path, path_name)

    return button_path

def md2html(text, work_full_path = None, static_file_prefix = None):
    assert text != None
    buf = text    
    
    if work_full_path and tex2png:
#        buf = trac_wiki_tex2md(buf, save_to_prefix = work_full_path)
        try:
            buf = trac_wiki_tex2md(buf, save_to_prefix = work_full_path)
        except Exception:
            msg = "it seems that latex or dvipng doesn't works well on your box, or source code is invalid"
            sys.stderr.write("\n" + msg + "\n")

            buf = text

    if work_full_path and dot2png:
#        buf = trac_wiki_dot2md(buf, save_to_prefix = work_full_path)
        try:
            buf = trac_wiki_dot2md(buf, save_to_prefix = work_full_path)
        except Exception:
            msg = "it seems that graphviz doesn't works well on your box, or source code is invalid"
            sys.stderr.write("\n" + msg + "\n")

            buf = text

    if static_file_prefix:
        buf = convert_static_file_url(buf, static_file_prefix)


    buf = md_table.md_table2html(buf)
    buf = code_block_to_md_code(buf)
    buf = trac_wiki_code_block_to_md_code(buf)

    buf = markdown.markdown(buf)
    
    return buf


def test_path2hierarchy():
    for i in [
        ("/", [("index", "/~index")]), # name, link pairs

        ("/system-management/gentoo/abc",
         [("system-management", "/system-management"),("gentoo", "/system-management/gentoo"),("abc", "/system-management/gentoo/abc"),]),

        ("/programming-language",
         [("programming-language", "/programming-language"),]),

        ("/programming-language/",
         [("programming-language", "/programming-language"),]),
                                       ]:
        req_path = i[0]
        links = i[1]
        assert path2hierarchy(req_path) == links

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    test_path2hierarchy()
