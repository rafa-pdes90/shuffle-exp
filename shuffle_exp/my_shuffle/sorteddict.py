from sortedcontainers import SortedDict as OriginalSortedDict

class SortedDict(OriginalSortedDict):
  def __setitem__(self, key, value):
    super(SortedDict, self).__setitem__(key, value)
    return self.index(key)
