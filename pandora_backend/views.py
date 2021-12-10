from django.shortcuts import render
from django.db import connections
from django.db.utils import OperationalError

from pandora_backend.celery import check_status


def index_view(request):
    from django.db import connections
    from django.db.utils import OperationalError
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
    except OperationalError:
        postgresql_status_msg = 'PostgreSQL: status DOWN'
    else:
        postgresql_status_msg = 'PostgreSQL: status ok'

    context = {
        'postgresql_status': postgresql_status_msg,
        'celery_status': 'None', # TODO back this state check_status(),
    }
    return render(request, template_name='backend/index.html', context=context)