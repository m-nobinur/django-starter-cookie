#! /bin/bash
#
# To use function, source this file:.
# RUN: source ./utils/scripts/migrate_n_run.sh
#

function mgrun() {
    # Description:
    #   Migrate the database and run the application.
    #
    # Usage:
    #   mgrun
    #
    # Returns:
    #   0 - Success
    #   1 - Failure
    #

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
}
