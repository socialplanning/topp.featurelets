from zope.app.tests.placelesssetup import setUp
from Products.Five import zcml

import Products.Five
import topp.featurelets

def register_zcml(with_setup=False):
    if with_setup:
        setUp()
    zcml.load_config('meta.zcml', Products.Five)
    zcml.load_config('permissions.zcml', Products.Five)
    zcml.load_config('configure.zcml', Products.Five)
    zcml.load_config('configure.zcml', topp.featurelets)
