

```
rm -f db.sqlite3

rm -rf myproject/accounts/migrations/
rm -rf myproject/crm/migrations/

mkdir myproject/accounts/migrations/
mkdir myproject/crm/migrations/

touch myproject/accounts/migrations/__init__.py
touch myproject/crm/migrations/__init__.py

python manage.py makemigrations accounts crm
python manage.py migrate

python manage.py createsuperuser --email='admin@email.com'
```
