from __future__ import annotations
from poke_team import Trainer, PokeTeam 
from typing import Tuple
from battle_mode import BattleMode
from data_structures import queue_adt
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from enum import Enum
class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        """
        Initalizes the battle class
        Parameters:
        trainer_1 (Trainer): The first trainer participating in the battle.
        trainer_2 (Trainer): The second trainer participating in the battle.
        battle_mode (BattleMode): The battle mode to be used.
        criterion (str, optional): The criterion for sorting teams in OPTIMISE mode.

        Returns PokeTeam , PokeTeam

        Time Complexity:
        O(1)
        """
        
        
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        """
        Starts the battle by calling a battle function

        Parameters: None
        Returns: Trainer or None

        Time Complexirty:
        O(1)
        
        """
        if self.battle_mode == BattleMode.SET:
            return self.set_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            return self.optimise_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            return self.rotate_battle()
 
    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        """
        Creates teams for the battle based on the specified battle mode's recommended data structure.

        Returns:
            Tuple[PokeTeam, PokeTeam]
        Time Complexity:
        O(1)
        """
       
        battle_modes_data_structures = {
        BattleMode.SET: ArrayStack(PokeTeam.TEAM_LIMIT),  #Recommended for Set Mode
        BattleMode.ROTATE: CircularQueue(PokeTeam.TEAM_LIMIT),  #Recommended for Rotating Mode
        BattleMode.OPTIMISE: ArraySortedList(PokeTeam.TEAM_LIMIT)  #Recommended for Optimized Mode
        }

        rec_data_structure = 0
        if self.battle_mode in battle_modes_data_structures:
            rec_data_structure = battle_modes_data_structures[self.battle_mode]
        
            #Check if both trainers are using the recommended data structure
            if not isinstance(self.trainer_1, type(rec_data_structure)) or \
                not isinstance(self.trainer_2, type(rec_data_structure)):
                #If wrong data structure
                raise ValueError("Teams are the wrong data structure")
        
        team1 = PokeTeam()
        team2 = PokeTeam()
        
        return team1, team2


    def set_battle(self) -> PokeTeam | None:
        """
        Implements set battle logic

        Parameters: None

        Time Complexity
        O(n) n is num of pokemon in eahc team
        """


        #Counter for the team index
        x = 0 ; y = 0

        #Check Speed of first pokemon 
        if self.trainer_1.team[0].get_speed() > self.trainer_2.team[0].get_speed():
            first_attacker = self.trainer_1
            second_attacker = self.trainer_2
        else :
            first_attacker = self.trainer_2
            second_attacker = self.trainer_1

        while len(self.trainer_1.team) != 0 and len(self.trainer_2.team)!= 0:
            second_attacker.team[y].defend(first_attacker.team[x].attack(second_attacker.team[y]))
            if second_attacker.team[y].is_alive() != True:
                first_attacker.team[x].level_up()
                if y<5:
                    y +=1
                else:
                    return first_attacker
            first_attacker.team[x].defend(second_attacker.team[y].attack(first_attacker.team[x]))
            if first_attacker.team[x].is_alive() != True:
                second_attacker.team[y].level_up()
                if x<5:
                    x+=1
                else:
                    return second_attacker

    def rotate_battle(self) -> PokeTeam | None:
        """
        Implements logic for rotate battle mode
        
        Time COmplexity:
        (n^2)

        """

        if self.trainer_1.team[0].get_speed() > self.trainer_2.team[0].get_speed():
            first_attacker = self.trainer_1.team
            second_attacker = self.trainer_2.team
        else :
            first_attacker = self.trainer_2.team
            second_attacker = self.trainer_1.team

        self.trainer_1.team.rot_team()
        self.trainer_2.team.rot_team()

        while len(self.trainer_1.team) != 0 and len(self.trainer_2.team)!= 0:
            #Saving the served Pokemon
            Pokemon_1 = first_attacker.serve()
            Pokemon_2 = second_attacker.serve()

            #Attack 1 
            Pokemon_2.defend(Pokemon_1.attack(Pokemon_2))
            if Pokemon_2.is_alive() == True:
                second_attacker.append(Pokemon_2)
            elif Pokemon_2.is_alive() != True:
                Pokemon_2 = second_attacker.serve()
                Pokemon_1.level_up()

            first_attacker.append(Pokemon_1)

            #Attack 2
            Pokemon_1.defend(Pokemon_2.attack(Pokemon_1))
            if Pokemon_1.is_alive() == True:
                first_attacker.append(Pokemon_1)
            elif Pokemon_1.is_alive() != True:
                Pokemon_1 = first_attacker.serve()
                Pokemon_2.level_up()

            second_attacker.append(Pokemon_2)

            #Loop until over
        print("winner is: ")
        if len(self.trainer_1.team) == 0:
            print("2")
            return self.trainer_2
        elif len(self.trainer_2.team) == 0:
            print("1")
            return self.trainer_1
        else:
            print("No Winner")
            return None



    def optimise_battle(self) -> PokeTeam | None:
        #Counter for the team index
        """
        Implements battle logic for optimize 
        
        Time complexity:
        O(n^2)
        """
        x = 0 ; y = 0

        #Check Speed of first pokemon 
        if self.trainer_1.team[0].get_speed() > self.trainer_2.team[0].get_speed():
            first_attacker = self.trainer_1
            second_attacker = self.trainer_2
        else :
            first_attacker = self.trainer_2
            second_attacker = self.trainer_1

        while len(self.trainer_1.team) != 0 and len(self.trainer_2.team)!= 0:
            second_attacker.team[y].defend(first_attacker.team[x].attack(second_attacker.team[y]))
            if second_attacker.team[y].is_alive() != True:
                first_attacker.team[x].level_up()
                if y>6:
                    y +=1
                else:return first_attacker
            first_attacker.team[x].defend(second_attacker.team[y].attack(first_attacker.team[x]))
            if first_attacker.team[x].is_alive() != True:
                second_attacker.team[y].level_up()
                if x>6:
                    x +=1
                else:return second_attacker
            

if __name__ == '__main__':
    
    t1 = Trainer('Ash')
    t1.pick_team("random")

    t2 = Trainer('Gary')
    t2.pick_team('random')
    b = Battle(t1, t2, BattleMode.SET)

    winner = b.commence_battle()
    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
