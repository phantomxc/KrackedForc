import cPickle, cStringIO

def pickle(some_obj):
   pickled_str_io = cStringIO.StringIO()
   cPickle.dump(some_obj, pickled_str_io)
   pickled_str = pickled_str_io.getvalue()
   return pickled_str

def unpickle(pickled_str):
   pickled_str_io = cStringIO.StringIO(pickled_str)
   return cPickle.load(pickled_str_io)
