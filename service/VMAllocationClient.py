import sys
import json
import urllib2

SERVER_BASE_URL='http://gtnklcloud1.klrdc.gtn'

def allocate(base_image, expires, comment):
    data = { 'base_image': base_image, 'expires': expires, 'comment': comment }
    data_str = json.dumps(data)
    o = urllib2.urlopen(SERVER_BASE_URL + '/allocate', data_str)
    rep_str = o.read()
    rep = json.loads(rep_str)
    return rep

def deallocate(image_id):
    data = { 'image_id': image_id }
    data_str = json.dumps(data)
    o = urllib2.urlopen(SERVER_BASE_URL + '/deallocate', data_str)
    rep_str = o.read()
    rep = json.loads(rep_str)
    return rep

def status(image_id):
    data = { 'image_id': image_id }
    data_str = json.dumps(data)
    o = urllib2.urlopen(SERVER_BASE_URL + '/status', data_str)
    rep_str = o.read()
    rep = json.loads(rep_str)
    return rep

def usage():
    print "Usage: %s <command> <arguments..>" % sys.argv[0]
    print " %s allocate <base_image> [<expiry>] [<comment>]" % sys.argv[0]
    print " %s deallocate <image_id>" % sys.argv[0]
    print " %s status <image_id>" % sys.argv[0]
    
if __name__ == '__main__':
    ret = None
    arglen = len(sys.argv)
    if arglen < 2:
        print "Too few arguments!"
        usage()
        sys.exit(-1)
    command = sys.argv[1]
    if command == 'allocate':
        base_image = None
        expires = 3600
        comment = ''
        if arglen < 3:
            print "Missing base image!"
            usage()
            sys.exit(-1)
        base_image = sys.argv[2]
        if arglen > 3:
            expires = int(sys.argv[3])
        if arglen > 4:
            comment = sys.argv[3]
        ret = allocate(base_image, expires, comment)
        print json.dumps(ret, indent=4)
    elif command == 'deallocate':
        image_id = None
        if arglen < 3:
            print "Missing image id!"
            usage()
            sys.exit(-1)
        image_id = sys.argv[2]
        ret = deallocate(image_id)
        print json.dumps(ret, indent=4)
    elif command == 'status':
        image_id = None
        if arglen < 3:
            print "Missing image id!"
            usage()
            sys.exit(-1)
        image_id = sys.argv[2]
        ret = status(image_id)
        print json.dumps(ret, indent=4)
    else:
        print "Unknown command"
        usage()
        sys.exit(-1)