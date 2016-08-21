import re
import time


class ProcessTimeMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        start = time.time()
        response = view_func(request, *view_args, **view_kwargs)
        total_time = time.time() - start
        STATS = {
            'total_time': total_time
        }
        if response and response.content:
            s = response.content
            regexp = re.compile(r'(?P<cmt><!--\s*STATS:(?P<fmt>.*?)ENDSTATS\s*-->)')
            match = regexp.search(s)
            if match:
                s = (
                    s[:match.start('cmt')]
                    + match.group('fmt') % STATS
                    + s[match.end('cmt'):])
                response.content = s
        return response
