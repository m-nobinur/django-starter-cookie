#! bin/bash
#
# To use function, source this file:.
# RUN: source ./utils/scripts/clean_media.sh
#

function clean_media(){
    # Description:
    #   Clean the media files.
    #
    # Usage:
    #   clean_media
    #
    # Returns:
    #   0 - Success
    #   1 - Failure
    #

    root_dir=$(pwd)

    if [ ! "$(ls -A $root_dir/media)" ]; then
        echo "The media directory is already empty."
        return 0
    fi

    for dir in $root_dir/media/*; do
    set -- "$@" "$dir"
    done

    rm -rf "$@"

    touch $root_dir/media/.gitkeep

}
