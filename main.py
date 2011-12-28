#!/usr/bin/env python
#-*- coding:utf-8 -*-
import cgi
import functools
import os
import re
import shutil
import web

import commons
import conf

__all__ = [
    "app",
]

urls = (
    "/robots.txt", "Robots",
    "/~([a-zA-Z0-9_\-/.]+)", "SpecialWikiPage",
    ur"/([a-zA-Z0-9_\-/.%s]*)" % commons.CJK_RANGE, "WikiPage",
)

app = web.application(urls, globals())

#
# template & session
#
if not web.config.get("_session"):
    session = web.session.Session(app, web.session.DiskStore(conf.sessions_path), initializer={"username": None})
    web.config._session = session
else:
    session = web.config._session

t_globals = {
    "utils" : web.utils,
    "session" : session,
    "ctx" : web.ctx
    }
t_render = web.template.render(conf.templates_path, globals=t_globals)

def session_hook():
    web.ctx.session = session
    web.template.Template.globals["session"] = session
app.add_processor(web.loadhook(session_hook))


def _limit_ip(*args, **kwargs):
    # allow_ips = ("192.168.0.10", )
    allow_ips = None
    remote_ip = web.ctx["ip"]

    if not commons.ip_in_network_ranges(remote_ip, allow_ips):
        return False

    return True

def limit_ip(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if _limit_ip(*args, **kwargs):
            return f(*args, **kwargs)
        raise web.Forbidden()
    return wrapper


def _acl(*args, **kwargs):
    inputs = web.input()
    action = inputs.get("action", "read")

    if conf.readonly:
        if action not in ("read", "source"):
            return False

    return True


def acl(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if _acl(*args, **kwargs):
            return f(*args, **kwargs)
        raise web.Forbidden()
    return wrapper


def get_recent_change_list(limit, show_fullpath = conf.show_fullpath):
    get_rc_list_cmd = " cd %s; find . -name '*.md' | xargs ls -t | head -n %d " % \
                      (conf.pages_path, limit)
    buf = os.popen(get_rc_list_cmd).read().strip()

    if buf:
        buf = web.utils.safeunicode(buf)
        lines = buf.split("\n")
        strips_seq_item = ".md"

        if show_fullpath:
            callable_obj = None
        else:
            callable_obj = get_page_file_title

        return sequence_to_unorder_list(lines, strips_seq_item, callable_obj=callable_obj)

def get_page_file_or_dir_fullpath_by_req_path(req_path):
    if not req_path.endswith("/"):
        return "%s.md" % os.path.join(conf.pages_path, req_path)
    elif req_path == "/":
        return conf.pages_path
    else:
        return os.path.join(conf.pages_path, req_path)

def get_page_file_title(req_path):
    """
        >>> get_page_file_title('application/air/run-air-application-on-gentoo')
        'run air application on gentoo'
    """
    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
    c = commons.cat(fullpath)

    p = '^#\s(?P<title>.+?)\s$'
    p_obj = re.compile(p, re.MULTILINE)
    match_obj = p_obj.search(c)
    if match_obj:
        title = match_obj.group('title')
    elif '/' in req_path:
        title = req_path.split('/')[-1].replace('-', ' ')
    else:
        title = 'untitled'

    return title

def get_dot_idx_content_by_fullpath(fullpath):
    dot_idx_fullpath = os.path.join(fullpath, ".index.md")
    return commons.cat(dot_idx_fullpath)


def get_page_file_list_content_by_fullpath(fullpath, show_fullpath = conf.show_fullpath):
    req_path = fullpath.replace(conf.pages_path, "")
    req_path = web.utils.strips(req_path, "/")

    tree_cmd = " cd %s; find %s -name '*.md' \! -name '.index.md' " % (conf.pages_path, req_path)
    buf = os.popen(tree_cmd).read().strip()

    if buf:
        buf = web.utils.safeunicode(buf)
        lines = buf.split("\n")
        strips_seq_item = ".md"

        if show_fullpath:
            callable_obj = None
        else:
            callable_obj = get_page_file_title

        return sequence_to_unorder_list(lines = lines,
                                        strips_seq_item = strips_seq_item,
                                        callable_obj = callable_obj)

def delete_page_file_by_fullpath(fullpath):
    if os.path.isfile(fullpath):
        os.remove(fullpath)
        return True
    elif os.path.isdir(fullpath):
        idx_dot_md = os.path.join(fullpath, ".index.md")
        os.remove(idx_dot_md)
        return True
    return False

def get_page_file_index(limit=conf.index_page_limit, show_fullpath = conf.show_fullpath):
    get_page_file_index_cmd = " cd %s; find . -name '*.md' | head -n %d " % (conf.pages_path, limit)
    buf = os.popen(get_page_file_index_cmd).read().strip()
    if buf:
        buf = web.utils.safeunicode(buf)
        lines = buf.split("\n")

        if show_fullpath:
            callable_obj = None
        else:
            callable_obj = get_page_file_title

        content = sequence_to_unorder_list(lines, strips_seq_item=".md", callable_obj=callable_obj)
        return content

def sequence_to_unorder_list(lines, strips_seq_item=None, callable_obj=None):
    """
        >>> sequence_to_unorder_list(['a','b','c'])
        '- [a](/a)\\n- [b](/b)\\n- [c](/c)'
    """
    lis = []

    for i in lines:
        name = web.utils.strips(i, "./")
        if strips_seq_item:
            name = web.utils.strips(name, strips_seq_item)

        url = os.path.join("/", name)
        if callable_obj:
            name = apply(callable_obj, (name, ))
        lis.append('- [%s](%s)' % (name, url))

    content = "\n".join(lis)
    content = web.utils.safeunicode(content)

    return content

def search_by_filename_and_file_content(keywords,
                                        limit = conf.search_page_limit,
                                        show_fullpath = conf.show_fullpath):
    """
    Following doesn't works if cmd contains pipe character:

        p_obj = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        p_obj.wait()
        resp = p_obj.stdout.read().strip()

    So we have to do use deprecated syntax ```os.popen```, for more detail, see
    http://stackoverflow.com/questions/89228/how-to-call-external-command-in-python .
    """

    find_by_filename_matched = " -o -name ".join([" '*%s*' " % i for i in keywords.split()])
    find_by_content_matched = " \| ".join(keywords.split())
    is_multiple_keywords = find_by_content_matched.find("\|") != -1

    if is_multiple_keywords:
        find_by_filename_cmd = " cd %s; "\
                               " find . \( -name %s \) -type f | " \
                               " grep '.md$' | head -n %d " % \
                               (conf.pages_path, find_by_filename_matched, limit)

        find_by_content_cmd = " cd %s; " \
                              " grep ./ --recursive --ignore-case --include='*.md' --regexp ' \(%s\) ' | " \
                              " awk -F ':' '{print $1}' | uniq | head -n %d " % \
                              (conf.pages_path, find_by_content_matched, limit)
    else:
        find_by_filename_cmd = " cd %s; " \
                               " find . -name %s -type f | " \
                               " grep '.md$' | head -n %d " % \
                               (conf.pages_path, find_by_filename_matched, limit)

        find_by_content_cmd = " cd %s; " \
                              " grep ./ --recursive --ignore-case --include='*.md' --regexp '%s' | " \
                              " awk -F ':' '{print $1}' | uniq | head -n %d " % \
                              (conf.pages_path, find_by_content_matched, limit)

    # print "find_by_filename_cmd:"
    # print find_by_filename_cmd

    # print "find_by_content_cmd:"
    # print find_by_content_cmd

    matched_content_lines = os.popen(find_by_content_cmd).read().strip()
    matched_content_lines = web.utils.safeunicode(matched_content_lines)
    if matched_content_lines:
        matched_content_lines = web.utils.safeunicode(matched_content_lines)
        matched_content_lines = matched_content_lines.split("\n")

    matched_filename_lines = os.popen(find_by_filename_cmd).read().strip()
    matched_filename_lines = web.utils.safeunicode(matched_filename_lines)
    if matched_filename_lines:
        matched_filename_lines = web.utils.safeunicode(matched_filename_lines)
        matched_filename_lines = matched_filename_lines.split("\n")

    if matched_content_lines and matched_filename_lines:
        # NOTICE: build-in function set doen't keep order, we shouldn't use it.
        # mixed = set(matched_filename_lines)
        # mixed.update(set(matched_content_lines))
        mixed = web.utils.uniq(matched_filename_lines + matched_content_lines)
    elif matched_content_lines and not matched_filename_lines:
        mixed = matched_content_lines
    elif not matched_content_lines  and matched_filename_lines:
        mixed = matched_filename_lines
    else:
        return None

    lines = mixed

    if show_fullpath:
        callable_obj = None
    else:
        callable_obj = get_page_file_title

    content = sequence_to_unorder_list(lines, strips_seq_item=".md", callable_obj=callable_obj)

    return content

special_path_mapping = {
    "index" : get_page_file_index,
    "s" : search_by_filename_and_file_content,
}

def _append_static_file(buf, filepath, file_type, add_newline=False):
    assert file_type in ("css", "js")

    if file_type == "css":
        ref = '<link href="%s" rel="stylesheet" type="text/css">' % filepath
    else:
        ref = '<script type="text/javascript" src="%s"></script>' % filepath

    if not add_newline:
        static_files = "%s\n    %s" % (buf, ref)
    else:
        static_files = "%s\n\n    %s" % (buf, ref)

    return static_files

def _get_trac_wiki_theme():
    static_files = ""
    css_files = ["trac.css", "wiki.css"]

    for i in css_files:
        filepath = os.path.join("/static", "css", i)
        static_files = _append_static_file(static_files, filepath, file_type="css")

    return static_files

def get_global_static_files(show_toc = conf.show_toc,
                            show_highlight = conf.show_highlight,
                            enable_safari_reader_mode = conf.enable_safari_reader_mode,
                            use_markdown_ide = conf.use_markdown_ide):
    static_files = _get_trac_wiki_theme()

    css_files = ("main.css",)
    for i in css_files:
        path = os.path.join("/static", "css", i)
        static_files = _append_static_file(static_files, path, file_type="css")

    if enable_safari_reader_mode:
        path = os.path.join("/static", "css", "safari_reader.css")
        static_files = _append_static_file(static_files, path, file_type="css")

    if show_toc:
        path = os.path.join("/static", "css", "toc.css")
        static_files = _append_static_file(static_files, path, file_type="css")

    if show_highlight:
        path = os.path.join("/static", "js", "prettify", "prettify.css")
        static_files = _append_static_file(static_files, path, file_type="css")


    static_files = "%s\n" % static_files


    js_files = ("jquery.js", "jquery-ui.js", "main.js")
    for i in js_files:
        path = os.path.join("/static", "js", i)
        static_files = _append_static_file(static_files, path, file_type="js")

    if use_markdown_ide:
        js_files = ("Markdown.Converter.js", "Markdown.Sanitizer.js", "Markdown.Editor.js")
        for i in js_files:
            path = os.path.join("/static", "js", i)
            static_files = _append_static_file(static_files, path, file_type="js")


    if show_toc:
        path = os.path.join("/static", "js", "toc.js")
        static_files = _append_static_file(static_files, path, file_type="js")

    if show_highlight:
        js_files = (os.path.join("prettify", "prettify.js"),
                    "highlight.js")
        for i in js_files:
            path = os.path.join("/static", "js", i)
            static_files = _append_static_file(static_files, path, file_type="js")

    return static_files

def get_the_same_folders_cssjs_files(req_path):
    # NOTICE: this features doesn't works on file system mounted by sshfs.

    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
    if os.path.isfile(fullpath):
        work_path = os.path.dirname(fullpath)
        static_file_prefix = os.path.join("/static/pages", os.path.dirname(req_path))
    elif os.path.isdir(fullpath):
        work_path = fullpath
        static_file_prefix = os.path.join("/static/pages", req_path)
    else:
        # special page, such as '~index'
        work_path = conf.pages_path
        static_file_prefix = "/static/pages"

    iters = os.listdir(work_path)
    cssjs_files = [i for i in iters
                   if (not i.startswith(".")) and (i.endswith(".js") or i.endswith(".css"))]

    if not cssjs_files:
        return ""

    css_buf = ""
    js_buf = ""
    for i in cssjs_files:
        if i.endswith(".css"):
            path = os.path.join(static_file_prefix, i)
            css_buf = _append_static_file(css_buf, path, file_type="css")
        elif i.endswith(".js"):
            path = os.path.join(static_file_prefix, i)
            js_buf = _append_static_file(js_buf, path, file_type="js")

    return "%s\n    %s" % (css_buf, js_buf)

def wp_read_recent_change():
    inputs = web.input()
    limit = inputs.get("limit")

    show_fullpath = inputs.get("show_fullpath") or conf.show_fullpath
    if show_fullpath == "0":
        show_fullpath = False

    title = "Recnet Changes"
    static_file_prefix = "/static/pages"
    req_path = title

    if limit:
        limit = int(limit) or conf.index_page_limit
        content = get_recent_change_list(limit, show_fullpath=show_fullpath)
    else:
        content = get_recent_change_list(conf.index_page_limit, show_fullpath=show_fullpath)

    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
    content = commons.md2html(text = content,
                                work_fullpath = fullpath,
                                static_file_prefix = static_file_prefix)

    static_files = get_global_static_files()
    # static_files = "%s\n    %s" % (static_files, get_the_same_folders_cssjs_files(req_path))

    return t_render.canvas(conf = conf,
                           req_path = req_path,
                           title = title,
                           content = content,
                           toolbox = False,
                           static_files = static_files)

def wp_read(req_path):
    inputs = web.input()

    show_fullpath = inputs.get("show_fullpath", True)
    if show_fullpath == "0":
        show_fullpath = False

    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

    if conf.enable_button_mode_path:
        buf = commons.text_path2btns_path("/%s" % req_path)
        title = commons.md2html(buf)
    else:
        title = req_path

    if os.path.isfile(fullpath):
        work_fullpath = os.path.dirname(fullpath)
        static_file_prefix = os.path.join("/static/pages", os.path.dirname(req_path))

        content = commons.cat(fullpath)
    elif os.path.isdir(fullpath):
        work_fullpath = fullpath
        static_file_prefix = os.path.join("/static/pages", req_path)

        dot_idx_content = get_dot_idx_content_by_fullpath(fullpath)
        page_file_list_content = get_page_file_list_content_by_fullpath(fullpath,
                                                                        show_fullpath=show_fullpath)
        content = ""

        if dot_idx_content:
            content = dot_idx_content
        if page_file_list_content:
            content = "%s\n\n----\n%s" % (content, page_file_list_content)
    else:
        web.seeother("/%s?action=edit" % req_path)
        return

    content = commons.md2html(text=content,
                                       work_fullpath=work_fullpath,
                                       static_file_prefix=static_file_prefix)

    static_files = get_global_static_files()
    static_files = "%s\n    %s" % (static_files, get_the_same_folders_cssjs_files(req_path))

    return t_render.canvas(conf = conf,
                           req_path=req_path,
                           title=title,
                           content=content,
                           static_files=static_files)

def wp_edit(req_path):
    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

    if conf.enable_button_mode_path:
        buf = commons.text_path2btns_path("/%s" % req_path)
        title = commons.md2html(buf)
    else:
        title = req_path

    if os.path.isfile(fullpath):
        content = commons.cat(fullpath)
    elif os.path.isdir(fullpath):
        content = get_dot_idx_content_by_fullpath(fullpath)
    elif not os.path.exists(fullpath):
        content = ""
    else:
        raise Exception("unknow path")

    static_files = get_global_static_files(show_toc = False,
                            show_highlight = False,
                            enable_safari_reader_mode = False,
                            use_markdown_ide = conf.use_markdown_ide)

    # Markdown editor style
    path = os.path.join("/static", "css", "pagedown.css")
    static_files = _append_static_file(static_files, path, file_type="css", add_newline=True)

    path = os.path.join("/static", "js", "editor.js")
    static_files = _append_static_file(static_files, path, file_type="js", add_newline=True)

    return t_render.editor(req_path, title, content, static_files=static_files)

def wp_rename(req_path):
    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

    if not os.path.exists(fullpath):
        raise web.NotFound()

    return t_render.rename(req_path, static_files = get_global_static_files())

def wp_delete(req_path):
    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

    delete_page_file_by_fullpath(fullpath)

    web.seeother("/")
    return


def wp_source(req_path):
    fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

    if os.path.isdir(fullpath):
        web.header("Content-Type", "text/plain")
        return "this is a black hole"

    elif os.path.isfile(fullpath):
        web.header("Content-Type", "text/plain")
        return commons.cat(fullpath)

    else:
        raise web.BadRequest()


class WikiPage:
    @limit_ip
    @acl
    def GET(self, req_path):
        req_path = cgi.escape(req_path)
        inputs = web.input()
        action = inputs.get("action", "read")

        assert action in ("edit", "read", "rename", "delete", "source")

        if action == "read":
            if req_path == "":
                return wp_read_recent_change()
            else:
                return wp_read(req_path)
        elif action == "edit":
            return wp_edit(req_path)
        elif action == "rename":
            return wp_rename(req_path)
        elif action == "delete":
            return wp_delete(req_path)
        elif action == "source":
            return wp_source(req_path)

        raise web.BadRequest()

    @limit_ip
    @acl
    def POST(self, req_path):
        req_path = cgi.escape(req_path)
        inputs = web.input()
        action = inputs.get("action")

        if action and action not in ("edit", "rename"):
            raise web.BadRequest()

        content = inputs.get("content")
        content = web.utils.safestr(content)

        # NOTICE: if req_path == `users/`, fullpath will be `/path/to/users/`,
        # parent will be `/path/to/users`.

        fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)

        parent = os.path.dirname(fullpath)
        if not os.path.exists(parent):
            os.makedirs(parent)

        if action == "edit":
            if not os.path.isdir(fullpath):
                web.utils.safewrite(fullpath, content.replace("\r\n", "\n"))
            else:
                idx_dot_md_fullpath = os.path.join(fullpath, ".index.md")
                web.utils.safewrite(idx_dot_md_fullpath, content.replace("\r\n", "\n"))

            web.seeother("/%s" % req_path)
        elif action == "rename":
            new_path = inputs.get("new_path")
            if not new_path:
                raise web.BadRequest()

            old_fullpath = get_page_file_or_dir_fullpath_by_req_path(req_path)
            if os.path.isfile(old_fullpath):
                new_fullpath = get_page_file_or_dir_fullpath_by_req_path(new_path)
            elif os.path.isdir(old_fullpath):
                new_fullpath = os.path.join(conf.pages_path, new_path)
            else:
                raise Exception("unknow path")

            if os.path.exists(new_fullpath):
                err_info = "Warning: The page foobar already exists."
                return t_render.rename(req_path, err_info, static_files = get_global_static_files())

            parent = os.path.dirname(new_fullpath)
            if not os.path.exists(parent):
                os.makedirs(parent)

            shutil.move(old_fullpath, new_fullpath)

            if os.path.isfile(new_fullpath):
                web.seeother("/%s" % new_path)
            elif os.path.isdir(new_fullpath):
                web.seeother("/%s/" % new_path)

            return

        url = os.path.join("/", req_path)
        web.redirect(url)


class SpecialWikiPage:
    @limit_ip
    @acl
    def GET(self, req_path):
        f = special_path_mapping.get(req_path)

        if not f:
            raise web.NotFound()

        inputs = web.input()
        show_fullpath = inputs.get("show_fullpath") or conf.show_fullpath
        if show_fullpath == "0":
            show_fullpath = False

        limit = inputs.get("limit", conf.index_page_limit)
        if limit:
            limit = int(limit)

        if req_path == "index":
            content = get_page_file_index(limit=limit, show_fullpath=show_fullpath)
            content = commons.md2html(content)

            static_files = get_global_static_files()
            static_files = "%s\n    %s" % (static_files, get_the_same_folders_cssjs_files(req_path))

            req_path = "~index"
            title = "index"
            return t_render.canvas(conf = conf,
                                   req_path=req_path,
                                   title=title,
                                   content=content,
                                   toolbox=False,
                                   static_files=static_files)


    @limit_ip
    @acl
    def POST(self, req_path):
        f = special_path_mapping.get(req_path)
        inputs = web.input()

        if not f:
            raise web.NotFound()

        keywords = inputs.get("k")
        keywords = web.utils.safestr(keywords)

        if not keywords:
            raise web.BadRequest()

        limit = inputs.get("limit", conf.search_page_limit)
        if limit:
            limit = int(limit)

        content = search_by_filename_and_file_content(keywords, limit=limit)

        if content:
            content = commons.md2html(content)
        else:
            content = "not found matched"

        return t_render.search(keywords = keywords, content = content,
                               static_files = get_global_static_files())


class Robots:
    def GET(self):
        path = os.path.join(conf.pages_path, "robots.txt")
        content = commons.cat(path)

        web.header("Content-Type", "text/plain")
        return content

def main():
    # Notice:
    # you should remove sessions/* if you want a clean environment

    if not os.path.exists(conf.sessions_path):
        os.mkdir(conf.sessions_path)

    if not os.path.exists(conf.pages_path):
        os.mkdir(conf.pages_path)

    page_link_in_static_path = os.path.join(conf.PWD, "static", "pages")
    if not os.path.exists(page_link_in_static_path):
        os.symlink(conf.pages_path, page_link_in_static_path)

    # import sys
    # sys.stderr = file(conf.error_log, "a")
    # sys.stdout = file(conf.info_log, "a")

    web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()

if __name__ == "__main__":
    main()
