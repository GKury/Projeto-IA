import random
import numpy as np

# Tamanho do tabuleiro
ROWS = 4
COLS = 5
MINES = 5

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


# Parâmetros do Q-learning
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON = 1.0  # Para exploração
EPSILON_DECAY = 0.995
MIN_EPSILON = 0.01

# Função para inicializar a Q-table
def initialize_q_table():
    # O estado pode ser o tabuleiro "flattened" (transformado em vetor 1D)
    # e as ações podem ser de duas formas: "revelar" ou "marcar bandeira"
    # O tabuleiro tem ROWS * COLS posições e para cada uma há 2 ações (revelar ou marcar bandeira)
    q_table = np.zeros([ROWS * COLS, 2])
    return q_table

# Função para escolher uma ação usando a política epsilon-greedy
def choose_action(q_table, state):
    if random.uniform(0, 1) < EPSILON:
        # Exploração: escolhe uma ação aleatória
        action = random.choice([0, 1])  # 0: Revelar, 1: Colocar bandeira
    else:
        # Exploração: escolhe a ação com maior valor Q
        action = np.argmax(q_table[state])
    return action

# Função para calcular a recompensa com base na ação
def calculate_reward(board, row, col, action):
    if action == 0:  # Revelar célula
        if board[row][col] == MINE:
            return -100  # Perdeu o jogo
        else:
            return 10  # Célula segura
    elif action == 1:  # Colocar bandeira
        if board[row][col] == MINE:
            return 5  # Colocou a bandeira corretamente
        else:
            return -5  # Colocou bandeira onde não tem mina

# Função para atualizar a Q-table
def update_q_table(q_table, state, action, reward, new_state):
    best_future_q = np.max(q_table[new_state])
    current_q = q_table[state, action]
    q_table[state, action] = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * best_future_q)

# Treinamento da IA
def train_ai(num_episodes=1000):
    q_table = initialize_q_table()

    for episode in range(num_episodes):
        board = create_board()
        visible_board = create_board()
        place_mines(board, random.randint(0, ROWS - 1), random.randint(0, COLS - 1))  # Coloca minas

        state = 0  # Estado inicial (posição no tabuleiro)
        done = False

        while not done:
            action = choose_action(q_table, state)
            row, col = divmod(state, COLS)

            # Realiza a ação e calcula a recompensa
            reward = calculate_reward(board, row, col, action)

            if action == 0:  # Revelar
                if not reveal(board, visible_board, row, col):
                    done = True  # Perdeu o jogo
                    reward = -100
            elif action == 1:  # Colocar bandeira
                visible_board[row][col] = FLAG if visible_board[row][col] == HIDDEN else HIDDEN

            # Define o próximo estado
            new_state = random.randint(0, ROWS * COLS - 1)

            # Atualiza a Q-table
            update_q_table(q_table, state, action, reward, new_state)

            # Verifica se venceu o jogo
            if check_victory(board, visible_board):
                done = True
                reward = 100  # Recompensa por vencer

            # Atualiza o estado
            state = new_state

        # Decaimento do epsilon (menos exploração conforme a IA aprende)
        global EPSILON
        EPSILON = max(MIN_EPSILON, EPSILON * EPSILON_DECAY)

    return q_table

# Iniciar treinamento
trained_q_table = train_ai()

def get_state(visible_board):
    """
    Converte o tabuleiro visível em um formato adequado para buscar na Q-table.
    Pode ser simplesmente uma tupla com todos os valores do tabuleiro visível.
    """
    # Exemplo: convertendo o tabuleiro 2D em uma tupla imutável
    return tuple([cell for row in visible_board for cell in row])

def choose_action(q_table, state, epsilon=0.1):
    """
    Escolhe a melhor ação com base no estado atual. Usa epsilon-greedy para explorar aleatoriamente.
    """
    if random.uniform(0, 1) < epsilon:  # Exploração: escolha uma ação aleatória às vezes
        return random.choice(['r', 'f'])  # 'r' para revelar, 'f' para bandeira
    else:
        return max(q_table[state], key=q_table[state].get)  # Exploitação: escolha a ação com o maior valor Q

def play_game_with_ai(q_table):
    """
    Joga uma partida de Campo Minado automaticamente usando a Q-table treinada.
    """
    # Cria o tabuleiro visível e inicializa variáveis do jogo
    visible_board = create_board()
    board = None
    mines_placed = False

    while True:
        print_board(visible_board)

        # Obtém o estado atual baseado no tabuleiro visível
        state = get_state(visible_board)

        # Escolhe a ação usando a Q-table treinada
        action = choose_action(q_table, state)

        # Exemplo de seleção aleatória de célula (pode ser melhorado para seguir a lógica do Q-learning)
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        # No primeiro movimento, colocamos as minas
        if not mines_placed:
            board = create_board()
            board = place_mines(board, row, col)  # Evita mina na primeira jogada
            mines_placed = True

        if action == 'r':  # Revelar célula
            if not reveal(board, visible_board, row, col):
                print("A IA pisou em uma mina! Game Over!")
                print_board(board, reveal=True)
                break
        elif action == 'f':  # Marcar/desmarcar bandeira
            if visible_board[row][col] == HIDDEN:
                visible_board[row][col] = FLAG
            elif visible_board[row][col] == FLAG:
                visible_board[row][col] = HIDDEN
        
        if check_victory(board, visible_board):
            print("A IA venceu!")
            print_board(board, reveal=True)
            break

# Exemplo de como rodar o jogo com a AI treinada
play_game_with_ai(trained_q_table)


