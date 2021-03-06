import os

from mailpile.mail_source import BaseMailSource
from mailpile.i18n import gettext as _
from mailpile.i18n import ngettext as _n


class MaildirMailSource(BaseMailSource):
    """
    This is a mail source that watches over one or more Maildirs.
    """
    # This is a helper for the events.
    __classname__ = 'mailpile.mail_source.maildir.MaildirMailSource'

    def __init__(self, *args, **kwargs):
        BaseMailSource.__init__(self, *args, **kwargs)
        self.watching = -1

    def open(self):
        with self._lock:
            mailboxes = self.my_config.mailbox.values()
            if self.watching == len(mailboxes):
                return True
            else:
                self.watching = len(mailboxes)

            for d in ('mtimes_cur', 'mtimes_new', 'mtimes_tmp'):
                if d not in self.event.data:
                    self.event.data[d] = {}

        self._log_status(_('Watching %d maildir mailboxes') % self.watching)
        return True

    def _has_mailbox_changed(self, mbx, state):
        for sub in ('cur', 'new', 'tmp'):
            try:
                mt = os.path.getmtime(os.path.join(self._path(mbx), sub))
            except (OSError, IOError):
                mt = -1
            state[sub] = long(mt)
        for sub in ('cur', 'new', 'tmp'):
            if state[sub] != self.event.data['mtimes_%s' % sub].get(mbx._key):
                return True
        return False

    def _mark_mailbox_rescanned(self, mbx, state):
        for sub in ('cur', 'new', 'tmp'):
            self.event.data['mtimes_%s' % sub][mbx._key] = state[sub]

    def is_mailbox(self, fn):
        if not os.path.isdir(fn):
            return False
        for sub in ('cur', 'new', 'tmp'):
            subdir = os.path.join(fn, sub)
            if not os.path.exists(subdir) or not os.path.isdir(subdir):
                return False
        return True
