import daemon

daemon.daemonize()


import main



if __name__=='__main__':
    from flup.server import fcgi_fork as fcgi
    server=fcgi.WSGIServer(main.app.wsgifunc(), bindAddress=('0.0.0.0', 8755), minSpare=2, maxSpare=2, maxChildren=2)
    server.run()

