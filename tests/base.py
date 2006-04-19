from Testing.ZopeTestCase import ZopeTestCase

from zope.interface import directlyProvides
from zope.app.annotation.interfaces import IAttributeAnnotatable

from topp.featurelets.interfaces import IFeatureletSupporter

from utils import register_zcml

class FeatureletsTestCase(ZopeTestCase):
    """
    Featurelets test case.
    """
    def afterSetUp(self):
        ZopeTestCase.afterSetUp(self)
        register_zcml(with_setup=True)
        directlyProvides(self.folder, IAttributeAnnotatable)
        self.supporter = IFeatureletSupporter(self.folder)
