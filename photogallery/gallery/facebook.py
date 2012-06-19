import ptah
import requests
from pyramid.compat import url_encode, urlparse
from pyramid.httpexceptions import HTTPBadRequest

from .user import User
from .settings import CFG_ID_AUTH

close = """<html><body>
<script>setTimeout(function(){window.close()}, 200)</script></body></html>"""


def facebook_process(request):
    """Process the facebook redirect"""
    print request.GET

    # get session
    st = request.GET.get('state').split(',')[-1]
    manager = ptah.sockjs.get_session_manager(request.registry)
    try:
        session = manager.get(st)
    except:
        raise HTTPBadRequest("No session")

    code = request.GET.get('code')
    if not code:
        raise HTTPBadRequest("No reason")

    # auth
    cfg = ptah.get_settings(CFG_ID_AUTH, request.registry)

    client_id = cfg['facebook_id']
    client_secret = cfg['facebook_secret']

    # Now retrieve the access token with the code
    access_url = '{0}?{1}'.format(
        'https://graph.facebook.com/oauth/access_token',
        url_encode({'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': request.route_url('facebook_process'),
                    'code': code}))

    r = requests.get(access_url)
    if r.status_code != 200:
        raise HTTPBadRequest("Status %s: %s" % (r.status_code, r.content))

    access_token = urlparse.parse_qs(r.content)['access_token'][0]

    with ptah.sa_session() as sa:
        user = User.get_bytoken(access_token)
        if user is not None:
            protocol = session.protocols.get('gallery')
            protocol.auth(user)
            
            response = request.response
            response.content_type = 'text/html'
            response.body = close
            return response

    # Retrieve profile data
    graph_url = '{0}?{1}'.format('https://graph.facebook.com/me',
                                 url_encode({'access_token': access_token}))
    r = requests.get(graph_url)
    if r.status_code != 200:
        raise HTTPBadRequest("Status %s: %s" % (r.status_code, r.content))

    profile = ptah.json.loads(r.content)

    id = profile['id']
    name = profile['name']
    email = profile.get('email','').lower()

    with ptah.sa_session() as sa:
        sa.query(User).filter(User.email == email).delete()

        user = User(
            token = access_token,
            source = 'facebook',
            name = name, email = email)
        sa.add(user)
        sa.flush()

        protocol = session.protocols.get('gallery')
        protocol.auth(user)

        response = request.response
        response.content_type = 'text/html'
        response.body = close
        return response
