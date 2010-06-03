"""Test setup for integration and functional tests.

When we import PloneTestCase and then call setupPloneSite(), all of
Plone's products are loaded, and a Plone site will be created. This
happens at module level, which makes it faster to run each test, but
slows down test runner startup.
"""

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.Five.testbrowser import Browser

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.PloneTestCase.setup import portal_owner, default_password

from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager

from AccessControl.SecurityManager import setSecurityPolicy
from AccessControl.ImplPython import ZopeSecurityPolicy

# When ZopeTestCase configures Zope, it will *not* auto-load products
# in Products/. Instead, we have to use a statement such as:
#   ztc.installProduct('SimpleAttachment')
# This does *not* apply to products in eggs and Python packages (i.e.
# not in the Products.*) namespace. For that, see below.
# All of Plone's products are already set up by PloneTestCase.

@onsetup
def setup_product():
    """Set up the package and its dependencies.

    The @onsetup decorator causes the execution of this body to be
    deferred until the setup of the Plone site testing layer. We could
    have created our own layer, but this is the easiest way for Plone
    integration tests.
    """

    # Load the ZCML configuration for the example.tests package.
    # This can of course use <include /> to include other packages.

    fiveconfigure.debug_mode = True
    import plonetheme.notredame
    zcml.load_config('configure.zcml', plonetheme.notredame)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML. Thus, we do it here. Note the use of installPackage()
    # instead of installProduct().
    # This is *only* necessary for packages outside the Products.*
    # namespace which are also declared as Zope 2 products, using
    # <five:registerPackage /> in ZCML.

    # We may also need to load dependencies, e.g.:
    #   ztc.installPackage('borg.localrole')

    ztc.installPackage('plonetheme.notredame')

# The order here is important: We first call the (deferred) function
# which installs the products we need for this product. Then, we let
# PloneTestCase set up this product on installation.

setup_product()
ptc.setupPloneSite(products=['plonetheme.notredame'])

class DummyMailHost:

     sentMail = []

     def send(self, mBody):
          self.sentMail.append(mBody)

     def secureSend(self, message, mto, mfrom, subject='[No Subject]',
                    mcc=None, mbcc=None, subtype='plain', charset='us-ascii',
                    debug=False, **kwargs):
         self.sentMail.append('To: '+mto+'/nFrom: '+mfrom+'/nSubject: '+\
                              subject+'/nMessage: '+message)

     def readMailBox(self):
          sentMail = self.sentMail
          self.sentMail = []
          return sentMail


class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """

    def afterSetUp(self):
        ptc.FunctionalTestCase.afterSetUp(self)

        roles = ('Member', 'Contributor')
        memberOnlyRoles = ('Member',)
        # Set up test user accounts
        self.portal.portal_membership.addMember(
                'contributor1', 'secret', roles, [],
                {'fullname': 'Contributor 1', 
                    'email':'contributor1@example.com'})
        self.portal.portal_membership.addMember(
                'contributor2', 'secret', roles, [],
                {'fullname': 'Contributor 2', 
                    'email':'contributor2@example.com'})
        self.portal.portal_membership.addMember(
                'contributor3', 'secret', memberOnlyRoles, [],
                {'fullname': 'Contributor 3', 
                    'email':'contributor3@example.com'})
        self.portal.portal_membership.addMember(
                'manager1', 'secret', ('Manager',), [],
                {'fullname': 'Manager 1',
                    'email': 'manager1@example.com'})

        # Create test groups
        self.portal.portal_groups.addGroup(
                'tac3_mailing_list',None,[], 
                {'title':'TAC3 Mailing List', 'email':''})
        self.portal.portal_groups.addGroup(
                'tac2_mailing_list',None,[],
                {'title':'TAC2 Mailing List', 'email':''})
        self.portal.portal_groups.addGroup(
                'tac1_mailing_list',None,[],
                {'title':'TAC1 Mailing List','email':''})
        self.portal.portal_groups.addGroup(
                'group_noemail',None,[],
                {'title':'Group Noemail','email':''})
        self.portal.portal_groups.addGroup(
                'group_noemail2',None,[],
                {'title':'Group 2 Noemail','email':''})
        self.portal.portal_groups.addGroup(
                'group_with_email',None,[],
                {'title':'Group With Email','email':'group@example.com'})
        self.portal.portal_groups.addGroup(
                'supergroup',None,[],
                {'title':'Supergroup','email':''})

        # add users to groups
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor3', 'tac3_mailing_list')
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor2', 'tac2_mailing_list')
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor1', 'tac1_mailing_list')

        self.portal.portal_groups.addPrincipalToGroup(
                'contributor1', 'group_noemail')
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor1', 'group_noemail2')
        self.portal.portal_groups.addPrincipalToGroup(
                'supergroup', 'group_noemail2')
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor2', 'group_with_email')
        self.portal.portal_groups.addPrincipalToGroup(
                'contributor3', 'supergroup')
        self.portal.portal_groups.addPrincipalToGroup(
                'group_with_email', 'supergroup')
        self.portal.portal_groups.addPrincipalToGroup(
                'group_noemail2', 'supergroup')

        ownerUser = self.portal.portal_membership.getMemberById(portal_owner)
        ownerUser.setMemberProperties(
                {'fullname': 'Portal Owner', 'email':'owner@example.com'})

        self.portal.email_from_address = 'site@example.com'
        self.portal.MailHost = DummyMailHost()
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        dummyMailHost = DummyMailHost()
        sm.registerUtility(dummyMailHost, IMailHost)

        setSecurityPolicy(ZopeSecurityPolicy(verbose=True))

        browser = self.browser = Browser()
        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            #traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising


