from fisher_yates_shuffle import fisher_yates_shuffle as fisher_yates
from sattolo_shuffle import sattolo_shuffle as sattolo
from spotify_shuffle import spotify_shuffle as spotify

class Song:
  def __init__(self, name, artist, pos):
    self.name = name
    self.artist = artist
    self.pos = pos


x = [Song(1, "A", 0), Song(2, "A", 1), Song(3,"B", 2), Song(4, "C", 3), Song(5, "B", 4), Song(6, "A", 5), Song(7, "D", 6),
     Song(8, "A", 7), Song(9, "D", 8)]

print ("Original:")
for song in x:
  print(song.name, song.artist)

print ("\r\nFisher-Yates Shuffle:")
test = list(x)
fisher_yates.shuffle(test)
for song in test:
  print(song.name, song.artist)

print ("\r\nSattolo Shuffle:")
test = list(x)
sattolo.shuffle(test)
for song in test:
  print(song.name, song.artist)

print ("\r\nSpotify Shuffle:")
test = list(x)
spotify.shuffle(test)
for song in test:
  print(song.name, song.artist)
