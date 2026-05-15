import os
import sys
import django

# Tell Sphinx to look in the parent directory for the Django project
sys.path.insert(0, os.path.abspath('..'))
# Point to your Django settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'news_project.settings'
# Initialize Django to load the models
django.setup()

project = 'NewsApp'
copyright = '2026, Developer'
author = 'Developer'
release = '00.00.01'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']