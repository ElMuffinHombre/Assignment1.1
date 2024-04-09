from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from battle_mode import BattleMode
from battle import Battle
from typing import Tuple
import random as rand

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        """
        Initalizes BattleTower Class

        Time Complexity
        O(1)
        """
        self.enemies_defeated = 0
        self.player_lives = rand.randint(self.MIN_LIVES,self.MAX_LIVES)
        self.enemy_list = ArraySortedList(PokeTeam.TEAM_LIMIT)
        self.enemy_counter = 0
        self.enemy_left = True

    def set_my_trainer(self,player_trainer: Trainer) -> None:
        """
        Sets Trainer

        Time Complexity
        O(1)
        """
        self.player_trainer = player_trainer

    def generate_enemy_trainers(self,n:int) -> None:
        """
        Creates enemy trainers

        Time Complexity 
        O(n)
        """
        self.enemy_trainers = CircularQueue(PokeTeam.TEAM_LIMIT)
        self.number_of_trainers = n
        for i in range(n):
            possible_names = ["Trainer John", "Student Mark", "Poke Girl Alissa", "Ranger Kate", "Ace Trainer Michael"
                              , "Youngster Joey", "Beauty Sarah", "Gym Leader Brock", "Elite Four Lance", "Champion Cynthia"]
            Name = possible_names[rand.randint(0,len(possible_names))]
            enemy_trainer = Trainer(Name)
            enemy_trainer.pick_team("Random")
            enemy_trainer_lives = rand.randint(self.MIN_LIVES,self.MAX_LIVES)
            enemy_info = ListItem(enemy_trainer,enemy_trainer_lives)
            self.enemy_list.add(enemy_info)
        

    def battles_remaining(self) -> bool:
         """
         Checks if there are remaining battles
         Time Complexity 
         O(1)
         """
         return self.player_lives > 0 and any(enemy[1] > 0 for enemy in self.enemy_trainers)

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Does battle until winner is declared

        Time complexity:
        O(f(n)) , I guess f(n) would be how long the rotate battle takes possibly O(n^2)


        """
        bat = Battle(self.player_trainer,self.enemy_trainers,battle_mode=BattleMode.ROTATE)
        winner = bat.commence_battle()
        #If Player wins
        if winner == self.player_trainer:
            self.enemy_trainers[self.enemy_counter].key -=1
            if self.enemy_trainers[self.enemy_counter].key == 0:
                self.enemy_counter+=1
                if self.enemy_counter == self.number_of_trainers:
                    self.enemy_left = False

        elif winner != self.player_trainer:
            self.player_lives -=1
                
        return winner, self.player_trainer , self.enemy_trainers , self.player_lives , self.enemy_trainers[self.enemy_counter].key

    def enemies_defeated(self) -> int:
        return self.enemy_left
