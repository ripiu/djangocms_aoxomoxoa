import types

from django.conf import settings

from .utils import TYPE_HTML5, get_video_id, get_item_class

item_publishers = {}


if 'cmsplugin_filer_image' in settings.INSTALLED_APPS:
    from cmsplugin_filer_image.cms_plugins import FilerImagePlugin

    class FilerImagePluginItemPublisher(FilerImagePlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/picture.html'

        def get_render_template(self, context, instance, placeholder):
            return self.render_template

        def render(self, context, instance, placeholder):
            context.update({
                'picture': instance.image,
                'external_picture': instance.image_url,
                'alt_text':
                    instance.alt_text or instance.image.default_alt_text,
                'caption_text':
                    instance.caption_text or instance.image.default_caption,
            })
            return context

    item_publishers.update({
        'FilerImagePlugin': FilerImagePluginItemPublisher,
    })


if 'djangocms_picture' in settings.INSTALLED_APPS:
    from djangocms_picture.cms_plugins import PicturePlugin

    class PicturePluginItemPublisher(PicturePlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/picture.html'

        def get_render_template(self, context, instance, placeholder):
            return self.render_template

        def render(self, context, instance, placeholder):
            print(instance.picture)
            if 'alt' in instance.attributes and instance.attributes['alt']:
                alt_text = instance.attributes['alt']
            else:
                alt_text = instance.picture.default_alt_text
            context.update({
                'picture': instance.picture,
                'external_picture': instance.external_picture,
                'alt_text': alt_text,
                'caption_text':
                    instance.caption_text or instance.picture.default_caption,
            })
            return context

    item_publishers.update({
        'PicturePlugin': PicturePluginItemPublisher,
    })

if 'djangocms_vimeo' in settings.INSTALLED_APPS:
    from django.conf import settings
    from djangocms_vimeo.cms_plugins import VimeoVideoPlugin

    class VimeoVideoPluginItemPublisher(VimeoVideoPlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/media.html'

        def render(self, context, instance, placeholder):
            media_type, video_id = get_video_id(instance.movie_url)
            context.update({
                'instance': instance,
                'placeholder': placeholder,
                'alt_text': 'Vimeo video',
                'media_type': media_type,
                'video_id': video_id,
            })
            return context

    item_publishers.update({
        'VimeoVideoPlugin': VimeoVideoPluginItemPublisher,
    })

if 'djangocms_video' in settings.INSTALLED_APPS:
    from django.conf import settings
    from djangocms_video.cms_plugins import (
        VideoPlayerPlugin,
        VideoSourcePlugin,
        VideoTrackPlugin,
    )

    class VideoPlayerPluginItemPublisher(VideoPlayerPlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/media.html'

        def get_render_template(self, context, instance, placeholder):
            return self.render_template

        def render(self, context, instance, placeholder):
            if instance.embed_link:
                media_type, video_id = get_video_id(instance.embed_link)
            else:
                media_type, video_id = (TYPE_HTML5, None)
            sources = [{
                'type': source.source_file.extension,
                'url': source.source_file.url
            } for source in instance.child_plugin_instances
              if source.__class__.__name__ == 'VideoSource']
            for child in instance.child_plugin_instances:
                child.get_plugin_class = types.MethodType(
                    get_item_class,
                    child
                )
            context.update({
                'instance': instance,
                'placeholder': placeholder,
                'picture': instance.poster,
                'alt_text': instance.label,
                'caption_text': None,
                'media_type': media_type,
                'video_id': video_id,
                'sources': sources,
            })
            return context

    class VideoTrackPluginItemPublisher(VideoTrackPlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/empty.html'

        def get_render_template(self, context, instance, placeholder):
            return self.render_template

    class VideoSourcePluginItemPublisher(VideoSourcePlugin):
        render_template = 'ripiu/djangocms_aoxomoxoa/empty.html'

        def get_render_template(self, context, instance, placeholder):
            return self.render_template

    item_publishers.update({
        'VideoPlayerPlugin': VideoPlayerPluginItemPublisher,
        'VideoTrackPlugin': VideoTrackPluginItemPublisher,
        'VideoSourcePlugin': VideoSourcePluginItemPublisher,
    })
