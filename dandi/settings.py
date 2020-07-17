import logging
from pathlib import Path
from typing import Type

from configurations import values
from django_girders.configuration import (
    ComposedConfiguration,
    ConfigMixin,
    DevelopmentBaseConfiguration,
    HerokuProductionBaseConfiguration,
    ProductionBaseConfiguration,
)


class SentryConfig(ConfigMixin):
    SENTRY_DSN = values.Value(environ_required=True)

    @staticmethod
    def after_binding(configuration: Type[ComposedConfiguration]) -> None:
        import sentry_sdk
        from sentry_sdk.integrations.celery import CeleryIntegration
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration

        sentry_sdk.init(
            dsn=configuration.SENTRY_DSN,
            integrations=[
                DjangoIntegration(),
                CeleryIntegration(),
                LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
            ],
            send_default_pii=True,
        )


class DandiConfig(ConfigMixin):
    WSGI_APPLICATION = 'dandi.wsgi.application'
    ROOT_URLCONF = 'dandi.urls'

    BASE_DIR = str(Path(__file__).absolute().parent.parent)

    @staticmethod
    def before_binding(configuration: Type[ComposedConfiguration]):
        configuration.INSTALLED_APPS += ['publish.apps.PublishConfig']

    DANDI_DANDISETS_BUCKET_NAME = values.Value(environ_required=True)
    DANDI_GIRDER_API_URL = values.URLValue(environ_required=True)
    DANDI_GIRDER_API_KEY = values.Value(environ_required=True)


class DevelopmentConfiguration(DandiConfig, DevelopmentBaseConfiguration):
    pass


class ProductionConfiguration(DandiConfig, SentryConfig, ProductionBaseConfiguration):
    pass


class HerokuProductionConfiguration(DandiConfig, SentryConfig, HerokuProductionBaseConfiguration):
    pass
