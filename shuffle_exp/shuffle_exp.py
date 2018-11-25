from fisher_yates_shuffle import fisher_yates_shuffle as fisher_yates
from sattolo_shuffle import sattolo_shuffle as sattolo
from balanced_shuffle import balanced_shuffle as balanced
from spotify_shuffle import spotify_shuffle as spotify
from my_shuffle import my_shuffle as my
from my_shuffle import my_shuffle_alt as my_alt

from collections import Counter
from timeit import default_timer as timer
import random
import matplotlib.pyplot as plt
import numpy
import statistics

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

def test1(groups):
  playlist_len = 100
  test_count = 1000000
  x = playlist_gen(playlist_len, playlist_len, unique_weight=True)
  weights = sorted([s.weight for s in x], reverse=True)
  
  plt.figure(1)

  # (No variation) Show how often a song is close to its expected position when every weight is unique
  variation = 0
  hap = {w:0 for w in weights}
  hap_alt = {w:0 for w in weights}

  for i in range(test_count):
    test = list(x)
    my.shuffle(test, groups, "weight")

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap[test[j].weight] += 1

  for i in range(test_count):
    test = list(x)
    my_alt.shuffle(test, groups, "weight")

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap_alt[test[j].weight] += 1
  
  percs = [(hap[w]/test_count)*100 for w in weights]
  percs_alt = [(hap_alt[w]/test_count)*100 for w in weights]

  plt.subplot(121)
  plt.gca().set_title('Sem variação')
  plt.plot(weights, percs, label='Triangular Distribution')
  plt.plot(weights, percs_alt, label='Weighted Random S.')
  plt.xticks(numpy.arange(0, playlist_len+1, 0.1*playlist_len))
  plt.yticks(numpy.arange(0, 101, 10))
  plt.axis([0, playlist_len, 0, 100])
  plt.xlabel('Pesos')
  plt.ylabel('%')
  plt.grid(True)
  plt.legend()

  # (10% variation) Show how often a song is close to its expected position when every weight is unique
  variation = max(1, playlist_len * 10/100)
  hap = {w:0 for w in weights}
  hap_alt = {w:0 for w in weights}

  for i in range(test_count):
    test = list(x)
    my.shuffle(test, groups, "weight")

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap[test[j].weight] += 1

  for i in range(test_count):
    test = list(x)
    my_alt.shuffle(test, groups, "weight")

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap_alt[test[j].weight] += 1
  
  percs = [(hap[w]/test_count)*100 for w in weights]
  percs_alt = [(hap_alt[w]/test_count)*100 for w in weights]

  plt.subplot(122)
  plt.gca().set_title('10% de variação')
  plt.plot(weights, percs, label='Triangular Distribution')
  plt.plot(weights, percs_alt, label='Weighted Random S.')
  plt.xticks(numpy.arange(0, playlist_len+1, 0.1*playlist_len))
  plt.yticks(numpy.arange(0, 101, 10))
  plt.axis([0, playlist_len, 0, 100])
  plt.xlabel('Pesos')
  plt.ylabel('%')
  plt.grid(True)
  plt.legend()

  plt.tight_layout()
  plt.savefig('1_1_{0}.png'.format(len(groups)), bbox_inches='tight')
  plt.close(1)

  plt.figure(2)

  # (Others) Show how often a song is close to its expected position when every weight is unique
  variation = max(1, playlist_len * 25/100)
  hap_fisher_yates = {w:0 for w in weights}
  hap_balanced = {w:0 for w in weights}
  hap_spotify = {w:0 for w in weights}

  for i in range(test_count):
    test = list(x)
    fisher_yates.shuffle(test)

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap_fisher_yates[test[j].weight] += 1

  for i in range(test_count):
    test = list(x)
    balanced.shuffle(test, groups)

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap_balanced[test[j].weight] += 1

  for i in range(test_count):
    test = list(x)
    spotify.shuffle(test, groups)

    for j in range(playlist_len):
      if weights[j] - variation <= test[j].weight <= weights[j] + variation:
        hap_spotify[test[j].weight] += 1
  
  percs_fisher_yates = [(hap_fisher_yates[w]/test_count)*100 for w in weights]
  percs_balanced = [(hap_balanced[w]/test_count)*100 for w in weights]
  percs_spotify = [(hap_spotify[w]/test_count)*100 for w in weights]
  
  plt.plot(weights, percs_fisher_yates, label='Fisher-Yates Shuffle')
  plt.plot(weights, percs_balanced, label='Balanced Shuffle')
  plt.plot(weights, percs_spotify, label='Spotify Shuffle')
  plt.xlabel('Pesos')
  plt.ylabel('%')
  plt.grid(True)
  plt.legend()

  plt.tight_layout()
  plt.savefig('1_2_{0}.png'.format(len(groups)), bbox_inches='tight')
  plt.close(2)

def test2(unique, groups):
  test_count = 1000000
  max_len = 10000
  all_len = [0]
  fisher_yates_times = [0]
  balanced_times = [0]
  spotify_times = [0]
  my_times = [0]
  my_alt_times = [0]

  for i in range(int(numpy.log2(max_len)) + 1):
    playlist_len = 2**i
    all_len.append(playlist_len)
    x = playlist_gen(playlist_len, playlist_len, unique_weight=unique)
    
    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      fisher_yates.shuffle(test)
      end = timer()
      times.append(end-start)
    fisher_yates_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      balanced.shuffle(test, groups)
      end = timer()
      times.append(end-start)
    balanced_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      spotify.shuffle(test, groups)
      end = timer()
      times.append(end-start)
    spotify_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      my.shuffle(test, groups, "weight")
      end = timer()
      times.append(end-start)
    my_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      my_alt.shuffle(test, groups, "weight")
      end = timer()
      times.append(end-start)
    my_alt_times.append(statistics.median(times))
  
  plt.figure(1)
  plt.plot(all_len, fisher_yates_times, label='Fisher-Yates Shuffle')
  plt.plot(all_len, balanced_times, label='Balanced Shuffle')
  plt.plot(all_len, spotify_times, label='Spotify Shuffle')
  plt.plot(all_len, my_times, label='Triangular Distribution')
  plt.plot(all_len, my_alt_times, label='Weighted Random S.')
  plt.xlabel('Tamanho da lista')
  plt.ylabel('Tempo em segundos')
  plt.grid(True)
  plt.legend()

  plt.gca().set_title('')
  plt.tight_layout()
  plt.savefig('2_{0}_{1}.png'.format(unique, len(groups)), bbox_inches='tight')
  plt.close(1)

def test3(unique, groups, test_group):
  test_count = 1000000
  max_len = 10000
  all_len = [0]
  fisher_yates_times = [0]
  balanced_times = [0]
  spotify_times = [0]
  my_times = [0]
  my_alt_times = [0]

  for i in range(int(numpy.log2(max_len)) + 1):
    playlist_len = 2**i
    all_len.append(playlist_len)
    x = playlist_gen(playlist_len, playlist_len, unique_weight=unique)
    
    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      fisher_yates.shuffle(test)
      end = timer()
      times.append(end-start)
    fisher_yates_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      balanced.shuffle(test, groups)
      end = timer()
      times.append(end-start)
    balanced_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      spotify.shuffle(test, groups)
      end = timer()
      times.append(end-start)
    spotify_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      my.shuffle(test, groups, "weight")
      end = timer()
      times.append(end-start)
    my_times.append(statistics.median(times))

    times = []
    for i in range(test_count):
      test = list(x)
      start = timer()
      my_alt.shuffle(test, groups, "weight")
      end = timer()
      times.append(end-start)
    my_alt_times.append(statistics.median(times))
  
  plt.figure(1)
  plt.plot(all_len, fisher_yates_times, label='Fisher-Yates Shuffle')
  plt.plot(all_len, balanced_times, label='Balanced Shuffle')
  plt.plot(all_len, spotify_times, label='Spotify Shuffle')
  plt.plot(all_len, my_times, label='Triangular Distribution')
  plt.plot(all_len, my_alt_times, label='Weighted Random S.')
  plt.xlabel('Tamanho da lista')
  plt.ylabel('Tempo em segundos')
  plt.grid(True)
  plt.legend()

  plt.gca().set_title('')
  plt.tight_layout()
  plt.savefig('3_{0}_{1}_{2}.png'.format(unique, len(groups), test_group), bbox_inches='tight')
  plt.close(1)


if __name__=='__main__':
  g1 = "artist"
  g2 = "album"
  s = [g1]
  f = [g1, g2]
  
  test = input("Test: ")

  if test == '1s':
    test1(s)
  if test == '1f':
    test1(f)
  elif test == '2fs':
    test2(False, s)
  elif test == '2ff':
    test2(False, f)
  elif test == '2ts':
    test2(True, s)
  elif test == '2tf':
    test2(True, f)
  elif test == '3fs1':
    test3(False, s, g1)
  elif test == '3fs2':
    test3(False, s, g2)
  elif test == '3ff1':
    test3(False, f, g1)
  elif test == '3ff2':
    test3(False, f, g2)
  elif test == '3ts1':
    test3(True, s, g1)
  elif test == '3ts2':
    test3(True, s, g2)
  elif test == '3tf1':
    test3(True, f, g1)
  elif test == '3tf2':
    test3(True, f, g2)
