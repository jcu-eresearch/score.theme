from setuptools import setup, find_packages
import os

version = '1.2-beta3'

setup(name='plonetheme.notredame',
      version=version,
      description="Theme for Plone 3 with color scheme based on new Plone Logo",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='web zope plone theme',
      author='Harito Reisman, Christian Schneider',
      author_email='notredame@haritomedia.com',
      url='http://svn.plone.org/svn/collective/plonetheme.notredame',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonetheme'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
          'collective.easytemplate', #need this for content rules
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
