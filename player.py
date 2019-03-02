import pygame.mixer


def produce_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    :param music_file: (file) file which contains music
    :return: none
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print("Music file %s loaded!" % music_file)
    except pygame.error:
        print("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


def play(music_file):
    """
    This function set options of mixer, starts producing music and catches exceptions
    :param music_file: (file) file which contains music
    :return:
    """
    print("playing music")
    freq = 40100  # audio CD quality
    # So, here was 44100 but it gain very strange messages, but music was in better quality
    # ALSA lib pcm.c:7963:(snd_pcm_recover) under run occurred
    bitsize = -16  # unsigned 16 bit
    channels = 1  # 1 is mono, 2 is stereo
    buffer = 1024  # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    try:
        produce_music(music_file)
    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        # (works only in console mode)
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit
