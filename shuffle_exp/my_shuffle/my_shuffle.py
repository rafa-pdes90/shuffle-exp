import random

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

    last_weight = float("inf")
    last_pos = 0

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


  x.sort(key=lambda i: songs_pos[i])