from Products.Five import BrowserView

class GroupMailView(BrowserView):
    "really don't understand what I'm doing here but here goes it anyway"

    def __call__(self, groupName=''):
        """External method to recurse through a plone group and collect all
        member emails. If a member is a group and doesn't not have an email
        address, then that group is inspected and its members' emails are added
        to the email list. Groups inspected are tracked to avoid circular
        references.  Once all emails are collected, the list is first converted
        to a set and then into a string with email addresses comma
        separated."""

        to_list = ""
        address_list = []

        self.context.plone_log('====group_email=====')
        if groupName is '':
            self.context.plone_log('ERROR: groupName parameter not supplied'
                                   ' in call')
            return 
            
        grp = self.context.acl_users.getGroup(groupName)
        if grp == None: 
            self.context.plone_log('ERROR: No group with than "' + groupName + 
                            '"\n Source file: getAllMembersEmails.py')
            return # This will cause an error

        group_email = grp.getProperty('email')
        # if the group doesn't have an email, get the emails of its members
        # otherwise, use the group email address
        # ASSUMPTION: group email address recipient list is consistant with
        # the membership of the plone group
        if group_email in ['',None]:
            list_of_emails = self.getMemberEmails(grp,[])
            set_of_emails = set(list_of_emails)
            to_emails = ','.join(set_of_emails)
        else:
            to_emails = group_email

        self.context.plone_log('Email going to: ' + to_emails)
        return to_emails




    def getMemberEmails(self, grp, groups_already_examined=[]):
        """Return email list of address for individual members. If a member 
        is a group without an email address, then the function recurses into 
        that group to collect its members' emails. The list of groups examined
        is maintained to avoid cycles (g1 in g2 & g2 in g1)"""

        def raising(self, info):
            import traceback
            #traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

        mail_list = []
        # add current group to list of examined groups
        groups_already_examined.append(grp.getId())

        # for each member of the group, collect their email addresses into the
        # mail list. If the member is a group without an email address then
        # recurse into that group.
        for user in grp.getMemberIds():
            user_obj = self.context.acl_users.getUser(user) or \
                    self.context.acl_users.getGroup(user)
            user_email = user_obj.getProperty('email')

            if user_email not in [None, '']:
                mail_list.append(user_email)
            else:
                if user_obj.isGroup():
                    if user not in groups_already_examined:
                        sub_list = self.getMemberEmails(user_obj, 
                                                    groups_already_examined)
                        mail_list = mail_list + sub_list
 
        return mail_list
