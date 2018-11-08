from fisher_yates_shuffle import fisher_yates_shuffle as fisher_yates
from sattolo_shuffle import sattolo_shuffle as sattolo
from balanced_shuffle import balanced_shuffle as balanced
from spotify_shuffle import spotify_shuffle as spotify
from my_shuffle import my_shuffle as my

from collections import Counter

class Song:
  def __init__(self, name, artist, album, weight):
    self.name = name
    self.artist = artist
    self.album = album
    self.weight = weight

  def __str__(self):
    return "{0.name} {0.artist} {0.album} {0.weight}".format(self)

if __name__=='__main__':
  x = [Song(1, "A", "a1", 3), Song(2, "A", "a2", 7), Song(3, "B", "b1", 1), Song(4, "C", "c1", 2),
      Song(5, "B", "b1", 5), Song(6, "A", "a1", 9), Song(7, "D", "d1", 6), Song(8, "A", "a1", 4),
      Song(9, "D", "d2", 8)]

  print ("Original:")
  for song in x:
    print(song)

  print ("\r\nFisher-Yates Shuffle:")
  test = list(x)
  fisher_yates.shuffle(test)
  for song in test:
    print(song)

  print ("\r\nSattolo Shuffle:")
  test = list(x)
  sattolo.shuffle(test)
  for song in test:
    print(song)

  print ("\r\nBalanced Shuffle:")
  test = list(x)
  balanced.shuffle(test, ["artist", "album"])
  for song in test:
    print(song)

  print ("\r\nSpotify Shuffle:")
  test = list(x)
  spotify.shuffle(test, ["artist", "album"])
  for song in test:
    print(song)

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
