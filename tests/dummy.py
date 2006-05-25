from OFS.DTMLMethod import DTMLMethod

from Products.Five import BrowserView

from zope.interface import Interface

from topp.featurelets.base import BaseFeaturelet

success = "SUCCESS!!"

class IDummyFeatureletInstalled(Interface):
    """
    Signifies that a dummy featurelet has been installed.
    """

class ObjectsFeaturelet(BaseFeaturelet):
    id = 'objects_featurelet'
    _info = {'objects': ({'id': 'foo', 'class': DTMLMethod},
                         {'id': 'bar', 'class': DTMLMethod},
                         ),
             }

class ContentFeaturelet(BaseFeaturelet):
    id = 'objects_featurelet'
    _info = {'content': ({'id': 'foo', 'title': 'Foo',
                          'portal_type': 'Document'},
                         {'id': 'bar', 'title': 'Bar',
                          'portal_type': 'Document'},
                         ),
             }

class ConfigFeaturelet(BaseFeaturelet):
    id = 'config_featurelet'
    _info = {}
    config_view = 'dummy_config'
    installed_marker = IDummyFeatureletInstalled

class DummyConfigView(BrowserView):
    def __call__(self):
        return success
