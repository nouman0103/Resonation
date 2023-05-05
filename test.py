import vlc
import timeit

musicObject = vlc.MediaPlayer("./__audio.mp3")

# Define a lambda function that calls musicObject.play()
play_music = lambda: musicObject.play()

# Measure the time taken to play the music 10 times
t = timeit.timeit(play_music, number=10)

print("Time taken to play the music:", t)
