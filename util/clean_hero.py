import os
import django
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import Hero
    all_rec = Hero.objects.all()

    for rec in all_rec:
        rec.delete()

    from banpick.models import Hero
    all_rec = Hero.objects.all()

    for rec in all_rec:
        rec.delete()


