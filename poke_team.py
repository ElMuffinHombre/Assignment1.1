from pokemon import *
import random
from typing import List
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue, Queue
from battle_mode import BattleMode

class PokeTeam:
    random.seed(20)
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]
    printer = 'x'

    def __init__(self):
        self.team = [None] * self.TEAM_LIMIT
        self.team_count = 0

    def choose_manually(self):
        """
        Allows User to choose team Manually

        Returns:
        None
        Time Complexity(O+M)
        """
        self.team = [None] * self.TEAM_LIMIT
        while True:
            try:
                pokenum = input("Would you like to change the number of pokemon on your team? (Y/N) \n").upper()
                break   

            except ValueError:
                print("Please put Y or N")
                continue
                                
                
        if  pokenum== 'Y':
            while True:
                    try:
                        teamlen = int(str(input("How many pokemon would you like on your team? ")))
                        self.TEAM_LIMIT = teamlen
                        break
                    except ValueError:
                        print("Please input a valid value")
                        continue

        elif pokenum == 'N':
            pass
                
        
        self.team_count = 0
        all_pokemon = get_all_pokemon_types()
        for x in range(PokeTeam.TEAM_LIMIT):
            for i in range(len(all_pokemon)):
                print(f"{i + 1}.) {all_pokemon[i]().get_name()}")
            while True:
                try:
                    choice = int(str(input("Please enter the pokemon(number) that you want:")))-1
                    break
                except ValueError:
                    print("invalid choice please enter an integer")
                    continue
            print(all_pokemon[choice]())
            print(f"i:{i} x:{x}")
            self.team[x] = all_pokemon[choice]()
            self.team_count += 1
            

    def choose_randomly(self) -> None:
        """
        Chooses Pokemon for the team randomly.

        This function randomly selects Pokemon for the team from the available options.

        Time Complexity:
            - O(M), where M is the size of the team.

        Returns:
            None
        """

        self.team = [None] * self.TEAM_LIMIT
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(PokeTeam.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1

    def regenerate_team(self) -> None:
        raise NotImplementedError

    def assign_team(self, criterion: str = None) -> None:
        """
        Assigns team based on Criterion given.

        Parameters:
        Critertion (str) : What the team should be sorted by

        Returns:
            None
        
        Time Complexity 
            O(nLog(n))
        
        
        """
        SortedTeam = ArraySortedList(self.TEAM_LIMIT)
        if criterion == self.CRITERION_LIST[1]:

            for i in enumerate(self.team):

                criterion_value = self.team[i].get_health()
                Poke_Attr = ListItem(self.team[i], criterion_value)
                SortedTeam.append(Poke_Attr)
        elif criterion == self.CRITERION_LIST[2]:

            for i in enumerate(self.team):

                criterion_value = self.team[i].get_defence()
                Poke_Attr = ListItem(self.team[i], criterion_value)
                SortedTeam.append(Poke_Attr)

        elif criterion == self.CRITERION_LIST[3]:

            for i in enumerate(self.team):

                criterion_value = self.team[i].get_battle_power()
                Poke_Attr = ListItem(self.team[i], criterion_value)
                SortedTeam.append(Poke_Attr)
        elif criterion == self.CRITERION_LIST[4]:
            for i in enumerate(self.team):
                criterion_value = self.team[i].get_speed()
                Poke_Attr = ListItem(self.team[i], criterion_value)
                SortedTeam.append(Poke_Attr)
        elif criterion == self.CRITERION_LIST[5]:
            for i in enumerate(self.team):
                criterion_value = self.team[i].get_level()
                Poke_Attr = ListItem(self.team[i], criterion_value)
                SortedTeam.append(Poke_Attr)

        self.team = SortedTeam
        return self.team

    def assemble_team(self, battle_mode: BattleMode) -> None:
        """
        Assembles team correctly in accordance to the Battle Mode
        for Set it becomes a stack
        for Rotate it becomes a Circular Queue
        for Optimized it becomes a SortedList
        Parameters:
        battle_mode (BattleMode): The chosen battle mode for the battle.

        Time Complexity:
            for SET and OPTIMIZED
            O(nlogn) or O(n^2)

            for ROTATE
            O(n)
     
        """
        while True:
            try:
                print("How would you like to assemble your team : ")
                print("Please choose between MANUAL or RANDOM : \n")
                Assembly = str(input()).upper()
                if Assembly == "MANUAL" or Assembly == "M":
                    self.choose_manually()
                elif Assembly == "RANDOM" or Assembly == "R":
                    self.choose_randomly()
                else: 
                    print("Invalid input. Please try again")
                    continue
                break
            except ValueError:
                print("Invalid input. Please try again")
                
        if battle_mode == BattleMode.SET:
            #StackADT
            return self.set_team()
        
        elif battle_mode == BattleMode.ROTATE:
            print("This was called")
            #Circular Queue
            return self.rot_team()
        
        elif battle_mode == BattleMode.OPTIMISE:
            x = 1
            for criterion in ["health", "defence", "battle_power", "speed", "level"]:
                print(f"{x}.) {criterion}")
            x += 1
            criterion_input = input("Please choose a criterion: ")
            if criterion_input in ["1", "health"]:
                criterion = self.CRITERION_LIST[1]
            elif criterion_input in ["2", "defence"]:
                criterion = self.CRITERION_LIST[2]
            elif criterion_input in ["3", "battle_power"]:
                criterion = self.CRITERION_LIST[3]
            elif criterion_input in ["4", "speed"]:
                criterion = self.CRITERION_LIST[4]
            elif criterion_input in ["5", "level"]:
                criterion = self.CRITERION_LIST[5]
            else:
                print("Invalid criterion chosen. Please choose again.")
            
            return self.assign_team(criterion)


    def special(self, battle_mode: BattleMode) -> None:
        """
        Perform a special action based on the specified battle mode.

        Parameters:
        battle_mode (BattleMode): The battle mode for which the special action is performed.

        Returns:
        None

        - For SET mode:
            Time Complexity: O(n)

        - For ROTATE mode:
            Time Complexity: O(n)

        - For OPTIMIZED mode:
            Time Complexity: O(nlogn)

        """
        if battle_mode == BattleMode.SET:
            #SPECIAL FOR SET BATTLE MODE
            midpoint = len(self.team) // 2
            temp_stack = ArrayStack(6)
            for i in range(midpoint):
                temp_stack.push(self.team.pop())
            while not temp_stack.is_empty():
                self.team.add(temp_stack.peek())
                temp_stack.pop()
            return self.team

        elif battle_mode == BattleMode.ROTATE:
            #SPECIAL FOR ROTATE BATTLE MODE
            midpoint = len(self.team) // 2
            SaveQueue = Queue()
            for _ in range(midpoint):
                SaveQueue.append(self.team.serve())
            #Using another stack to flip the back end of the queue
            FlipStack = ArrayStack(midpoint)
            for _ in range(midpoint):
                FlipStack.push(self.team.serve())
            while len(FlipStack) != 0:
                self.team.append(FlipStack.peek())
                FlipStack.pop
            while len(SaveQueue) != 0:
                self.team.append(SaveQueue.serve())
            return self.team

        elif battle_mode == BattleMode.OPTIMISE:
            reverserList = ArraySortedList(self.TEAM_LIMIT)
            for i in range(len(self.team)):
                self.team[i].key = 6 - i
                reverserList.add(self.team[i])
            return reverserList

    def __getitem__(self, index: int):
        """
        Retrieve an item from the team at the specified index.

        Parameters:
            index (int): The index of the item to retrieve.

        Returns:
            object: The item at the specified index in the team.

        Time Complexity:
        O(1)

        """
        return self.team[index]
    

    def __len__(self):
        """
        Get the number of Pokemon in the team.

        Returns:
        int: The number of Pokemon in the team.

        Time Complexity:
        O(1)
        """

        return len(self.team)

    def __str__(self):
        """
        Returns the String of all the Pokemon in the team List
        
        Time Complexity:
        O(1)
        """
        TeamList = "Team:\n"
        TeamList += '\n '.join(str(pokemon) for pokemon in self.team)
        return TeamList


        #Created for Assemble_Team
    def set_team(self):
        """
        Makes Team into a ArrayStack for Set battle
        
        Time Complexity:
        O(n)

        Returns:
          Team as a stack
        """
        #StackADT
        StackTeam = ArrayStack(PokeTeam.TEAM_LIMIT)
        for i in self.team:
            StackTeam.push(i)
        self.team = StackTeam
        return self.team
    
    def rot_team(self):
        """
        Makes Team into a Circular Queue for Rotate battle
        
        Time Complexity:
        O(n)

        Returns:
          Team as a Ciruclar Queue
        """
        RotateTeam = CircularQueue(PokeTeam.TEAM_LIMIT)
        for i in self.team:
            RotateTeam.append(i)
        self.team = RotateTeam
        return self.team

    def serve(self):
        return self.team.serve()

    def append(self,item):
        return self.team.append(item)


class Trainer:

    def __init__(self,name: str) -> None:
        """
        initializes the trainer class

        time comeplexity:
        O(1)
        """
        self.name = name
        self.team = PokeTeam()
        self.pokedex = set()


    def pick_team(self, method: str) -> None:
        """
        lets player choose between choosuing a team manually and randomly

        time complexity
        O(1)
        """
        match(method.upper()):
            case "RANDOM":
                self.team.choose_randomly()
            case "MANUAL":
                self.team.choose_manually()

    def get_team(self) -> PokeTeam:
        """
        returns Team
        Time Complexity
        O(1)
        """
        return self.team


    def get_name(self) -> str:
        """
        returns Name
        Time Complexity
        O(1)
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        registers a poketype
        Time Complexity
        O(1)
        """
        self.pokedex.add(pokemon.poketype)


    def get_pokedex_completion(self) -> float:
        """
        gets the pokedex completion as a float
        Time Complexity
        O(1)
        """
        pokedex_completion = self.pokedex.__len__()
        return round(pokedex_completion/15,2)
    
    def __str__(self) -> str:
        """
        returns a string with the trainer name and pokedex completion
        Time Complexity
        O(1)
        """
        trainer_info = f"Trainer {self.name} "
        trainer_info += f"Pokedex Completion: {int(self.get_pokedex_completion()*100)}%"
        return trainer_info
    
if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())