import unittest

from Products.Five.zcml import load_string

from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from zope.interface import Interface

from base import FeatureletsTestCase
from dummy import ConfigFeaturelet
from dummy import success

class TestFeatureletConfig(FeatureletsTestCase):

    def afterSetUp(self):
        FeatureletsTestCase.afterSetUp(self)
        decl = """
        <configure xmlns="http://namespaces.zope.org/zope"
            xmlns:browser="http://namespaces.zope.org/browser">

            <browser:page
                for="topp.featurelets.tests.dummy.IDummyFeatureletInstalled"
                class="topp.featurelets.tests.dummy.DummyConfigView"
                permission="zope2.View"
                name="dummy_config"
                />

        </configure>
        """
        load_string(decl)        
        self.featurelet = ConfigFeaturelet()

    def test_configViewOnlyWhenInstalled(self):
        request = self.folder.REQUEST
        view = None
        try:
            view = getMultiAdapter((self.folder, request),
                                   Interface,
                                   name=ConfigFeaturelet.config_view)
        except ComponentLookupError:
            pass
        self.failIf(view is not None)

        self.supporter.installFeaturelet(self.featurelet)
        view = getMultiAdapter((self.folder, request),
                               Interface,
                               name=ConfigFeaturelet.config_view)
        self.failIf(view is None)
        self.assertEqual(view(), success)

        view = None
        self.supporter.removeFeaturelet(self.featurelet)
        try:
            view = getMultiAdapter((self.folder, request),
                                   Interface,
                                   name=ConfigFeaturelet.config_view)
        except ComponentLookupError:
            pass
        self.failIf(view is not None)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFeatureletConfig))
    return suite
