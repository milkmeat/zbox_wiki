import os

debug = True

# path
PWD = os.path.dirname(os.path.realpath(__file__))
pages_path = os.path.join(PWD, "pages")

static_path = os.path.join(PWD, "static")
sessions_path = os.path.join(PWD, 'sessions')
tmp_path = os.path.join(PWD, "tmp")
templates_path = os.path.join(PWD, "templates")


# pagination
index_page_limit = 50
search_page_limit = 100


# UI functions 
show_full_path = False
auto_toc = True
highlight = True

button_mode_path = True
reader_mode = True


# ACL
readonly = True


# debug
#error_log = os.path.join(PWD, "error_log.txt")
#info_log = os.path.join(PWD, "info_log.txt")


# bio/info
maintainer_email = "shuge.lee@gmail.com"
repository_url = "git://github.com/shuge/zbox_wiki.git"

if maintainer_email:
    splits = maintainer_email.split("@")
    maintainer_email_prefix = splits[0]
    maintainer_email_suffix = splits[1]