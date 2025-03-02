import os


class InterfaceView():
    def __init__(self):
        self.choice_list = []

    def menu(self):
        """Displays a menu of choices and returns the user's selection.
        This method prints a welcome message followed by a list of menu options.
        Each option is displayed with its corresponding numeric value and label.
        The screen is cleared after the user makes a selection.
        Returns:
            int: The numeric value corresponding to the user's menu selection
        """

        for value in self.choice_list:
            print(f"{value['value']} : {value['label']}")
        choice_input = input("Choose an option : ")
        choice = 0
        try:
            choice = int(choice_input)
            os.system('cls' if os.name == 'nt' else 'clear')
        except ValueError:
            print(f"Invalid choice : {choice_input}, please try again.")
        return choice

    def set_choice_list(self, choice_list):
        """Set the list of choices for the menu.
        This method sets the list of choices that will be displayed in the menu.
        Each choice should be a dictionary with 'value' and 'label' keys.
        Args:
            choice_list (list): A list of dictionaries containing menu choices
        Returns:
            None
        """

        self.choice_list = choice_list
