import re
import logging


req_log = logging.getLogger(__name__)


def log_cond(request):
    return re.search(r'^/(login|logout|auth)', request.path)


def simple_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        if not log_cond(request):
            keys = sorted(filter(lambda k: re.match(r'(HTTP_|CONTENT_)', k), request.META))
            keys = ['REMOTE_ADDR'] + keys
            meta = ''.join("%s=%s\n" % (k, request.META[k]) for k in keys)
            status = response.status_code
            response_headers = [(str(k), str(v)) for k, v in response.items()]
            for c in response.cookies.values():
                response_headers.append(('Set-Cookie', str(c.output(header=''))))
            headers = ''.join("%s: %s\n" % c for c in response_headers)
            req_log.info('"%s %s\n%s\n%s\n%s' % (request.method, request.build_absolute_uri(), meta, status, headers))
        return response

    return middleware
