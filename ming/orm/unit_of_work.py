from .base import state, ObjectState

class UnitOfWork(object):

    def __init__(self, session):
        self.session = session
        self._objects = {}

    def save(self, obj):
        self._objects[id(obj)] = obj

    @property
    def new(self):
        return (obj for obj in self._objects.itervalues()
                if state(obj).status == ObjectState.new)

    @property
    def clean(self):
        return (obj for obj in self._objects.itervalues()
                if state(obj).status == ObjectState.clean)

    @property
    def dirty(self):
        return (obj for obj in self._objects.itervalues()
                if state(obj).status == ObjectState.dirty)

    @property
    def deleted(self):
        return (obj for obj in self._objects.itervalues()
                if state(obj).status == ObjectState.deleted)

    def flush(self):
        new_objs = {}
        for i, obj in self._objects.items():
            st = state(obj)
            if st.status == ObjectState.new:
                self.session.insert_now(obj, st)
                st.status = ObjectState.clean
                new_objs[i] = obj
            elif st.status == ObjectState.dirty:
                self.session.update_now(obj, st)
                st.status = ObjectState.clean
                new_objs[i] = obj
            elif st.status == ObjectState.deleted:
                self.session.delete_now(obj, st)
            elif st.status == ObjectState.clean:
                new_objs[i] = obj
            else:
                assert False, 'Unknown obj state: %s' % st.status
        self._objects = new_objs
        self.session.imap.clear()
        for obj in new_objs.itervalues():
            self.session.imap.save(obj)

    def __repr__(self):
        l = ['<UnitOfWork>']
        l.append('  <new>')
        l += [ '    %r' % x for x in self.new ]
        l.append('  <clean>')
        l += [ '    %r' % x for x in self.clean ]
        l.append('  <dirty>')
        l += [ '    %r' % x for x in self.dirty ]
        l.append('  <deleted>')
        l += [ '    %r' % x for x in self.deleted ]
        return '\n'.join(l)

    def clear(self):
        self._objects = {} # dict[id(obj)] = obj
