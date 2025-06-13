import os
import sys
import django
from django.test.utils import get_runner
from django.conf import settings

def run_tests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings.test'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    failures = test_runner.run_tests(['users', 'academics', 'courses', 'assessment', 'student_services'])
    sys.exit(bool(failures))

if __name__ == '__main__':
    run_tests()