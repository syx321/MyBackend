#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from surakarta.game import Game

class Surakarta():
    def __init__(self):
        self.__board = Game(1)
        self.__board.reset_board()

    def fire(self, player, location, *kw):
        self.__board.do_move(location)
        result = self.__board.has_winner()
        board = self.__board.get_board()

        return board, result[1]

    def rollback(self):
        self.__board.cancel_move()
