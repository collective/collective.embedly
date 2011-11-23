from setuptools import setup, find_packages
import os

version = '1.7'

test_require = ['plone.app.testing']

setup(name='collective.embedly',
      version=version,
      description="TinyMCE visual editor support for embed.ly service",
      long_description=open(os.path.join("collective", "embedly", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
      ],
      keywords='web zope plone embedly TyniMCE plugin',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='https://github.com/collective/collective.embedly',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      tests_require=test_require,
      install_requires=[
          'setuptools',
          'plone.app.registry',
          # -*- Extra requirements: -*-
      ], 
      extras_require={'tests': test_require, }, 
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
