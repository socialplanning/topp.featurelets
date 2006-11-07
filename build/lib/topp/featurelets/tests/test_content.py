import unittest
import zExceptions

from base import FeatureletsPortalTestCase
from base import HAS_CMF
from dummy import ContentFeaturelet

class TestContentFeaturelet(FeatureletsPortalTestCase):

    def afterSetUp(self):
        FeatureletsPortalTestCase.afterSetUp(self)
        self.featurelet = ContentFeaturelet()

    def test_objectsAreCreated(self):
        for ob_info in ContentFeaturelet._info['content']:
            self.failIf(self.folder.hasObject(ob_info['id']))
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ContentFeaturelet._info['content']:
            ob = self.folder._getOb(ob_info['id'], None)
            self.assertEqual(ob.portal_type, ob_info['portal_type'])

    def test_objectsAreDeleted(self):
        self.supporter.installFeaturelet(self.featurelet)
        self.supporter.removeFeaturelet(self.featurelet)
        for ob_info in ContentFeaturelet._info['content']:
            self.failIf(self.folder.hasObject(ob_info['id']))

    def test_twiceIsOkay(self):
        marker = 'marked'
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ContentFeaturelet._info['content']:
            ob = self.folder._getOb(ob_info['id'])
            ob.marker = marker
        self.supporter.installFeaturelet(self.featurelet)
        for ob_info in ContentFeaturelet._info['content']:
            ob = self.folder._getOb(ob_info['id'])
            self.assertEqual(ob.marker, marker)

    def test_twiceDoesNotRestoreDeleted(self):
        self.supporter.installFeaturelet(self.featurelet)
        del_id = ContentFeaturelet._info['content'][0]['id']
        self.folder._delOb(del_id)
        self.supporter.installFeaturelet(self.featurelet)
        self.failIf(self.folder.hasObject(del_id))

    def test_alreadyExistsRaisesError(self):
        ob_info = ContentFeaturelet._info['content'][0]
        self.folder.portal_types.constructContent(ob_info['portal_type'],
                                                  self.folder, ob_info['id'])
        self.assertRaises(zExceptions.BadRequest,
                          self.supporter.installFeaturelet,
                          self.featurelet)

    def test_uninstalledRemovalIsOkay(self):
        self.supporter.removeFeaturelet(self.featurelet)

    def test_uninstallDoesNotRemoveExistingObjects(self):
        ob_info = ContentFeaturelet._info['content'][0]
        self.folder.portal_types.constructContent(ob_info['portal_type'],
                                                  self.folder, ob_info['id'])
        self.supporter.removeFeaturelet(self.featurelet)
        self.failUnless(self.folder.hasObject(ob_info['id']))

def test_suite():
    suite = unittest.TestSuite()
    if HAS_CMF:
        suite.addTest(unittest.makeSuite(TestContentFeaturelet))
    return suite
