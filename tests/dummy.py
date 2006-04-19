from OFS.DTMLMethod import DTMLMethod

from zope.interface import Interface

from topp.featurelets.base import BaseFeaturelet

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
