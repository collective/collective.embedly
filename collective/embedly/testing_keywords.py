class Keywords(object):
    """Robot Framework keyword library"""

    def get_test_user_name(self):
        import plone.app.testing
        return plone.app.testing.interfaces.TEST_USER_NAME

    def get_test_user_password(self):
        import plone.app.testing
        return plone.app.testing.interfaces.TEST_USER_PASSWORD

    def get_test_site_owner_name(self):
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_NAME

    def get_test_site_owner_password(self):
        import plone.app.testing
        return plone.app.testing.interfaces.SITE_OWNER_PASSWORD
