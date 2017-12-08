import os
import django

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import HeroPickStat
    HeroPickStat.objects.all().delete()
