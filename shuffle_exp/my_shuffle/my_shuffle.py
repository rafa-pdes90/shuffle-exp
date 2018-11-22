import random

def shuffle(x, y, w):
  def pos(song, weight, w_step):
    mode = 100.0 - (getattr(song, weight) - random.random())*w_step
    return random.triangular(0.0, 100.0, mode)
  
  w_max = max([getattr(x[i], w) for i in range(len(x))])
  w_step = 100.0 / w_max
  x.sort(key=lambda i: pos(i, w, w_step))
  weighted_shuffle(x, y, w)

def weighted_shuffle(x, y, w):
  songs_by_y = {}
  pos_by_y = {}
  song_count = len(x)
  
  for i in range(song_count):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
      pos_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(x[i])
    pos_by_y[y_attrib].append(i)

  if len(songs_by_y) > 1:
    songs_pos = {}
    g_step = 1.0 / song_count

    for y_key in songs_by_y:
      songs = songs_by_y[y_key]
      pos = pos_by_y[y_key]

      if len(y) > 1:
        weighted_shuffle(songs, y[1:], w)
      
      i = 0
      j = len(songs) - 1
      lim_min = 0.0
      lim_max = 1.0

      while i < j:
        first = pos[i]/(song_count-1)
        last = pos[j]/(song_count-1)
        sub_count = j-i + 1
        min_gap = sub_count * g_step
        
        if (last - first) < min_gap:
          max_gap = (sub_count+1) * g_step
          inc = random.uniform(min_gap, max_gap)/2
          temp = max(lim_min, first - inc)
          effective_inc = first - temp
          if effective_inc < inc:
            inc += inc - effective_inc
          first = temp
          last = min(lim_max, last + inc)

        lim_min = songs_pos[songs[i]] = first
        lim_max = songs_pos[songs[j]] = last
        i += 1
        j -= 1
      
      if i == j:
        songs_pos[songs[i]] = pos[i]/(song_count-1)

    x.sort(key=lambda i: songs_pos[i])
  elif len(y) > 1:
    weighted_shuffle(x, y[1:], w)
