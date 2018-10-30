import random

def shuffle(x, y):
  songs_by_y = {}
  songs_pos = {}
  
  for song in x:
    y_attrib = getattr(song, y[0])
    if y_attrib not in songs_by_y:
      songs_by_y[y_attrib] = list()
    songs_by_y[y_attrib].append(song)

  for songs in songs_by_y.values():
    song_count = len(songs)
    appear_base = 100/song_count
    appear_lim = appear_base - 100/(song_count+1)
    appear_max, appear_min = appear_base + appear_lim, appear_base - appear_lim
    
    offset_lim = 100.0 - (appear_max * (song_count - 1))
    offset = random.uniform(0, offset_lim)

    if len(y) > 1:
      shuffle(songs, y[1:])

    random.shuffle(songs)

    songs_pos[songs[0]] = offset
    
    for i in range (1, song_count):
      songs_pos[songs[i]] = songs_pos[songs[i-1]] + random.uniform(appear_min, appear_max)

  x.sort(key=lambda i: songs_pos[i])
