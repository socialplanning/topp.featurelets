import zExceptions

from zope.interface import implements

from interfaces import IFeatureletRegistry

class FeatureletRegistry(object):
    """
    A global utility implementing IFeatureletRegistry.
    """
    implements(IFeatureletRegistry)

    _featurelets = {}
    
    def registerFeaturelet(self, featurelet):
        """
        See IFeatureletRegistry.
        """
        if self._featurelets.has_key(featurelet.id):
            msg = "Featurelet with id '%s' already registered." \
                  % featurelet.id
            raise zExceptions.BadRequest, msg
        self._featurelets[featurelet.id] = featurelet

    def unregisterFeaturelet(self, featurelet_id):
        """
        See IFeatureletRegistry.
        """
        if self._featurelets.has_key(featurelet_id):
            del self._featurelets[featurelet_id]

    def getFeaturelet(self, featurelet_id):
        """
        See IFeatureletRegistry.
        """
        return self._featurelets.get(featurelet_id)

    def getFeaturelets(self, supporter=None):
        """
        See IFeatureletRegistry.
        """
        featurelets = self._featurelets.values()
        if supporter is None:
            return featurelets

        def supportsInterfaces(obj, featurelet):
            """
            Returns True if obj supports featurelet's required
            interfaces, False if not.
            """
            for iface in featurelet.getRequiredInterfaces():
                try:
                    iface(obj)
                except TypeError:
                    return False
            return True

        return [f for f in featurelets if supportsInterfaces(supporter, f)]
