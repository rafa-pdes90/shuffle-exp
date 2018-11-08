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
  songs_pos = {}
  song_count = len(x)
  
  for i in range(song_count):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(x[i])
    songs_pos[x[i]] = i

  songs_list = songs_by_y.values()

  if len(songs_list) > 1:
    g_step = 1.0 / song_count

    for songs in songs_list:
      if len(y) > 1:
        weighted_shuffle(songs, y[1:], w)
      
      i = 0
      j = len(songs) - 1
      lim_min = 0.0
      lim_max = 1.0

      while i < j:
        first = songs_pos[songs[i]]/(song_count-1)
        last = songs_pos[songs[j]]/(song_count-1)
        sub_count = j-i + 1
        min_gap = sub_count * g_step
        
        if (last - first) < min_gap:
          max_gap = (sub_count+1) * g_step
          inc = random.uniform(min_gap, max_gap)/2
          first = max(lim_min, first - inc)
          last = min(lim_max, last + inc)

        lim_min = songs_pos[songs[i]] = first
        lim_max = songs_pos[songs[j]] = last
        i += 1
        j -= 1
      
      if i == j:
        songs_pos[songs[i]] = songs_pos[songs[i]]/(song_count-1)

    x.sort(key=lambda i: songs_pos[i])
  elif len(y) > 1:
    weighted_shuffle(x, y[1:], w)
