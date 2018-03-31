import os
import django
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vainconcierge.settings")

    django.setup()

    from vainpick.models import Match
    all_rec = Match.objects.all()

    max_count = int(sys.argv[1])
    current_count = len(all_rec)

    for rec in all_rec:
        if current_count <= max_count:
            break
        rec.delete()
        current_count -= 1

    
