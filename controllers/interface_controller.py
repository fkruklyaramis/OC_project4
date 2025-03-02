
from views.interface_view import InterfaceView
from controllers.tournament_controller import TournamentController
from views.tournament_view import TournamentView


class InterfaceController():
    """Interface controller class.
    This class manages the user interface and menu navigation.
    """
    def __init__(self, view: InterfaceView):
        self.view = view

    def show_menu(self):
        """Display the tournament menu.
        This method displays a menu interface for tournament management options.
        Returns:
            str: The user's menu selection.
        """

        menu = self.menu_tournament()
        return menu

    def menu_tournament(self):
        """Display the tournament menu.
        This method displays a menu interface for tournament management options.
        Returns:
            str: The user's menu selection.
        """
        TournamentController(TournamentView()).manage_tournament()
