# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals, with_statement

import argparse
import atexit
import gettext
import io
import os
import site
import sys
import threading
import time
import traceback
from signal import SIGTERM

app = None

MAIN_DIR = os.path.abspath(os.path.realpath(os.path.expanduser(os.path.dirname(os.path.dirname(__file__)))))
PROG_DIR = os.path.abspath(os.path.realpath(os.path.expanduser(os.path.dirname(__file__))))
LOCALE_DIR = os.path.join(PROG_DIR, 'locale')
LIBS_DIR = os.path.join(PROG_DIR, 'libs')
REQS_FILE = os.path.join(MAIN_DIR, 'requirements.txt')


class Daemon(object):
    """
    Usage: subclass the Daemon class
    """

    def __init__(self, pidfile, working_dir="/"):
        self.stdin = getattr(os, 'devnull', '/dev/null')
        self.stdout = getattr(os, 'devnull', '/dev/null')
        self.stderr = getattr(os, 'devnull', '/dev/null')
        self.pidfile = pidfile
        self.working_dir = working_dir
        self.pid = None

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                os._exit(0)
        except OSError, e:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                os._exit(0)
        except OSError, e:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdin = sys.__stdin__
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)
        self.pid = os.getpid()
        file(self.pidfile, 'w+').write("%s\n" % self.pid)

    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "pidfile %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()

    def stop(self):
        """
        Stop the daemon
        """

        # Get the pid from the pidfile
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidfile %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidfile)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                self.delpid()
            else:
                sys.exit(1)


def isElevatedUser():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def isVirtualEnv():
    return hasattr(sys, 'real_prefix')


def check_requirements():
    # sickrage requires python 2.7.8+
    if sys.version_info < (2, 7, 8):
        sys.exit("Sorry, SiCKRAGE requires Python 2.7.8+")

    try:
        import OpenSSL

        v = OpenSSL.__version__
        v_needed = '0.15'

        if not v >= v_needed:
            print('OpenSSL installed but {} is needed while {} is installed. '
                  'Run `pip install -U pyopenssl`'.format(v_needed, v))
    except:
        print('OpenSSL not available, please install for better requests validation: '
              '`https://pyopenssl.readthedocs.org/en/latest/install.html`')


def version():
    # Get the version number
    with io.open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'version.txt'))) as f:
        return f.read()


def main():
    global app

    # set thread name
    threading.currentThread().setName('MAIN')

    # fix threading time bug
    time.strptime("2012", "%Y")

    # add sickrage libs path to python system path
    if not (LIBS_DIR in sys.path):
        sys.path, remainder = sys.path[:1], sys.path[1:]
        site.addsitedir(LIBS_DIR)
        sys.path.extend(remainder)

    # set system default language
    gettext.install('messages', LOCALE_DIR, unicode=1, codeset='UTF-8', names=["ngettext"])

    try:
        from sickrage.core import Core

        # main app instance
        app = Core()

        # sickrage startup options
        parser = argparse.ArgumentParser(prog='sickrage')
        parser.add_argument('-v', '--version',
                            action='version',
                            version='%(prog)s {}'.format(version()))
        parser.add_argument('-d', '--daemon',
                            action='store_true',
                            help='Run as a daemon (*NIX ONLY)')
        parser.add_argument('-q', '--quite',
                            action='store_true',
                            help='Disables logging to CONSOLE')
        parser.add_argument('-p', '--port',
                            default=0,
                            type=int,
                            help='Override default/configured port to listen on')
        parser.add_argument('--dev',
                            action='store_true',
                            help='Enable developer mode')
        parser.add_argument('--debug',
                            action='store_true',
                            help='Enable debugging')
        parser.add_argument('--datadir',
                            default=os.path.abspath(os.path.join(os.path.expanduser("~"), '.sickrage')),
                            help='Overrides data folder for database, config, cache and logs (specify full path)')
        parser.add_argument('--config',
                            default='config.ini',
                            help='Overrides config filename (specify full path and filename if outside datadir path)')
        parser.add_argument('--pidfile',
                            default='sickrage.pid',
                            help='Creates a PID file (specify full path and filename if outside datadir path)')
        parser.add_argument('--nolaunch',
                            action='store_true',
                            help='Suppress launching web browser on startup')

        # Parse startup args
        args = parser.parse_args()
        app.quite = args.quite
        app.web_port = int(args.port)
        app.no_launch = args.nolaunch
        app.developer = args.dev
        app.debug = args.debug
        app.data_dir = os.path.abspath(os.path.realpath(os.path.expanduser(args.datadir)))
        app.cache_dir = os.path.abspath(os.path.realpath(os.path.join(app.data_dir, 'cache')))
        app.config_file = args.config
        daemonize = (False, args.daemon)[not sys.platform == 'win32']
        pid_file = args.pidfile

        if not os.path.isabs(app.config_file):
            app.config_file = os.path.join(app.data_dir, app.config_file)

        if not os.path.isabs(pid_file):
            pid_file = os.path.join(app.data_dir, pid_file)

        # check lib requirements
        check_requirements()

        # add sickrage module to python system path
        if not (PROG_DIR in sys.path):
            sys.path, remainder = sys.path[:1], sys.path[1:]
            site.addsitedir(PROG_DIR)
            sys.path.extend(remainder)

        # Make sure that we can create the data dir
        if not os.access(app.data_dir, os.F_OK):
            try:
                os.makedirs(app.data_dir, 0o744)
            except os.error:
                sys.exit("Unable to create data directory '" + app.data_dir + "'")

        # Make sure we can write to the data dir
        if not os.access(app.data_dir, os.W_OK):
            sys.exit("Data directory must be writeable '" + app.data_dir + "'")

        # Make sure that we can create the cache dir
        if not os.access(app.cache_dir, os.F_OK):
            try:
                os.makedirs(app.cache_dir, 0o744)
            except os.error:
                sys.exit("Unable to create cache directory '" + app.cache_dir + "'")

        # Make sure we can write to the cache dir
        if not os.access(app.cache_dir, os.W_OK):
            sys.exit("Cache directory must be writeable '" + app.cache_dir + "'")

        # daemonize if requested
        if daemonize:
            app.no_launch = True
            app.quite = True
            app.daemon = Daemon(pid_file, app.data_dir)
            app.daemon.daemonize()
            app.pid = app.daemon.pid

        # start app
        app.start()
    except (SystemExit, KeyboardInterrupt):
        if app:
            app.shutdown()
    except ImportError:
        traceback.print_exc()
        if os.path.isfile(REQS_FILE):
            print("Failed to import required libs, please run "
                  "'pip install --user -U -r {}' from console".format(REQS_FILE))
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
