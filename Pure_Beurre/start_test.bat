coverage run --source='.' manage.py test substitute.tests
coverage html --skip-covered -d coverage_html
start coverage_html\index.html