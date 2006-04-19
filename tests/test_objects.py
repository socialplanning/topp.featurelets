import unittest
import zExceptions

from OFS.DTMLMethod import DTMLMethod

from base import FeatureletsTestCase
from dummy import ObjectsFeaturelet

class TestObjectsFeaturelet(FeatureletsTestCase):

    def afterSetUp(self):
        FeatureletsTestCase.afterSetUp(self)
        self.featurelet = ObjectsFeaturelet()

    def test_objectsAreCreated(self):
        for ob_info in ObjectsFeaturelet._info['objects']:
            self.failIf(self.folder.hasObject(ob_info['id']))
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ObjectsFeaturelet._info['objects']:
            ob = self.folder._getOb(ob_info['id'], None)
            self.assertEqual(ob.__class__, ob_info['class'])

    def test_objectsAreDeleted(self):
        self.supporter.installFeaturelet(self.featurelet)
        self.supporter.removeFeaturelet(self.featurelet)
        for ob_info in ObjectsFeaturelet._info['objects']:
            self.failIf(self.folder.hasObject(ob_info['id']))

    def test_twiceIsOkay(self):
        marker = 'marked'
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ObjectsFeaturelet._info['objects']:
            ob = self.folder._getOb(ob_info['id'])
            ob.marker = marker
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ObjectsFeaturelet._info['objects']:
            ob = self.folder._getOb(ob_info['id'])
            self.assertEqual(ob.marker, marker)

    def test_twiceDoesNotRestoreDeleted(self):
        self.supporter.installFeaturelet(self.featurelet)
        del_id = ObjectsFeaturelet._info['objects'][0]['id']
        self.folder._delOb(del_id)
        self.supporter.installFeaturelet(self.featurelet)
        self.failIf(self.folder.hasObject(del_id))

    def test_alreadyExistsRaisesError(self):
        ob = DTMLMethod()
        ob_id = ObjectsFeaturelet._info['objects'][0]['id']
        self.folder._setOb(ob_id, ob)
        self.assertRaises(zExceptions.BadRequest,
                          self.supporter.installFeaturelet,
                          self.featurelet)

    def test_uninstalledRemovalIsOkay(self):
        self.supporter.removeFeaturelet(self.featurelet)

    def test_uninstallDoesNotRemoveExistingObjects(self):
        ob = DTMLMethod()
        ob_id = ObjectsFeaturelet._info['objects'][0]['id']
        self.folder._setOb(ob_id, ob)
        self.supporter.removeFeaturelet(self.featurelet)
        self.failUnless(self.folder.hasObject(ob_id))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestObjectsFeaturelet))
    return suite

