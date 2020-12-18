coverage run --source='.' manage.py test substitute.project_tester.selenium substitute.project_tester.tests
coverage html --skip-covered --skip-empty -d substitute\project_tester\coverage_html
start substitute\project_tester\coverage_html\index.html