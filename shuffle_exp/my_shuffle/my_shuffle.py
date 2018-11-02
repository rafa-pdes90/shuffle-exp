import random

def weigthed_shuffle(items, items_pos, weights):
  items.sort(key=lambda i: -random.random() ** (1.0 / weights[items_pos[i]]))

def shuffle(x, y, w):
  songs_by_y = {}
  songs_pos = {}
  
  for i in range(len(x)):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(x[i])
    songs_pos[x[i]] = i
  
  for songs in songs_by_y.values():
    if len(y) > 1:
      shuffle(songs, y[1:], w)
    else:
      weigthed_shuffle(songs, songs_pos, w)

    song_count = len(songs)
    appear_base = 100.0/song_count
    appear_lim = appear_base - 100.0/(song_count+1)
    appear_max, appear_min = min(100.0, appear_base + appear_lim), max(0.0, appear_base - appear_lim)
    
    offset = random.uniform(0.0, 100.0)

    last_pos = songs_pos[songs[0]] = offset    
    for i in range (1, song_count):
      last_pos = songs_pos[songs[i]] = (last_pos + random.uniform(appear_min, appear_max)) % 100

  x.sort(key=lambda i: songs_pos[i])