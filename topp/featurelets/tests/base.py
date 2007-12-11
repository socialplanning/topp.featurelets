from warnings import warn
from time import time

import transaction
from Testing import ZopeTestCase

HAS_CMF = True
try:
    from Products.CMFTestCase.CMFTestCase import CMFTestCase
    from Products.CMFTestCase.CMFTestCase import setupCMFSite
    setupCMFSite()
except ImportError:
    HAS_CMF = False
    class CMFTestCase:
        pass

from zope.interface import directlyProvides
from zope.annotation.interfaces import IAttributeAnnotatable

from topp.featurelets.interfaces import IFeatureletSupporter

from utils import register_zcml

class FeatureletsTestCase(ZopeTestCase.ZopeTestCase):
    """
    Featurelets test case.
    """
    def afterSetUp(self):
        ZopeTestCase.ZopeTestCase.afterSetUp(self)
        register_zcml(with_setup=True)
        directlyProvides(self.folder, IAttributeAnnotatable)
        self.supporter = IFeatureletSupporter(self.folder)

class FeatureletsPortalTestCase(CMFTestCase):
    """
    Featurelets portal test case.
    """
    def afterSetUp(self):
        ZopeTestCase.PortalTestCase.afterSetUp(self)
        register_zcml(with_setup=True)
        directlyProvides(self.folder, IAttributeAnnotatable)
        self.supporter = IFeatureletSupporter(self.folder)
