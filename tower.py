from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple
import random as rand

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        self.enemies_defeated = 0
        self.player_lives = rand.randint(self.MIN_LIVES,self.MAX_LIVES)
        

    def set_my_trainer(self,player_trainer: Trainer) -> None:
        self.player_trainer = player_trainer

    def generate_enemy_trainers(self,n:int) -> None:
        self.enemy_trainers = []
        for i in range(n):
            enemy_trainer = Trainer("Enemy no.{i}")
            enemy_trainer_lives = rand.randint(self.MIN_LIVES,self.MAX_LIVES)
            self.enemy_trainers.append((enemy_trainer, enemy_trainer_lives))



    def battles_remaining(self) -> bool:
         return self.player_lives > 0 and any(enemy[1] > 0 for enemy in self.enemy_trainers)

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        raise NotImplementedError

    def enemies_defeated(self) -> int:
        return self.enemies_defeated