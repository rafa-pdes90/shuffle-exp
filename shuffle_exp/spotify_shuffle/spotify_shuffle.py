import random

def shuffle(x, y):
  songs_by_y = {}
  songs_pos = {}
  
  for song in x:
    y_attrib = getattr(song, y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = []
    songs_by_y[y_attrib].append(song)

  for songs in songs_by_y.values():
    if len(y) > 1:
      shuffle(songs, y[1:])
    else:
      random.shuffle(songs)

    song_count = len(songs)
    appear_base = 100.0/song_count
    appear_lim = appear_base - 100.0/(song_count+1)
    appear_max, appear_min = min(100.0, appear_base + appear_lim), max(0.0, appear_base - appear_lim)
    
    offset = random.uniform(0.0, 100.0)

    songs_pos[songs[0]] = offset
    
    for i in range (1, song_count):
      songs_pos[songs[i]] = (songs_pos[songs[i-1]] + random.uniform(appear_min, appear_max)) % 100

  x.sort(key=lambda i: songs_pos[i])
