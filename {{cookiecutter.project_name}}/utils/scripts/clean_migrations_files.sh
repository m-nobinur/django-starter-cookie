#! /bin/bash
#
# To use function, source this file:.
# RUN: source ./utils/scripts/clean_migrations_files.sh
#

. ./utils/scripts/clean_media.sh

function clean_mgs(){
    # Description:
    #   Clean the migrations files.
    #
    # Usage:
    #   clean_mgs
    #
    # Returns:
    #   0 - Success
    #   1 - Failure
    #

    root_dir=$(pwd)

    find $root_dir -path "*/migrations/*.py" -not -name "__init__.py" -delete
    find $root_dir -path "*/*/migrations/*.py" -not -name "__init__.py" -delete
    find $root_dir -path "*/migrations/*.pyc"  -delete
    find $root_dir -path "*/*/migrations/*.pyc"  -delete

    find $root_dir -path "*/db.sqlite3" -delete

    clean_media

    DJANGO_SUPERUSER_PASSWORD="admin"
    export DJANGO_SUPERUSER_PASSWORD


    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser --noinput --email a@m.com
}
