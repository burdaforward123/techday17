# -*- coding: UTF-8 -*-
import pygame
import StringIO
import traceback
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from random import randint
import datetime as dt
import sys, traceback
reload(sys)  
sys.setdefaultencoding('utf8')

class VoiceSynthesizer(object):

    voices = ['Hans',
              'Marlene']

    greetings = ["Hallo",
                 "Moin",
                 "Servus",
                 "Guten tag",
                 "Huhu",
                 "Na",
                 "Hi",
                 "Tach"]

    smalltalk = ["schön dich zu sehen",
                 "du bist ein könig",
                 "ich wünsch dir einen schönen tag",
                 "ich hoffe du hast einen schönen tag",
                 "heute nur mit reservierung",
                 "ich habe dich vermisst",
                 "du schaust aber heute super aus",
                 "interessante frisur",
                 "wenn ich könnte, würde ich dich umarmen",
                 "<prosody rate='x-slow'><lang xml:lang='es-ES'>hasta la vista, <break time='100ms'/> baby</lang></prosody>",
                 "<prosody rate='x-slow'><lang xml:lang='en-GB'>take care and good bye</lang></prosody>",
                 "man sieht sich",
                 "wir sehen uns",
                 "bis später",
                 "ich hab dich lieb",
                 "du bist die nummer eins",
                 "du bist super",
                 "endlich bist du da",
                 "du hast abgenommen, toll!",
                 "tolle frisur",
                 "du hast dein Meeting verpasst",
                 "Alle warten schon auf dich",
                 "Hubert Burda hat versucht dich zu erreichen",
                 "danke für die tolle Nacht!",
                 "tolle figur"]
    
    def is_morning(self):
        h = dt.datetime.now().hour
        return h < 10

    def is_evening(self):
        h = dt.datetime.now().hour
        return h > 16
    
    def is_monday(self):
        d = datetime.datetime.today().weekday()
        return d==0

    def is_friday(self):
        d = datetime.datetime.today().weekday()
        return d==4

    def rand_elem(self, some_list):
        r = randint(0, some_list.__len__()-1)
        return some_list[r];

    # %greetings %name, %smalltalk
    # volume='x-loud', pitch='x-high'
    def say_hello(self, name):

        preambel=''
        if self.is_morning():
            preambel = "Guten Morgen"
        elif self.is_evening():
            preambel = "Guten Abend"
        else:
            preambel = self.rand_elem(self.greetings) 

        sentence = '<prosody rate="100%">' + \
		preambel + '</prosody>' + \
		" <break time='10ms'/> " + name + \
		" <break time='500ms'/>  " + self.rand_elem(self.smalltalk)
 
        self.say(sentence.encode('utf-8'))

    def __init__(self, volume=1.0):
       pygame.mixer.init()
       self._volume = volume
       session = Session(profile_name="default")
       self.__polly = session.client("polly")

    def _getVolume(self):
       return self._volume

    def say(self, text):
       self._synthesize(text)

    def _synthesize(self, text):
       # Implementation specific synthesis
       try:
          # Request speech synthesis
          response = self.__polly.synthesize_speech(Text='<speak>' + text + '</speak>', 
                        OutputFormat="ogg_vorbis", VoiceId=self.rand_elem(self.voices), TextType="ssml") #"Marlene"
       except (BotoCoreError, ClientError) as error:
          # The service returned an error
          print(error)
          exc_type, exc_value, exc_traceback = sys.exc_info()
          traceback.print_exception(exc_type, exc_value, exc_traceback,
          limit=5, file=sys.stdout)

       # Access the audio stream from the response
       if "AudioStream" in response:
          # Note: Closing the stream is important as the service throttles on the
          # number of parallel connections. Here we are using contextlib.closing to
          # ensure the close method of the stream object will be called automatically
          # at the end of the with statement's scope.
          with closing(response["AudioStream"]) as stream:
             data = stream.read()
             filelike = StringIO.StringIO(data)  # Gives you a file-like object
             sound = pygame.mixer.Sound(filelike)
             sound.set_volume(self._getVolume())
             sound.play()
             while pygame.mixer.get_busy() == True:
                continue



#if __name__ == "__main__":
#
#    # Test code
#    debugging = False
#    try:
#       synthesizer = VoiceSynthesizer(1.0)
#       synthesizer.say_hello("Sven")
#    except:
#       print "exception occurred!"
#       exc_type, exc_value, exc_traceback = sys.exc_info()
#       traceback.print_exception(exc_type, exc_value, exc_traceback,
#       limit=5, file=sys.stdout)
#
#    print "done"
