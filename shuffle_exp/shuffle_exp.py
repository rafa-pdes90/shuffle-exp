from fisher_yates_shuffle import fisher_yates_shuffle as fisher_yates
from sattolo_shuffle import sattolo_shuffle as sattolo
from balanced_shuffle import balanced_shuffle as balanced
from spotify_shuffle import spotify_shuffle as spotify
from my_shuffle import my_shuffle as my

class Song:
  def __init__(self, name, artist, album):
    self.name = name
    self.artist = artist
    self.album = album

  def __str__(self):
    return "{0.name} {0.artist} {0.album}".format(self)

if __name__=='__main__':
  x = [Song(1, "A", "a1"), Song(2, "A", "a2"), Song(3, "B", "b1"), Song(4, "C", "c1"),
      Song(5, "B", "b1"), Song(6, "A", "a1"), Song(7, "D", "d1"), Song(8, "A", "a1"),
      Song(9, "D", "d2")]

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

  hap = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
  print ("\r\nMy Shuffle:")
  for i in range(10000):
    test = list(x)
    my.shuffle(test, ["artist"], [3, 7, 1, 2, 5, 9, 6, 4, 8])
    index = test.index(x[5])
    hap[index+1] += 1
  sum = 0
  for v in hap.values():
    sum += v
  for i in range(1, 10):
    print (i, ": ", (hap[i]/sum)*100, "%")
