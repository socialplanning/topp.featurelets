from setuptools import setup, find_packages

version = '0.3.0'

setup(name='topp.featurelets',
      version=version,
      description="Base support for plone featurelets (i.e. feature plugins)",
      long_description=open('topp/featurelets/README.txt').read(),
      classifiers=['Framework :: Plone', 'Framework :: Zope2',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Programming Language :: Python :: 2',
                   ],
      # classifier strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='featurelets openplans plone topp',
      author='Rob Miller',
      author_email='robm@openplans.org',
      url='https://svn.openplans.org/svn/topp.featurelets/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['topp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'topp.utils>=0.5',
      ],
      dependency_links=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
