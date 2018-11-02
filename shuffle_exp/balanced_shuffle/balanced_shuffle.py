import random

def fill(songs, max_count):
  s_count = len(songs)
  n = max_count
  k = min((max_count - s_count), s_count)
  if k == s_count and 2*s_count < max_count:
    s_count = -s_count
  
  while k > 0:
    if k > 1:
      reg_r = n/k
      deviation = random.random() * reg_r
      r = int(random.uniform(max(1.0, reg_r - deviation), min(n-k+1 , reg_r + deviation)))
    else:
      r = n
    
    if s_count > 0:
      index = max_count - n
      songs.insert(index, None)
    else:
      index = max_count - n + 1
      songs[index:index] = [None for i in range(r)]

    n -= r
    k -= 1
  
  offset = random.randrange(max_count)
  songs[:] = songs[-offset:] + songs[:-offset]

def merge(x, songs_by_y, songs_pos, max_count, y):
  index = -1
  last_song = None

  for i in range(max_count):
    column = []

    for songs in songs_by_y.values():
      if songs[i] is not None:
        column.append(songs[i])
    
    random.shuffle(column)
    
    if last_song is not None and getattr(column[0], y) == getattr(last_song, y):
      for song in column[1:] + column[:1]:
        index += 1
        old_pos = songs_pos.pop(song)
        if old_pos != index:
          songs_pos[x[index]] = old_pos
          x[old_pos], x[index] = x[index], x[old_pos]
      last_song = column[0]
    else:
      for song in column:
        index += 1
        old_pos = songs_pos.pop(song)
        if old_pos != index:
          songs_pos[x[index]] = old_pos
          x[old_pos], x[index] = x[index], x[old_pos]
      last_song = column[-1]

def shuffle(x, y):
  songs_by_y = {}
  songs_pos = {}
  
  for i in range(len(x)):
    y_attrib = getattr(x[i], y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(x[i])
    songs_pos[x[i]] = i

  max_count = len(max(songs_by_y.values(), key=lambda s: len(s)))

  for songs in songs_by_y.values():
    if len(y) > 1:
      shuffle(songs, y[1:])
    else:
      random.shuffle(songs)

    fill(songs, max_count)
  
  merge(x, songs_by_y, songs_pos, max_count, y[0])
