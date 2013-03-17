#-*- coding: utf-8 -*-

""" TODO:
 - kodowanie znaków
 - get_dump
"""

import re, copy
import urllib as url
import sqlite3 as db
from andip.provider import AbstractProvider

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class WikiProvider(AbstractProvider):
    def __init__(self, url, database):
        self.__apiUrl = url
        self.__databaseName = '../data/' + database + '.db'
        
    def _get_conf_from_database(self, result):
        assert isinstance(result, str)
        assert len(result) > 0

        con = None
        try:
            con = db.connect(self.__databaseName)
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * FROM indeks WHERE word="%s"' % result)
        
            data = cur.fetchone()
            if data == None:
                return None
            
            type = data['type']
            cur.execute('SELECT * FROM %s WHERE result="%s"' % (type, result))
            data = cur.fetchone()
            
            del data['result']
            word = data['word']
            del data['word']
            return [type, word, data]

        except db.Error, e:
            print "Database connection error %s:" % e.args[0]
            
        finally:
            if con:
                con.close()
                
    def _get_word_from_database(self, type, word, conf):
        assert isinstance(word, str)
        assert len(word) > 0
        assert isinstance(type, str)
        assert len(type) > 0
        assert isinstance(conf, dict)
        assert len(conf) > 0
        
        con = None
        try:
            con = db.connect(self.__databaseName)
            con.row_factory = dict_factory
            cur = con.cursor()

#            args = [k for (k, v) in conf.iteritems()]
#            vals = [v for (k, v) in conf.iteritems()]
            where = ''
            for (i, j) in conf.iteritems():
                where += '"%s"="%s" AND ' % (i, j)
#            where = where[:-5]
            where += '"word"="%s" ' % word
            cur.execute('SELECT result FROM %s WHERE %s' % (type, where))

            data = cur.fetchone()
            if data != None:
                return data['result']
            else:
                return None

        except db.Error, e:
            print "Database connection error %s:" % e.args[0]
            
        finally:
            if con:
                con.close()
                
    def _insert_data_into_database(self, type, word, conf):
        assert isinstance(word, str)
        assert len(word) > 0
        assert isinstance(type, str)
        assert len(type) > 0
        assert isinstance(conf, dict)
        assert len(conf) > 0
        
        con = None
        try:
            con = db.connect(self.__databaseName)
            cur = con.cursor()

            cols = ''
            vals = ''
            for (i, j) in conf.iteritems():
                cols += '%s, ' % i  
                vals += '%s, ' % j
            
            cols += 'word'
            vals += '%s' % word

            print cols
            print vals
            cur.execute('INSERT INTO %s (%s) VALUES(%s)' % (type, cols, vals))
            cur.execute('INSERT INTO indeks (word, type) VALUES(%s, %s)' % (word, type))
            con.commit()
        except db.Error, e:
            print "Database connection error %s:" % e.args[0]
            
        finally:
            if con:
                con.close()
        
    def _get_data_from_api(self, word):
        assert isinstance(word, str)
        
        return url.urlopen(self.__apiUrl + 'w/api.php?format=xml&action=query&prop=revisions&rvprop=content&titles=' + word).read()
    
class PlWikiProvider(WikiProvider):
    
    def __init__(self):
        WikiProvider.__init__(self, "http://pl.wiktionary.org/", "pl")
        self.__schema_adjective = None

    def __save_conf_noun(self, word, data):
        pass
    
    def __save_conf_verb(self, word, data):
        pass
    
    def __save_conf_adjective(self, word, data):
        if len(data) == 0:
            raise Exception("API error: couldn't find adjective")
        
#        words = data[0].replace("|", "").split("\n")
#        
#        assert len(words) > 0
#        word = words[0]
#        
#        # generowanie stopniowania
#        if word == '' or word == 'brak':
#            # brak stopniowania?
#            pass
#        else:
##            print word # stopniowanie na podstawie podanego drugiego stopnia
#            pass
        
#        data = {'stopien' : 'podstawowy'}
#        # generowanie odmian
        if self.__schema_adjective is None:
            self.__schema_adjective = self._load("../data/adjective_schema")

        last_letter = word[len(word) - 1]
#        print base_word, last_letter
#        if last_letter == 'y' or last_letter == 'i':
        retval = copy.deepcopy(self.__schema_adjective[last_letter])
#            print retval['przypadek']['mianownik']['liczba']['mnoga']['rodzaj']['m']
#            for przyp in retval['przypadek']:
#                for licz in retval['przypadek'][przyp]['liczba']:
#                    for rodz in retval['przypadek'][przyp]['liczba'][licz]['rodzaj']:
#                        retval['przypadek'][przyp]['liczba'][licz]['rodzaj'][rodz] = base_word[0:len(base_word) - 1] + retval['przypadek'][przyp]['liczba'][licz]['rodzaj'][rodz]
        try:
            con = db.connect("../data/pl.db")
            cur = con.cursor()
#            cur.execute('CREATE TABLE przymiotnik_schemat (sufix TEXT, przypadek TEXT, liczba TEXT, rodzaj TEXT, result TEXT)')
            for przyp in retval['przypadek']:
                for licz in retval['przypadek'][przyp]['liczba']:
                    for rodz in retval['przypadek'][przyp]['liczba'][licz]['rodzaj']:
                        if licz == 'pojedyncza':
                            rodza = {
                                "m" : "męski",
                                "ż" : "żeński",
                                "n" : "nijaki"
                            }.get(rodz)
                        else:
                            rodza = {
                                "m" : "męskoosobowy",
                                "nm" : "niemęskoosobowy"
                            }.get(rodz)
                            
                        print 'INSERT INTO przymiotnik_schemat (przypadek, liczba, rodzaj, sufix, result) VALUES (%s, %s, %s, %s, %s)' % (last_letter, przyp, licz, rodza, retval['przypadek'][przyp]['liczba'][licz]['rodzaj'][rodz])
                        cur.execute('INSERT INTO przymiotnik_schemat VALUES ("%s", "%s", "%s", "%s", "%s")' % (last_letter, przyp, licz, rodza, retval['przypadek'][przyp]['liczba'][licz]['rodzaj'][rodz]))
                        con.commit()
                
#            cur.execute('INSERT INTO indeks (word, type) VALUES(%s, %s)' % (word, type))
#            cur.execute('INSERT INTO przymiotnik ("word") VALUES ("dupa")')
#            con.commit()
#            print cur.fetchall()
        except db.Error, e:
            print "Database connection error %s:" % e.args[0]
            
        finally:
            if con:
                con.close() 
                
#            print base_word, 'haskey', base_word[len(base_word) - 2]
#            print retval['przypadek']['mianownik']['liczba']['mnoga']['rodzaj']['m']
#            if self.__schema_adjective['exceptions'].has_key(base_word[len(base_word) - 2]) == 1:
#                tmp = list(retval['przypadek']['mianownik']['liczba']['mnoga']['rodzaj']['m'])
#                tmp[len(base_word) - 2]  = self.__schema_adjective['exceptions'][base_word[len(base_word) - 2]]
#                retval['przypadek']['mianownik']['liczba']['mnoga']['rodzaj']['m'] = "".join(tmp)
#                
#                tmp = list(retval['przypadek']['wołacz']['liczba']['mnoga']['rodzaj']['m'])
#                tmp[len(base_word) - 2]  = self.__schema_adjective['exceptions'][base_word[len(base_word) - 2]]
#                retval['przypadek']['wołacz']['liczba']['mnoga']['rodzaj']['m'] = "".join(tmp)
##                print retval['przypadek']['mianownik']['liczba']['mnoga']['rodzaj']['m']
##                print retval['przypadek']['wołacz']['liczba']['mnoga']['rodzaj']['m']
#        else:
#            raise Exception("adjective is not regular!")


    def get_conf(self, word):
        
        data = self._get_conf_from_database(word)
        if data != None:
            return data
        else:
            return 'data not found: %s' % word
    
    def get_word(self, config, cycle = False):
        '''
            Conf is a configuration that user chose to get information about word.
            It's a touple, that first element determines type of word, second is the word alone,
            and the third is a dictionary that contains details about form of word we want to have
        
        '''
        assert isinstance(config, tuple)
        assert len(config) == 3
        type, word, conf = config

        assert isinstance(type, str)
        assert isinstance(word, str)
        assert isinstance(conf, dict)

        
        # searching in database
        data = self._get_word_from_database(type, word, conf)
        if data != None or cycle == True:
            return data
        
        # creating config using wiki API, adding to database
        data = self._get_data_from_api(word)

        wikiType = re.findall("-([^-]*)-polski", data)
        if len(wikiType) == 0 or wikiType[0] != type:
            raise Exception("data not found: %s" % word)
        
        switch = {
            'przymiotnik':  self.__save_conf_adjective,
            'czasownik':    self.__save_conf_verb,
            'rzeczownik':   self.__save_conf_noun #
        }.get(type)(word, re.findall("\{\{odmiana-" + type + "-polski([^\}]*)\}\}", data));
        return self.get_word(config, True)

    def get_dump(self, word = None, conf = None):
        """
        Dump data of a specified word in a string recognazible by FileProvider.
        @param word: a word to dump
        @param conf: restric dump to a specified configuration
        @return: string in a JSON format
        """
        pass








