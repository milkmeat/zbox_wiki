import os
osp = os.path

PWD = osp.dirname(osp.realpath(__file__))
pages_path = osp.join(PWD, "pages")

sessions_path = osp.join(PWD, 'sessions')
templates_path = osp.join(PWD, "templates")

index_page_limit = 50
search_page_limit = 100

show_fullpath = False
show_toc = True
show_highlight = True

enable_button_mode_path = True
enable_safari_reader_mode = True

error_log = os.path.join(PWD, "error_log.txt")
info_log = os.path.join(PWD, "info_log.txt")
