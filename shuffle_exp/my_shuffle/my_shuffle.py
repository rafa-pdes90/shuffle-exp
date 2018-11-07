import random
import numpy
import statistics

def weighted_shuffle(items, weight):
  items.sort(key=lambda i: -random.random() ** (1.0 / getattr(i, weight)))

def shuffle(x, y, w, w_step=None):
  songs_by_y = {}
  songs_pos = {}

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

  for songs in songs_by_y.values():
    if len(y) > 1:
      shuffle(songs, y[1:], w, w_step=w_step)
    else:
      weighted_shuffle(songs, w)

    song_count = len(songs)
    appear_base = 100.0/song_count
    appear_lim = appear_base - 100.0/(song_count+1)
    appear_max, appear_min = min(100.0, appear_base + appear_lim), max(0.0, appear_base - appear_lim)

    offset_base = 100.0 - getattr(songs[0], w)*w_step
    offset_mode = [offset_base, offset_base + (w_step/2), offset_base + w_step]
    last_pos = songs_pos[songs[0]] = statistics.mean(numpy.random.triangular(0.0, offset_mode, 100.0))

    for i in range (1, song_count):
      last_pos = songs_pos[songs[i]] = (last_pos + random.uniform(appear_min, appear_max)) % 100

  x.sort(key=lambda i: songs_pos[i])
