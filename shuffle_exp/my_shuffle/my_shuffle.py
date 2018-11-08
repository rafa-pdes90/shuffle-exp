from .sorteddict import SortedDict
import random
import numpy
import statistics

def weighted_shuffle(items, weight):
  items.sort(key=lambda i: -random.random() ** (1.0 / getattr(i, weight)))

def shuffle(x, y, w, w_step=None):
  songs_by_y = {}
  songs_pos = SortedDict()

  if w_step is None:
    w_min=float("inf")
    w_max=0
  
  for i in range(len(x)):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(x[i])
    weight = getattr(x[i], w)
    if w_step is None:
      w_min = min(w_min, weight)
      w_max = max(w_max, weight)

  if w_step is None:
    w_step = 100.0 / (w_max - w_min + 1)

  if len(y) > 1:
    for songs in songs_by_y.values():
      shuffle(songs, y[1:], w, w_step=w_step)
  else:
    for songs in songs_by_y.values():
      weighted_shuffle(songs, w)

  songs_groups = sorted(songs_by_y.values(), reverse=True, key=lambda i: [getattr(s, w) for s in i])

  for i in range(len(songs_groups) - 1, -1, -1):
    songs = songs_groups[i]
    song_count = len(songs)

    offset_mode = 100.0 - (getattr(songs[0], w) - 0.5)*w_step
    pos = numpy.random.triangular(0.0, offset_mode, 100.0)
    while pos in songs_pos:
      pos = numpy.random.triangular(0.0, offset_mode, 100.0)
    last_index = songs_pos.__setitem__(pos, songs[0])

    for j in range (1, song_count):
      song_w = getattr(songs[j], w)
      total = 0
      for k in range(last_index -1, -1, -1):
        item = songs_pos.peekitem(index=k)
        item_w = getattr(item[1], w)
        if song_w <= item_w:
          total += item_w

  x[:] = songs_pos.values()
