import os
import main as main_

PWD = os.path.dirname(os.path.realpath(__file__))
proj_root_full_path = PWD

main_.fix_pages_path_symlink(proj_root_full_path)
main_.app.run()