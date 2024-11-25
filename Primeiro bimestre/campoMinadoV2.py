import random

# Tamanho do tabuleiro
ROWS = 8
COLS = 10
MINES = 10

# Representações
HIDDEN = '-'
MINE = '*'
FLAG = 'F'

# Função para criar o tabuleiro
def create_board():
    # Cria o tabuleiro vazio
    board = [[HIDDEN for _ in range(COLS)] for _ in range(ROWS)]
    return board

# Função para plantar minas no tabuleiro, excluindo a primeira célula clicada
def place_mines(board, exclude_row, exclude_col):
    #Faz com que o programa não quebre a seguir
    match exclude_row:
        case 0:
            exclude_row = 1
        case 7:
            exclude_row = 6

    match exclude_col:
        case 0:
            exclude_col = 1
        case 9:
            exclude_col = 8

    mine_positions = set()
    while len(mine_positions) < MINES:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        # Garante o primeiro clique seja em um espaço vazio (0)
        if row != exclude_row - 1 and row != exclude_row and row != exclude_row + 1 and col != exclude_col -1 and col != exclude_col and col != exclude_col + 1:
            mine_positions.add((row, col))
            board[row][col] = MINE
    return board

# Função para contar minas adjacentes a uma célula
def count_adjacent_mines(board, row, col):
    adjacent_mines = 0
    for i in range(max(0, row - 1), min(ROWS, row + 2)):
        for j in range(max(0, col - 1), min(COLS, col + 2)):
            if board[i][j] == MINE:
                adjacent_mines += 1
    return adjacent_mines

# Função para mostrar o tabuleiro
def print_board(board, reveal=False):
    for row in board:
        print(' '.join(row))
    print()

# Função para revelar a célula clicada
def reveal(board, visible_board, row, col):
    if board[row][col] == MINE:
        return False  # O jogador clicou em uma mina, perdeu o jogo
    
    # Se for uma célula já revelada, não faz nada
    if visible_board[row][col] != HIDDEN:
        return True

    # Conta o número de minas ao redor
    mines_around = count_adjacent_mines(board, row, col)
    visible_board[row][col] = str(mines_around)

    # Se não houver minas ao redor, revela as células adjacentes
    if mines_around == 0:
        for i in range(max(0, row - 1), min(ROWS, row + 2)):
            for j in range(max(0, col - 1), min(COLS, col + 2)):
                if visible_board[i][j] == HIDDEN:
                    reveal(board, visible_board, i, j)
    return True

# Função para verificar vitória (todas as células sem mina reveladas)
def check_victory(board, visible_board):
    for row in range(ROWS):
        for col in range(COLS):
            if visible_board[row][col] == HIDDEN and board[row][col] != MINE:
                return False
    return True

# Função principal do jogo
def play_game():
    # Cria o tabuleiro visível para o jogador
    visible_board = create_board()
    
    # Variável para armazenar se as minas já foram colocadas
    mines_placed = False
    board = None  # Inicializado depois do primeiro clique
    
    # Loop do jogo
    while True:
        print_board(visible_board)
        command = input("\nDigite sua ação (ex: 'r 2 3' para revelar ou 'f 2 3' para marcar bandeira): ")
        
        parts = command.split()

        while len(parts) != 3:
            command = input("\nAção inválida. Digite 3 caracteres separados por 1 espaço (ex: 'r 2 3' para revelar ou 'f 2 3' para marcar bandeira): ")
            parts = command.split()
        
        action = parts[0]
        row = int(parts[1])
        col = int(parts[2])

        while action != 'r' and action != 'f':
            action = input("\nAção inválida. Digite 'r' para revelar ou 'f' para marcar bandeira: ")

        while row < 0 or row > 7:
            row = int(input("\nLinha inválida. Digite um número entre 0 e 7 para escolher uma linha: "))

        while col < 0 or col > 9:
            col = int(input("\nColuna inválida. Digite um número entre 0 e 9 para escolher uma coluna: "))

        # No primeiro movimento, colocamos as minas
        if not mines_placed:
            board = create_board()
            board = place_mines(board, row, col)  # Evita mina na primeira jogada
            mines_placed = True
        
        if action == 'r':  # Revelar célula
            if not reveal(board, visible_board, row, col):
                print("Você pisou em uma mina! Game Over!")
                print_board(board, reveal=True)
                break
        elif action == 'f':  # Marcar/desmarcar bandeira
            if visible_board[row][col] == HIDDEN:
                visible_board[row][col] = FLAG
            elif visible_board[row][col] == FLAG:
                visible_board[row][col] = HIDDEN
        
        if check_victory(board, visible_board):
            print("Parabéns! Você venceu!")
            print_board(board, reveal=True)
            break

# Inicia o jogo
play_game()
