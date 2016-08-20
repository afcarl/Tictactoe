# -*- coding: utf-8 -*-
__author__ = 'Chason'
from random import random
import copy
from ChessBoard import ChessBoard

class StatisticAgent:
    def __init__(self, chess_board, my_flag, enemy_flag):
        self.chess_board = chess_board
        self.my_flag = my_flag
        self.enemy_flag = enemy_flag
        self.sim_times = 1000

    def line2matrix(self, num):
        r = num / self.chess_board.col
        c = num % self.chess_board.col
        return r, c


    def rnd_move(self, board):
        empty = self.chess_board.search_empty_spaces(board)
        empty_count = len(empty)
        if empty_count > 0:
            rnd = (int)(random()*empty_count)
            return self.line2matrix(empty[rnd])
        else:
            return -1, -1

    def make_rnd_move(self, board, flag):
        r, c = self.rnd_move(board)
        if r != -1 and c != -1:
            board[r][c] = flag
            winner = self.chess_board.judge(r, c)
            return winner
        else:
            return -1



    def simulation(self, r, c):
        sim_board = copy.deepcopy(self.chess_board.board)
        sim_chess_board = ChessBoard()
        sim_chess_board.reset_board(sim_board)
        winner = sim_chess_board.make_a_move(r, c, self.my_flag)
        # sim_chess_board.print_board()

        if winner == self.chess_board.draw_flag:
            return 0.0
        elif winner == self.my_flag:
            return 1.0
        win_times = 0
        for i in range(self.sim_times):
            sim_board2 = copy.deepcopy(sim_board)
            sim_chess_board2 = ChessBoard()
            sim_chess_board2.reset_board(sim_board2)
            while True:
                winner = sim_chess_board2.make_rnd_move(self.enemy_flag)
                if winner != None:
                    break
                winner = sim_chess_board2.make_rnd_move(self.my_flag)
                if winner == self.my_flag:
                    win_times += 1
                    break
                elif winner == self.chess_board.draw_flag:
                    break
        return 1.0 * win_times / self.sim_times

    def statistic_move(self):
        empty = self.chess_board.search_empty_spaces(self.chess_board.board)
        scores = []
        for e in empty:
            print 'e =', e
            r, c = self.line2matrix(e)
            scores.append(self.simulation(r, c))
        print scores
        max_score = 0
        max_score_inx = 0
        for i,s in enumerate(scores):
            if s >= max_score:
                max_score = s
                max_score_inx = empty[i]
        return self.line2matrix(max_score_inx)

    def make_statistic_move(self, board, flag):
        r, c = self.statistic_move()
        if r != -1 and c != -1:
            board[r][c] = flag
            winner = self.chess_board.judge(r, c)
            return winner
        else:
            return -1