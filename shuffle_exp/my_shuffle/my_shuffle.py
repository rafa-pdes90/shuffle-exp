import random
import numpy
import statistics

def shuffle(x, y, w):
  def pos(song, weight, w_step):
    mode = 100.0 - (getattr(song, weight) - random.random())*w_step
    return numpy.random.triangular(0.0, mode, 100.0)
  
  w_min=float("inf")
  w_max=0
  
  for i in range(len(x)):
    weight = getattr(x[i], w)
    w_min = min(w_min, weight)
    w_max = max(w_max, weight)

  w_step = 100.0 / (w_max - w_min + 1)
  x.sort(key=lambda i: pos(i, w, w_step))
  weighted_shuffle(x, y, w)

def weighted_shuffle(x, y, w):
  songs_by_y = {}
  songs_pos = {}
  song_count = len(x)
  g_step = 1.0/song_count
  
  for i in range(song_count):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append((x[i], i))

  for songs in songs_by_y.values():
    if len(y) > 1:
      weighted_shuffle(songs, y[1:], w)
    
    group_count = len(songs)

    if group_count == 1:
      songs_pos[songs[0][0]] = songs[0][1]/(song_count-1)
    else:
      first = songs[0][1]/(song_count-1)
      last = songs[-1][1]/(song_count-1)
      min_gap = group_count * g_step

      if (last - first) < min_gap:
        max_gap = (group_count+1) * g_step
        inc = random.uniform(min_gap, max_gap)/2
        first = max(0.0, first - inc)
        last = min(1.0, last + inc)

      songs_pos[songs[0][0]] = first
      songs_pos[songs[-1][0]] = last


  x.sort(key=lambda i: songs_pos[i])
