
def index(request):
    return {}, 'index.phtml'

def notfound(request):
    return {}, 'notfound.phtml', 404
