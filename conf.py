import os

# path
PWD = os.path.dirname(os.path.realpath(__file__))
pages_path = os.path.join(PWD, "pages")

sessions_path = os.path.join(PWD, 'sessions')
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
readonly = False


# debug
error_log = os.path.join(PWD, "error_log.txt")
info_log = os.path.join(PWD, "info_log.txt")


# bio/info
#maintenance_email = "shuge.lee@gmail.com"
maintenance_email = None
repository_url = None

if maintenance_email:
    splits = maintenance_email.split("@")
    maintenance_email_prefix = splits[0]
    maintenance_email_suffix = splits[1]