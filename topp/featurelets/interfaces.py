from zope.interface import Interface, Attribute

class IFeaturelet(Interface):
    """
    Marks a featurelet that can be plugged in to any IFeatureletSupporter.
    """

    id = Attribute("id", "Featurelet id.")
    
    title = Attribute("title", "Featurelet title.")
    
    config_view = Attribute("config_view", """
    The name of the view that is contains the configuration for this
    featurelet.  It should be publishable on objects that provide the
    interface specified by installed_marker.
    """)

    installed_marker = Attribute("installed_marker", """
    A marker interface that should be provided by the featurelet
    supporter context object when the featurelet is installed, and
    removed when then featurelet is uninstalled.
    """)

    def getRequiredInterfaces():
        """
        Returns a tuple of any interfaces (additional to
        IFeatureletSupporter) that this featurelet requires of its
        supporters.  Featurelet supporters may either implement or
        singly adapt to each of the required interfaces.
        """

    def deliverPackage(obj):
        """
        Performs the actual installation of the functionality
        'package' of the featurelet into an object.  Raises an
        exception if the object does not implement or adapt to
        IFeatureletSupporter of any of the required interfaces.

        If the featurelet is already installed, the featurelet will
        only install any differences btn the supporters stored
        featurelet description and the description that the featurelet
        has currently.

        Returns the featurelet description as it was installed.
        """

    def removePackage(obj):
        """
        Removes the featurelet's functionality from the obj.  This is
        potentially destructive (it will remove any objects that the
        featurelet created, for instance) so it should be used with
        care.
        """

class IFeatureletSupporter(Interface):
    """
    Marks a featurelet supporter that can accomodate IFeaturelets.
    """

    def getInstalledFeatureletIds():
        """
        Returns the ids of all installed featurelets; retrieved from
        the information the featurelets place in the featurelet
        annotation.
        """

    def getFeatureletDescriptor(id):
        """
        Returns the featurelet descriptor for the provided featurelet
        id, or None if the featurelet isn't installed.
        """

    def installFeaturelet(featurelet):
        """
        Installs the provided featurelet into the supporter. 
        """

    def removeFeaturelet(featurelet):
        """
        Uninstalls the provided featurelet by id, if it is installed.

        Can also take a full featurelet object, if you aren't into
        brevity.
        """

class IMenuSupporter(Interface):
    """
    Marks an object as being able to receive menu item mappings as
    provided by a featurelet.
    """

    def addMenuItem(menu_id, menu_item):
        """
        Adds a menu item to the specified menu.  Does nothing if a
        menu item with the same title already exists.

        o menu_id - A string representing the id of the menu w/ which
        the item should be registered.

        o menu_item - A mapping containing the menu item info.
        """

    def removeMenuItem(menu_id, menu_item_title):
        """
        Removes the menu item w/ the specified title from the
        specified menu.  Does nothing if a menu item w/ the specified
        title does not exist.

        o menu_id - A string representing the id of the menu from
        which the item should be removed.

        o menu_item_title - A string representing the title of the
        menu item that should be removed.
        """

    def getMenuItems(menu_id):
        """
        Returns a mapping of menu items for the specified menu id.
        Keys are the titles, values are menu item info mappings.
        """

class IFeatureletRegistry(Interface):
    """
    Defines a featurelet registration utility that featurelet
    supporters can use to discover which featurelets are available.
    """

    def registerFeaturelet(featurelet):
        """
        Registers a featurelet with the registry.  Raises an exception
        if a featurelet with the same id already exists.
        """

    def unregisterFeaturelet(featurelet_id):
        """
        Removes a featurelet with the specified id from the registry.
        Does nothing if no matching featurelet is registered.
        """

    def getFeaturelet(featurelet_id):
        """
        Retrieves the featurelet w/ the specified id.  Returns None if
        no matching featurelet is registered.
        """

    def getFeaturelets(supporter=None):
        """
        Returns all registered featurelets.  If 'supporter' is
        provided, then supporter is checked for adaptation to each of
        the featurelets' required interfaces, and only the featurelets
        which can actually be installed into the supporter are
        returned.
        """
