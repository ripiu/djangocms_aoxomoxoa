from django.conf import settings

TYPE_VIMEO = 'vimeo'
TYPE_WISTIA = ''
TYPE_YOUTUBE = 'youtube'
TYPE_HTML5 = 'html5video'


def get_video_id(url):
    """Returns Video_ID extracting from the given url

    Examples of URLs:
      Valid:
        'http://youtu.be/_lOT2p_FCvA',
        'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
        'http://www.youtube.com/embed/_lOT2p_FCvA',
        'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
        'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
        'youtube.com/watch?v=_lOT2p_FCvA',
        'https://vimeo.com/262970846',
        'https://*.wistia.com/medias/4x2dthmzyw?wvideo=4x2dthmzyw'

      Invalid:
        'youtu.be/watch?v=_lOT2p_FCvA',
    """

    from urllib.parse import urlparse, parse_qs

    if url.startswith(('youtu', 'www.youtu')):
        url = 'http://' + url
    elif url.startswith(('vimeo', 'www.vimeo')):
        url = 'https://' + url
    query = urlparse(url)

    if 'youtube' in query.hostname:
        if query.path == '/watch':
            return (TYPE_YOUTUBE, parse_qs(query.query)['v'][0])
        elif query.path.startswith(('/embed/', '/v/')):
            return (TYPE_YOUTUBE, query.path.split('/')[2])
    elif 'youtu.be' in query.hostname:
        return (TYPE_YOUTUBE, query.path[1:])
    elif 'vimeo' in query.hostname:
        return (TYPE_VIMEO, query.path[1:])
    elif 'wistia' in query.hostname:
        return (TYPE_WISTIA, parse_qs(query.query)['wvideo'][0])
    else:
        raise ValueError


def get_item_class(obj):
    from cms.plugin_pool import plugin_pool
    publishers = settings.RIPIU_AOXOMOXOA_ITEM_PUBLISHERS
    return publishers.get(
        obj.plugin_type,
        plugin_pool.get_plugin(obj.plugin_type)
    )
