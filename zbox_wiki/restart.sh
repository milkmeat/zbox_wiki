kill -9 `ps -ef | grep launchWiki.py  | grep -v grep | awk '{print \$2}'`  
rm -f *.pyc
python launchWiki.py
