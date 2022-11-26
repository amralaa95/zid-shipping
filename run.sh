#!/bin/sh
set -x


if [ "$1" = "shipment" ];
then

    echo "==================="
    echo "Running shipment"
    echo "==================="
    echo
    python manage.py migrate
    python manage.py loaddata auth.json
    python manage.py collectstatic --no-input
    python manage.py runserver 0.0.0.0:9000
fi