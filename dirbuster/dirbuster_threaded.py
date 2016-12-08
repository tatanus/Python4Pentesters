#!/usr/bin/env python

# Original code borrowed from: https://github.com/showmehow/pypwn/blob/master/dirbuster.py
# Modified by: Adam Compton

import sys
import urllib2
import ssl
import thread

def test_dir(url, depth, max_depth, dir_list):
    if (depth > max_depth):
        return
    depth = depth +1

    for d in dir_list:
        new_url = url + "/" + d
        try:
            # make a SSL handler that ignores SSL CERT issues
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            response = urllib2.urlopen(new_url, context=ctx)
            if response and response.getcode() == 200:
                print "[+] FOUND %s" % (new_url)
                thread.start_new_thread(test_dir, (new_url, depth, max_depth, dir_list, ))
        except urllib2.HTTPError, e:
            if e.code == 401:
                print "[!] Authorization Required %s " % (new_url)
            elif e.code == 403:
                print "[!] Forbidden %s " % (new_url)
            elif e.code == 404:
                print "[-] Not Found %s " % (new_url)
            elif e.code == 503:
                print "[!] Service Unavailable %s " % (new_url)
            else:
                print "[?] Unknwon"

def load_file(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    def usage():
        print "%s <url> <depth> <dirlist filename>" % (sys.argv[0])
    if len(sys.argv) <> 4:
        usage()
        sys.exit(0)

    url = sys.argv[1]
    depth = int(sys.argv[2])
    dir_file = sys.argv[3]

    dir_list = load_file(dir_file)

    test_dir(url, 0, depth, dir_list)

    print "\n Max Depth Reached \n"
