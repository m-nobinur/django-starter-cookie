{% if cookiecutter.cloud_provider == 'AWS' -%}
from storages.backends.s3boto3 import S3Boto3Storage

from {{ cookiecutter.project_base }}.settings.prod import MEDIAFILES_LOCATION, STATICFILES_LOCATION


class StaticRootS3Boto3Storage(S3Boto3Storage):
    location = STATICFILES_LOCATION
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = MEDIAFILES_LOCATION
    file_overwrite = False
{%- elif cookiecutter.cloud_provider == 'GCP' -%}
from storages.backends.gcloud import GoogleCloudStorage


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
{%- endif %}
