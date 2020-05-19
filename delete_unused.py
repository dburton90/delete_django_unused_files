from pathlib import Path
from collections import defaultdict

from django.db.models import FileField, Q
from django.apps import apps




def get_files():
    all_files = defaultdict(set)
    storages = {}
    for m in apps.get_models():
        fields = [f for f in m._meta.get_fields() if isinstance(f, FileField)]
        for field in fields:
            bs = field.storage.base_location
            storages[bs] = field.storage

            f = ~Q(Q(**{field.attname + '__isnull': True})|Q(**{field.attname:''}))
            all_files[bs].update(m.objects.filter(f).values_list(field.attname, flat=True))
    return all_files, storages


def find_to_delete_files(all_files):
    to_delete = defaultdict(list)

    for key, file_names in all_files.items():
        base = Path(key)
        for f in base.rglob('*'):
            filename = str(f.relative_to(base))
            if f.is_file() and filename not in file_names:
                to_delete[key].append(filename)

    return to_delete


def delete_files(to_delete, storages):
    for key, files in to_delete.items():
        if files:
            print(key + " deleting files:")
            for f in files:
                storages[key].delete(f)
                print("- ", f)
    else:
        print("Nothing to delete")


def delete_unused_files():
    f, s = get_files()
    d = find_to_delete_files(f)
    delete_files(d, s)


if __name__ == '__main__':
    delete_unused_files()
