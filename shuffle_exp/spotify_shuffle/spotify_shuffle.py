import random

def fisher_yates_shuffle(x):
  for i in range(len(x)-1, 0, -1):
    j = random.randrange(i + 1)
    x[i], x[j] = x[j], x[i]

def shuffle(x):
  songs_by_artists = {}
  
  for song in x:
    if song.artist not in songs_by_artists:
      songs_by_artists[song.artist] = list()
    songs_by_artists[song.artist].append(song)

  for songs in songs_by_artists.values():
    song_count = len(songs)
    appear_base = 100/song_count
    appear_lim = appear_base - 100/(song_count+1)
    appear_max, appear_min = appear_base + appear_lim, appear_base - appear_lim
    
    offset_lim = 100.0 - (appear_max * (song_count - 1))
    offset = random.uniform(0, offset_lim)

    fisher_yates_shuffle(songs)

    songs[0].pos = offset
    
    for i in range (1, song_count):
      songs[i].pos = songs[i-1].pos + random.uniform(appear_min, appear_max)

  x.sort(key=lambda i: i.pos)
