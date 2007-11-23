from OFS.interfaces import IObjectManager
import zExceptions

from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy

try:
    from Products.CMFCore.utils import getToolByName
except ImportError:
    getToolByName = None

from interfaces import IFeatureletSupporter
from interfaces import IMenuSupporter

from config import MENU_ID

class BaseFeaturelet(object):
    """
    Abstract base class for featurelet objects.  At a minimum,
    subclasses must provide 'id' and 'title' attributes (to complete
    the IFeaturelet implementation) and an '_info' attribute which
    actually describes the featurelet's contents.
    """
    _required_interfaces = (IObjectManager, IMenuSupporter)
    _menu_id = MENU_ID

    config_view = None
    installed_marker = None

    def __init__(self, context):
        self.context = context
    
    def _checkForRequiredInterfaces(self, obj):
        """
        Checks to see if the obj implements or can be adapted to all
        of the featurelet's required interfaces.
        """
        for iface in (IFeatureletSupporter,) + \
                self.getRequiredInterfaces():
            # just let adaptation raise an exception if necessary
            iface(obj)

    def getRequiredInterfaces(self):
        """
        See IFeaturelet.
        """
        return self._required_interfaces

    def _addObjects(self, obj):
        """
        Adds any objects that are specified by the featurelet's info.
        First checks for a previous installation of this featurelet,
        skips anything that was previously installed.

        Raises an error if content of the same id that was NOT a part
        of a previous installation of this featurelet exists.
        """
        info = self._info
        supporter = IFeatureletSupporter(obj)
        objmgr = IObjectManager(obj)

        prior_ids = tuple()
        prior_info = supporter.getFeatureletDescriptor(self.id)
        if prior_info is not None:
            prior_content = prior_info.get('objects', tuple())
            prior_ids = [item['id'] for item in prior_content]

        for item in info.get('objects', tuple()):
            iid = item['id']
            if iid not in prior_ids:
                if objmgr.hasObject(iid):
                    msg = "Object with id '%s' already exists." % iid
                    raise zExceptions.BadRequest, msg
                try:
                    newobj = item['class']()
                except TypeError:
                    # might need an id passed to the constructor                    
                    newobj = item['class'](iid)
                objmgr._setOb(iid, newobj)

    def _addContent(self, obj):
        """
        Adds any CMF content that is specified by the featurelet's
        info.  First checks for a previous installation of this
        featurelet, skips anything that was previously installed.

        Raises an error if content of the same id that was NOT a part
        of a previous installation of this featurelet exists.
        """
        ttool = getToolByName(obj, 'portal_types')
        info = self._info
        supporter = IFeatureletSupporter(obj)
        objmgr = IObjectManager(obj)

        prior_ids = tuple()
        prior_info = supporter.getFeatureletDescriptor(self.id)
        if prior_info is not None:
            prior_content = prior_info.get('content', tuple())
            prior_ids = [item['id'] for item in prior_content]

        for item in info.get('content', tuple()):
            if item['id'] not in prior_ids:
                ttool.constructContent(item['portal_type'],
                                       objmgr, item['id'],
                                       title=item['title'])

    def _addMenuItems(self, obj):
        """
        Registers any menu items that are specified by the
        featurelet's info.
        """
        info = self._info
        menu_id = self._menu_id
        supporter = IMenuSupporter(obj)
        menu_items = info.get('menu_items', tuple())
        for item_info in menu_items:
            supporter.addMenuItem(menu_id, item_info)

    def deliverPackage(self, obj):
        """
        See IFeaturelet.
        """
        self._checkForRequiredInterfaces(obj)
        if self._info.get('objects') is not None:
            self._addObjects(obj)
        if self._info.get('content') is not None \
               and getToolByName is not None:
            self._addContent(obj)
        if self._info.get('menu_items') is not None:
            self._addMenuItems(obj)
        if self.installed_marker is not None:
            directlyProvides(obj, directlyProvidedBy(obj),
                             self.installed_marker)
        return self._info

    def _removeObjects(self, obj, prior_info, info_key):
        """
        Removes any objects that were added to the supporter as a
        result of a prior installation of this featurelet.  Will not
        touch any objects that were not installed by this featurelet.
        """
        prior_objects = prior_info.get(info_key)
        if prior_objects is None:
            return

        objmgr = IObjectManager(obj)
        prior_ids = [item['id'] for item in prior_objects]
        del_ids = [id_ for id_ in prior_ids if objmgr.hasObject(id_)]
        if del_ids:
            objmgr.manage_delObjects(ids=del_ids)

    def _removeMenuItems(self, obj, prior_info):
        """
        Removes any menu items that were registered with this
        supporter as a result of a prior installation of this
        featurelet.  Will not affect any menu items that were not
        installed by this featurelet.
        """
        prior_menu_items = prior_info.get('menu_items')
        if prior_menu_items is None:
            return

        menu_id = self._menu_id
        supporter = IMenuSupporter(obj)
        for item in prior_menu_items:
            supporter.removeMenuItem(menu_id, item.get('title'))

    def removePackage(self, obj):
        """
        See IFeaturelet.
        """
        supporter = IFeatureletSupporter(obj)
        prior_info = supporter.getFeatureletDescriptor(self.id)
        if prior_info is None:
            return
        self._removeObjects(obj, prior_info, 'objects')
        if getToolByName is not None:
            self._removeObjects(obj, prior_info, 'content')
        self._removeMenuItems(obj, prior_info)
        if self.installed_marker is not None:
            directlyProvides(obj, directlyProvidedBy(obj) -
                             self.installed_marker)

    @property
    def installed(self):
        #XXX double context due to IFeaturelet(IFeatureletSupporter(IProject)))
        return self.installed_marker.providedBy(self.context.context)
