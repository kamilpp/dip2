# -*- coding: utf-8 -*-

from andip import AnDiP
#from andip.provider import FileProvider
from andip.provider import PlWikiProvider

#ad = AnDiP(FileProvider("../data/polish"))
ad = AnDiP(PlWikiProvider())

#print 'opisany', ad.get_word(('przymiotnik', 'opis', {'liczba': 'pojedyncza', 'rodzaj': 'm'}))
#print 'opisane', ad.get_word(('przymiotnik', 'opis', {'liczba': 'mnoga', 'rodzaj': 'm'}))
#print 'opisana', ad.get_word(('przymiotnik', 'opis', {'liczba': 'pojedyncza', 'rodzaj': 'ż'}))
#print 'opisane', ad.get_word(('przymiotnik', 'opis', {'liczba': 'mnoga', 'rodzaj': 'ż'}))
#
#print ad.get_word(("czasownik", "występować", {'aspekt': 'dokonane', 'forma': 'czas teraźniejszy', 'liczba': 'mnoga', 'osoba': 'trzecia'}))
#print ad.get_word(("czasownik", "występować", {'aspekt': 'dokonane', 'forma': 'czas przeszły', 'liczba': 'mnoga', 'osoba': 'trzecia'}))
#
#print ad.get_word("występować")
#print ad.get_word("srać")

#print ad.get_conf("występować")
#print ad.get_conf("srać")
#print ad.get_conf("piękny")
print ad.get_conf("zdrowi")
#print ad.get_conf("zachodni")
print ad.get_conf("miła")
#print ad.get_conf("zachodni")
#print ad.get_conf("żałosny")
#print ad.get_conf("żółty")
#print ad.get_conf("zdrów")

#print ad.get_word(('przymiotnik', 'miły', {'przypadek' : 'mianownik', 'liczba' : 'mnoga', 'rodzaj' : 'męskoosobowy'}))
print ad.get_word(('przymiotnik', 'głupi', {'przypadek' : 'mianownik', 'liczba' : 'mnoga', 'rodzaj' : 'męskoosobowy'}))
#
#print ad.get_word(('przymiotnik', 'żółty', {'przypadek': 'miejscownik', 'liczba': 'mnoga', 'rodzaj': 'm' }))
