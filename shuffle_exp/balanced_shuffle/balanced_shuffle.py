import random

def fill(songs, max_count):
  s_count = len(songs)
  n = max_count
  k = min((max_count - s_count), s_count)
  if k == s_count and 2*s_count < max_count:
    s_count = -s_count

  while k > 0:
    reg_r = n/k
    deviation = 0.1 * n
    r = int(random.uniform(max(1.0, reg_r - deviation), min(n-k+1 , reg_r + deviation)))
    
    if s_count > 0:
      index = max_count - n
      songs.insert(index, None)
    else:
      index = max_count - n + 1
      songs[index:index] = [None for i in range(r)]

    n -= r
    k -= 1
  
  offset = random.randrange(max_count)
  songs = songs[-offset:] + songs[:-offset]

def merge(songs_by_y, max_count, y):
  songs_pos = {}
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
        songs_pos[song] = index
      last_song = column[0]
    else:
      for song in column:
        index += 1
        songs_pos[song] = index
      last_song = column[-1]

  return songs_pos

def shuffle(x, y):
  songs_by_y = {}
  
  for song in x:
    y_attrib = getattr(song, y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(song)

  max_count = len(max(songs_by_y.values(), key=lambda s: len(s)))

  for songs in songs_by_y.values():
    if len(y) > 1:
      shuffle(songs, y[1:])
    else:
      random.shuffle(songs)

    fill(songs, max_count)

  songs_pos = merge(songs_by_y, max_count, y[0])
  
  x.sort(key=lambda i: songs_pos[i])
