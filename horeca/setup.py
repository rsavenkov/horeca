import os
from setuptools import setup, find_packages

setup(
    name='horeca-backend',
    version=os.getenv('HORECA_VERSION') or os.getenv('BITBUCKET_COMMIT'),
    url='https://bitbucket.org/bsl-dev/horeca_backend/src/master/',
    description='Backend for Horeca web',
    packages=find_packages(),
    setup_requires=['wheel'],
    install_requires=[
        'Django==3.1.4',
        'djangorestframework==3.12.2',
        'django-cors-headers==3.6.0',
        'psycopg2-binary==2.8.6',
        'django-rest-passwordreset==1.1.0',
        'openpyxl==3.0.6',
        'Pillow==8.1.0',
        'django-filter==2.4.0',
        'django-multiselectfield==0.1.12',
        'requests==2.25.1',
        'factory-boy==3.2.0',
    ],
    include_package_data=True,
)
