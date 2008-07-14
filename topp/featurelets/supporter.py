from persistent.mapping import PersistentMapping

from zope.interface import implements
from zope.app.annotation.interfaces import IAnnotations
from zope.component import getAdapter

from interfaces import IFeatureletSupporter, IFeaturelet

class FeatureletSupporter(object):
    """
    Adapts from IAnnotatable to IFeatureletSupporter.
    """

    implements(IFeatureletSupporter)
    annotations_key = "featurelets"

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        key = self.annotations_key
        if not annotations.has_key(key):
            annotations[key] = PersistentMapping()
        self.storage = annotations[key]

    def getInstalledFeatureletIds(self):
        """
        See IFeatureletSupporter.
        """
        return self.storage.keys()

    def getFeatureletDescriptor(self, id):
        """
        See IFeatureletSupporter.
        """
        return self.storage.get(id)

    def installFeaturelet(self, featurelet):
        """
        See IFeatureletSupporter.
        """
        name, featurelet = self._fetch_featurelet(featurelet)
        info = featurelet.deliverPackage(self.context)
        self.storage[name] = info
        
    def removeFeaturelet(self, featurelet):
        """
        See IFeatureletSupporter.
        """
        name, featurelet=self._fetch_featurelet(featurelet)
        if self.storage.has_key(name):
            featurelet.removePackage(self.context)
            self.storage.pop(name)

    def _fetch_featurelet(self, name):
        #if not isinstance(name, basestring) and IFeaturelet.providedBy(name):
        if not isinstance(name, basestring):
            return name.id, name
        return name, getAdapter(self, IFeaturelet, name)
