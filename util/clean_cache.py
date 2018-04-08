import os
import django
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from banpick.models import Seq_Cache
    all_rec = Seq_Cache.objects.all()

    for rec in all_rec:
        rec.delete()


