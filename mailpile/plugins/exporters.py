import mailbox
import os
import time

import mailpile.config
from mailpile.commands import Command
from mailpile.i18n import gettext as _
from mailpile.i18n import ngettext as _n
from mailpile.mailutils import Email
from mailpile.plugins import PluginManager
from mailpile.util import *


_plugins = PluginManager(builtin=os.path.basename(__file__)[:-3])


##[ Configuration ]###########################################################

MAILBOX_FORMATS = ('mbox', 'maildir')

_plugins.register_config_variables('prefs', {
    'export_format': ['Default format for exporting mail',
                      MAILBOX_FORMATS, 'mbox'],
})


##[ Commands ]################################################################

class ExportMail(Command):
    """Export messages to an external mailbox"""
    SYNOPSIS = (None, 'export', None, '<msgs> [flat] [<fmt>:<path>]')
    ORDER = ('Searching', 99)

    def export_path(self, mbox_type):
        if mbox_type == 'mbox':
            return 'mailpile-%d.mbx' % time.time()
        else:
            return 'mailpile-%d'

    def create_mailbox(self, mbox_type, path):
        if mbox_type == 'mbox':
            return mailbox.mbox(path)
        elif mbox_type == 'maildir':
            return mailbox.Maildir(path)
        raise UsageError('Invalid mailbox type: %s' % mbox_type)

    def command(self, save=True):
        session, config, idx = self.session, self.session.config, self._idx()
        mbox_type = config.prefs.export_format

        if self.session.config.sys.lockdown:
            return self._error(_('In lockdown, doing nothing.'))

        args = list(self.args)
        if args and ':' in args[-1]:
            mbox_type, path = args.pop(-1).split(':', 1)
        else:
            path = self.export_path(mbox_type)

        if args and args[-1] == 'flat':
            flat = True
            args.pop(-1)
        else:
            flat = False

        if os.path.exists(path):
            return self._error('Already exists: %s' % path)

        msg_idxs = list(self._choose_messages(args))
        if not msg_idxs:
            session.ui.warning('No messages selected')
            return False

        # Exporting messages without their threads barely makes any
        # sense.
        if not flat:
            for i in reversed(range(0, len(msg_idxs))):
                mi = msg_idxs[i]
                msg_idxs[i:i+1] = [int(m[idx.MSG_MID], 36)
                                   for m in idx.get_conversation(msg_idx=mi)]

        # Let's always export in the same order. Stability is nice.
        msg_idxs.sort()

        mbox = self.create_mailbox(mbox_type, path)
        exported = {}
        while msg_idxs:
            msg_idx = msg_idxs.pop(0)
            if msg_idx not in exported:
                e = Email(idx, msg_idx)
                session.ui.mark('Exporting =%s ...' % e.msg_mid())
                mbox.add(e.get_msg())
                exported[msg_idx] = 1

        mbox.flush()

        return self._success(
            _('Exported %d messages to %s') % (len(exported), path),
            {
                'exported': len(exported),
                'created': path
            })

_plugins.register_commands(ExportMail)
