# -*- coding: utf-8 -*-

from andip.provider import AbstractProvider

class AnDiP(object):
	def __init__(self, provider):
		assert isinstance(provider, AbstractProvider)

		self.__provider = provider

	def get_word(self, conf):
		"""
		Get a specified word from a dictionary.

		@param conf a tuple build from three parts: part of a speech, base word and dict of properties

		@return word in a specified configuration
		"""

		return self.__provider.get_word(conf)

	def get_conf(self, word):
		"""
		Get the configuration for a given word.

		Each configuration is a tuple build from three parts:
		- part of a speech
		- base word
		- dict of properties

		@return a list with configurations
		"""

		return self.__provider.get_conf(word)
