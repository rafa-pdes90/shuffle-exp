from fisher_yates_shuffle import fisher_yates_shuffle as fisher_yates
from sattolo_shuffle import sattolo_shuffle as sattolo
from balanced_shuffle import balanced_shuffle as balanced
from spotify_shuffle import spotify_shuffle as spotify
from my_shuffle import my_shuffle as my
from my_shuffle import my_shuffle_alt as my_alt

from collections import Counter
import random
import matplotlib.pyplot as plt

class Song:
  def __init__(self, title, artist, album, weight):
    self.title = title
    self.artist = artist
    self.album = album
    self.weight = weight

  def __str__(self):
    return "{0.title} - {0.artist} - {0.album} - {0.weight}".format(self)

def playlist_gen(song_count, max_weight, unique_weight=False):
  def title_gen(title_len, rel_id):
    prefix = ""

    if title_len > 1:
      new_id = (rel_id - 26) // 26
      prefix = title_gen(title_len - 1, new_id)
    
    sufix = chr((rel_id % 26) + 65)
    return prefix + sufix
  
  playlist = []
  song_id = 0
  artist_count = int(random.triangular(1,song_count))
  artist_rem = song_count - artist_count

  if unique_weight:
    weights = random.sample(range(1, max_weight+1), song_count)
  else:
    weights = [random.randint(1, max_weight) for i in range(song_count)]
  
  for i in range(artist_count):
    print()
    if i < artist_count - 1:
      artist_rem += 1
      count = random.randint(1, artist_rem)
      artist_rem -= count
    else:
      count = artist_rem + 1

    album_count = int(random.triangular(1, count))
    album_rem = count - album_count

    for j in range(album_count):
      if j < album_count - 1:
        album_rem += 1
        count = random.randint(1, album_rem)
        album_rem -= count
      else:
        count = album_rem + 1
      
      while count > 0:
        rel_id = song_id
        title_len = 1

        while rel_id >= 26:
          title_len += 1
          rel_id = (rel_id / 26) - 1
        
        title = title_gen(title_len, song_id)
        song = Song(title, str(i), str(i)+str(j), weights[song_id])
        playlist.append(song)
        song_id += 1
        count -= 1

  return playlist

if __name__=='__main__':
  playlist_len = 100
  test_count = 1000

  # Show how often a song is close to its expected position when every weight is unique
  variation = max(1, playlist_len * 10/100)
  x = playlist_gen(playlist_len, playlist_len, unique_weight=True)
  weights = sorted([s.weight for s in x], reverse=True)
  hap = {w:0 for w in weights}

  for i in range(test_count):
    test = list(x)
    my_alt.shuffle(test, ["artist", "album"], "weight")

    for j in range(playlist_len):
      if test[j].weight <= weights[j] + variation and test[j].weight >= weights[j] - variation:
        hap[test[j].weight] += 1
  
  percs = [(hap[w]/test_count)*100 for w in weights]
  plt.subplot(131)
  plt.plot(weights, percs)

  # Show how often a song is close to its expected position when every weight is not unique
  variation = max(1, playlist_len * 10/100)
  x = playlist_gen(playlist_len, playlist_len, unique_weight=True)
  weighted = sorted(x, key=lambda i: i.weight)
  weights = sorted([s.weight for s in x], reverse=True)
  hap = {i:0 for i in range(1, playlist_len+1)}

  for i in range(test_count):
    test = list(x)
    my_alt.shuffle(test, ["artist", "album"], "weight")

    for j in range(playlist_len):
      if test[j].weight <= weights[j] + variation and test[j].weight >= weights[j] - variation:
        index = weighted.index(test[j]) + 1
        hap[index] += 1
  
  percs = [(hap[i]/test_count)*100 for i in range(1, playlist_len+1)]
  plt.subplot(132)
  plt.plot(range(1,playlist_len+1), percs)


  # (Alternative) Show how often a song is close to its expected position when every weight is not unique
  variation = max(1, playlist_len * 10/100)
  hap = {i:0 for i in range(1, playlist_len+1)}

  for i in range(test_count):
    test = playlist_gen(playlist_len, playlist_len, unique_weight=False)
    weighted = sorted(test, key=lambda i: i.weight)
    weights = [s.weight for s in reversed(weighted)]
    my_alt.shuffle(test, ["artist", "album"], "weight")

    for j in range(playlist_len):
      if test[j].weight <= weights[j] + variation and test[j].weight >= weights[j] - variation:
        index = weighted.index(test[j]) + 1
        hap[index] += 1
  
  percs = [(hap[i]/test_count)*100 for i in range(1, playlist_len+1)]
  plt.subplot(133)
  plt.plot(range(1,playlist_len+1), percs)

  plt.show()

'''
  print ("\r\nMy Shuffle:")
  hap = {i:[] for i in range(len(x))}
  modo = 0
  total = 1 * (10000**modo)
  for i in range(total):
    test = list(x)
    my.shuffle(test, ["artist", "album"], "weight")
    if modo == 0:
      for s in test:
        print(s)
      print()
    else:
      for j in range(len(x)):
        index = test.index(x[j]) + 1
        hap[j].append(index)
  if modo == 1:
    for i in range(len(x)):
      print("\r\n", x[i], ":")
      counts = Counter(hap[i])
      for j in range(1, len(x)+1):
        perc = (counts[j]/len(hap[i]))*100
        print(j, ":", perc)
'''