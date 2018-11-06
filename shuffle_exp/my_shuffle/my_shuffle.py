import random
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
  
  songs_groups = sorted(songs_by_y.values(), reverse=False, key=lambda i: statistics.median(getattr(s, w) for s in i))

  for songs in songs_groups:
    if len(y) > 1:
      shuffle(songs, y[1:], w, w_step=w_step)
    else:
      weighted_shuffle(songs, w)

    last_weight = float("inf")
    last_pos = 0.0

    for i in range(len(songs)):
      if songs[i].weight <= last_weight:
        low_lim = 100.0 - (songs[i].weight * w_step)
        up_lim = low_lim + w_step
        last_pos = songs_pos[songs[i]] = random.uniform(low_lim, up_lim)
      else:
        t_step = w_step*(100.0 - last_pos)/100.0
        low_lim = 100.0 - (songs[i].weight * t_step)
        up_lim = low_lim + t_step
        last_pos = songs_pos[songs[i]] = random.uniform(low_lim, up_lim)
      last_weight = songs[i].weight
      
    all_pos = songs_pos.values()
    min_pos = min(all_pos)
    max_pos = max(all_pos)
    offset = random.uniform(0.0 - min_pos, 100.0 - max_pos)
    
    for key in songs_pos:
      songs_pos[key] += offset

  x.sort(key=lambda i: songs_pos[i])
