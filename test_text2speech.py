#! /usr/bin/env python

from text2speech import VoiceSynthesizer

# Test code
try:
   name = "Mister Robot"
   volume = 1.0

   synthesizer = VoiceSynthesizer(volume)
   synthesizer.say_hello(name)
except:
   print "exception occurred!"
   exc_type, exc_value, exc_traceback = sys.exc_info()
   traceback.print_exception(exc_type, exc_value, exc_traceback,
   limit=5, file=sys.stdout)
