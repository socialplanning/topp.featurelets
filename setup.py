from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='topp.featurelets',
      version=version,
      description="Base support for featurelets (i.e. feature plugins)",
      long_description="""\
""",
      classifiers=[], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='featurelets openplans topp',
      author='Rob Miller',
      author_email='robm@openplans.org',
      url='https://svn.openplans.org/svn/topp.featurelets/',
      license='GPL',
      install_depends=['topp.utils>=0.1'],
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['topp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
