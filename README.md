# delete django unused files

Simple script for deleting all files in filesystem without link to existing instance of FileField in djangomodels
It finds all FileField and compare to its storage's existing content. The files existing in storage and not existing in database will be deleted.

Best usage is with IPython
```
./manage.py shell -i ipython
%load https://raw.githubusercontent.com/dburton90/delete_django_unused_files/master/delete_unused.py
```
