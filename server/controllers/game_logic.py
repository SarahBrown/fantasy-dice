from random import randint

class game_logic:

    # define static variables
    result = None

    @staticmethod
    def compute_result(dice_list):
        result = 0
        for x in dice_list:
            result += x
        return result

    @staticmethod
    def generate_dice(num_dice):
        dice_list = []
        # add num_dice values to the list
        for i in range(num_dice):
            # assuming all dice are d6
            dice_list.append(randint(1,6))
        # compute result and store to static var
        game_logic.result = game_logic.compute_result(dice_list)
        return dice_list

    @staticmethod
    def check_result(user_answer):
        if user_answer == game_logic.result:
            return True
        else:
            return False
