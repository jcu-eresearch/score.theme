import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing, eventtesting

from Testing import ZopeTestCase as ztc

from plonetheme.notredame.tests import base

def test_suite():
    return unittest.TestSuite([

        #doctest.REPORT_ONLY_FIRST_FAILURE
        ztc.ZopeDocFileSuite(
            'contentrules.txt', package='plonetheme.notredame',
            test_class=base.FunctionalTestCase,
            optionflags= doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
