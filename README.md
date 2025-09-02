# Madinatna

Django + DRF app for managing clusters, categories, and facilities with images.

- Admin dashboard for CRUD
- REST API for tenants to browse facilities by cluster/category
- Role-based editing: owners can edit their own facility

Quick start:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API base: /api/
- /api/categories/
- /api/clusters/
- /api/facilities/
- /api/facilities/?cluster=<id>&category=<id>
- /api/facilities/mine/

Upload directory: media/facility_images
