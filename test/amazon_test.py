#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import amazons
import numpy as np
from unittest import TestCase

class TestAmazon(TestCase):
    def test_init(self):

        # 实例化单元测试
        a = amazons.Amazons()
        default_board = np.zeros((10,10), dtype=np.int)

        # 初始化先手方棋子位置
        default_board[0, 3] = 1
        default_board[0, 6] = 1
        default_board[3, 0] = 1
        default_board[3, 9] = 1
        # 初始化后手方棋子位置
        default_board[6, 0] = 2
        default_board[9, 3] = 2
        default_board[9, 6] = 2
        default_board[6, 9] = 2

        np.testing.assert_array_equal(a.getBoard(), default_board.reshape((-1,)))

class TestAmazonMove(TestCase):
    def test_move():
        
