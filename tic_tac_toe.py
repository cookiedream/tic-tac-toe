import numpy as np
import random



# 棋盤函數，每次落子後顯示棋盤
def show(chessboard):
    for i in range(len(chessboard)):
        mark = ' '
        row = chessboard[i]
        for j in row:
            mark = mark + tag[j + 1] + ' ' 
        print(mark)


# 判斷棋盤是否還有空位
def empty(chessboard, position):
    for point in position:
        if chessboard[point[0]][point[1]] == 0:
            return True
    return False



def alpha_beta(chessboard, win, position, now_player, next_player, alpha, beta):
    
    # 終止條件
    winner = terminal(chessboard, win, position)
    if winner != 0:
        return winner
    elif empty(chessboard, position) == False:
        return 0
    
    
    
    for i in range(len(position)):
        temp = position[i]
        if chessboard[temp[0]][temp[1]] == 0:
            chessboard[temp[0]][temp[1]] = now_player
            
            test = alpha_beta(chessboard, win, position, next_player, now_player, alpha, beta)
            
            chessboard[temp[0]][temp[1]] = 0
            
            
            # 如果現在是電腦 , Max玩家 , 修改alpha
            if now_player == 1:
                if test > alpha:
                    alpha = test
                if alpha >= beta:
                    return alpha
                
                
            # 如果现在是玩家,Min玩家,修改beta值
            else:
                if test < beta:
                    beta = test
                if alpha >= beta:
                    return alpha

                
    # # 修改上一個node的值
    # if now_player == 1:
    #     node = alpha
    # else:
    #     node = beta
    # return node


# 評估函數，根據遊戲規則計算分數
def evaluate(chessboard, win, position):
    score = 0
    for line in win:
        computer_count = 0
        palyer_count = 0
        empty_cells = 0
        for i in line:
            row, col = position[i]
            if chessboard[row][col] == 1:
                computer_count += 1
            elif chessboard[row][col] == -1:
                palyer_count += 1
            else:
                empty_cells += 1

        if computer_count == 3:
            score += 100
        elif computer_count == 2 and empty_cells == 1:
            score += 10
        elif computer_count == 1 and empty_cells == 2:
            score += 1

        if palyer_count == 3:
            score -= 100
        elif palyer_count == 2 and empty_cells == 1:
            score -= 10
        elif palyer_count == 1 and empty_cells == 2:
            score -= 1

    return score

# 判斷是否產生贏家
def terminal(chessboard, win, position):
    for line in win:
        m1,n1 = position[line[0]][0],position[line[0]][1]
        m2,n2 = position[line[1]][0],position[line[1]][1]
        m3,n3 = position[line[2]][0],position[line[2]][1]
        if chessboard[m1][n1] == chessboard[m2][n2] == chessboard[m3][n3] == -1:
            return -1
        elif chessboard[m1][n1] == chessboard[m2][n2] == chessboard[m3][n3] == 1:
            return 1
    return 0


# 修改computer_move函數以使用新的評估函數
def computer_move(chessboard, win, position):
    val = -2
    move = []
    for i in range(len(position)):
        temp = position[i]
        if chessboard[temp[0]][temp[1]] == 0:
            chessboard[temp[0]][temp[1]] = 1  # 假設電腦走該位置

            if terminal(chessboard, win, position) == 1:
                return temp, i

            # 計算分數
            score = evaluate(chessboard, win, position)
            chessboard[temp[0]][temp[1]] = 0  # 將該位置清0

            if score > val:
                val = score
                move = [temp]
            elif score == val:
                move.append(temp)

    cmove = random.choice(move)
    for j in range(len(position)):
        if cmove == position[j]:
            return cmove, j
        
if __name__ == '__main__':
    chessboard = [[0,0,0],[0,0,0],[0,0,0]]
    
    position =[[0,0],[0,1],[0,2],
            [1,0],[1,1],[1,2],
            [2,0],[2,1],[2,2]]
    
    win = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6))
    tag = ['o', '.', 'x']
    result = ['o勝!', '和局', 'x勝!']
    player = -1     # 玩家為-1
    computer = 1    # 電腦為1
    first = input("o玩家先手，x電腦先手:")
    if first == "o":
        next_move = player 
    elif first == "x":
        next_move = computer
    else:
        next_move = player
        print("錯誤位置，重新輸入")
        
    show(chessboard)
    
    
    print('=========================')
    print('Game Start!')
    
    while empty(chessboard, position) and terminal(chessboard, win, position) == 0:        
    
        if next_move == player and empty(chessboard, position):
            try:
                hmove = int(input("由左至右，由上至下輸入(1-9):"))
                if chessboard[position[hmove-1][0]][position[hmove-1][1]] != 0:
                    print('該位置已有棋子，重選')
                    continue
                chessboard[position[hmove-1][0]][position[hmove-1][1]] = player  
                next_move = computer     
            except:
                print("輸入1~9")
                continue
        
        if next_move == computer and empty(chessboard, position):
            cmove, po = computer_move(chessboard, win, position)         
            chessboard[cmove[0]][cmove[1]] = computer    
            print("電腦落子:", po)
            next_move = player
          
        show(chessboard)
    
    print('=========================')
    print('最終:')
    show(chessboard)
    s = terminal(chessboard, win, position)
    print('Game End:',result[s+1])
    print('=========================')