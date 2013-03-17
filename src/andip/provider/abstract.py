#-*- coding: utf-8 -*-

class AbstractProvider(object):
    def get_word(self, conf):
        raise Exception("abstract method")

    def get_conf(self, word):
        raise Exception("abstract method")
