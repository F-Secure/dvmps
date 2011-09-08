from wsgiref.simple_server import make_server
import VMAllocationService
import json

vma = None

def vm_allocator_app(environ, start_response):
    command = environ['PATH_INFO']

    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    start_response(status, headers)

    res = None
    request_params = None

    if vma is not None and environ['REQUEST_METHOD'] == 'POST' and environ.has_key('CONTENT_LENGTH'):
        data_size = int(environ['CONTENT_LENGTH'])
        data = environ['wsgi.input'].read(data_size)
        request_params = json.loads(data)

        if command == '/allocate':
            base_image = None
            expires = None
            comment = None
            if request_params.has_key('base_image'):
                base_image = request_params['base_image']
            if request_params.has_key('expires'):
                expires = request_params['expires']
            if request_params.has_key('comment'):
                comment = request_params['comment']
            if base_image is not None and expires is not None:
                res = vma.allocate_image(base_image, expires, comment)
        elif command == '/deallocate':
            image_id = None
            if request_params.has_key('image_id'):
                image_id = request_params['image_id']
            if image_id is not None:
                res = vma.deallocate_image(image_id)
        elif command == '/status':
            image_id = None
            if request_params.has_key('image_id'):
                image_id = request_params['image_id']
            if image_id is not None:
                res = vma.image_status(image_id)
        elif command == '/systemstatus':
            res = vma.status()
    else:
        if vma is not None:
            res = vma.find_ip_for_mac('00:aa:ee:00:ee:cb')
    return [json.dumps(res)]

if __name__ == '__main__':
    vma = VMAllocationService.VMAllocationService()
#    vma.define_mac_ip_pair('00:aa:ee:00:ee:c8', '10.70.180.200')
#    vma.define_mac_ip_pair('00:aa:ee:00:ee:c9', '10.70.180.201')
#    vma.define_mac_ip_pair('00:aa:ee:00:ee:ca', '10.70.180.202')
#    vma.define_mac_ip_pair('00:aa:ee:00:ee:cb', '10.70.180.203')
#    vma.define_mac_ip_pair('00:aa:ee:00:ee:cc', '10.70.180.204')
    vma.define_mac_ip_pair('00:aa:ee:85:0d:ab', '10.133.13.171')
    vma.define_mac_ip_pair('00:aa:ee:85:0d:ac', '10.133.13.172')
    vma.define_mac_ip_pair('00:aa:ee:85:0d:ad', '10.133.13.173')

    vma.define_base_image('noushe-linux', '/var/lib/libvirt/qemu/templates/template-noushe-linux-test2.xml', '/var/lib/libvirt/images/base/noushe-linux-test2.qcow2')
#    vma.define_base_image('noushe-winxp', '/var/lib/libvirt/qemu/templates/template-noushe-winxp.xml', '/var/lib/libvirt/images/base/noushe-winxp.qcow2')

    httpd = make_server('', 80, vm_allocator_app)
    print "Serving on port 80..."

    # Serve until process is killed
    httpd.serve_forever()