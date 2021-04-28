import torch
import random
import numpy as np
from collections import deque
from Constants import Properties
from game_grid import GamePlay
from model import Linear_QNet, QTrainer
from tracker import plot

MAX_MEMORY = 500_000
BATCH_SIZE = 1000
LR = 0.0005


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(900, 1700, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

        self.game = GamePlay()

        # Inputs
        self.grid = []
        self.enemypos_list = []
        self.player_pos = []
        self.player_lives = 0
        self.score = 0

        # Outputs
        # self.actions = [Properties.LEFTARROW, Properties.RIGHTARROW, Properties.DOWNARROW, Properties.UPARROW]
        # actions options [0,0,0,1] - R
        # actions options [0,0,1,0] - L
        # actions options [0,1,0,0] - D
        # actions options [1,0,0,0] - U

    def load_model(self, name='model.pth'):
        self.model.load(name)

    def get_state(self):
        self.grid = self.game.map.grid
        grid = self.game.map.numerical1d(self.grid)

        player_pos = [self.game.pacman.x, self.game.pacman.y]
        player_grid = list(self.game.map.find_grid(player_pos[0],player_pos[1]))
        player_lives = self.game.pacman.lives
        player_speed = self.game.pacman.speed
        player_dir = self.game.pacman.direction
        direction = 0

        if player_dir == 'Left':
            direction = 1
        elif player_dir == 'Up':
            direction = 2
        elif player_dir == 'Down':
            direction = 3

        score = self.game.score
        enemies = len(self.game.enemies)

        # Keep track of enemy pos and if they are chasing you
        enemypos_list = []
        for enemy in self.game.enemies:
            chase = 0
            if enemy.mode == 'Chase':
                chase = 1

            enemypos_list += [enemy.id, enemy.x, enemy.y, chase]

        state = grid + player_pos + [player_lives, player_speed, direction] + player_grid
        state += [score] + [enemies]

        # Pad 0's at the end for consistent size
        l = len(state) + len(enemypos_list)
        zs = 900 - l
        zeros = [0] * zs
        state += zeros

        # Keep enmy pos at end for consistent values when adding more meta data
        state += enemypos_list

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        while True:
            # get old state
            state_old = self.get_state()

            # get move
            final_move = self.get_action(state_old)

            # perform move and get new state
            self.game.game_step(final_move, True)
            state_new = self.get_state()

            done = self.game.pacman.lives <= 0
            reward = self.game.reward

            # train short memory
            self.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            self.remember(state_old, final_move, reward, state_new, done)

            if done:
                # train long memory, plot result
                score = self.game.score
                self.game.restart()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save()

                print('Game:', self.n_games, 'Record:', record)
                print('Score:', score, 'Reward:', reward)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    neo = Agent()
    neo.load_model()
    neo.train()
