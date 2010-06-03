Introduction
============

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = 'contributor1'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True


Testing the groupEmail script
=============================

Testing that script has can be found
------------------------------------
    >>> my_func = portal.restrictedTraverse('@@getGroupEmails')
    >>> my_func
    <Products.Five.metaclass.getGroupEmails object ...
    >>> my_func('group_with_email')
    'group@example.com'

Testing correctness of script
-----------------------------

Test getGroupEmail script on a group with an email address
    >>> browser.open(portal_url + '/@@getGroupEmails?groupName=group_with_email')
    >>> browser.contents
    'group@example.com'

Test getGroupEmail script on a group without an email address and a single
member, Contributor1
    >>> browser.open(portal_url + '/@@getGroupEmails?groupName=group_noemail')
    >>> browser.contents
    'contributor1@example.com'

Test getGroupEmail script on a group containing members that are users, groups (noemail), and group (with email). Also contains a cycle.
    >>> browser.open(portal_url + '/@@getGroupEmails?groupName=supergroup')
    >>> browser.contents
    'group@example.com,contributor3@example.com,contributor1@example.com'

