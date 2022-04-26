from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        # import signal handlers
        import images.signals

"""
You import the signals for this application in the ready() method so that they are
imported when the images application is loaded.
"""
