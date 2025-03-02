from views.interface_view import InterfaceView
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.markdown import Markdown
import os


class ReportView(InterfaceView):
    """A view class for displaying reports and handling user interface for tournament management.

    This class extends InterfaceView and provides methods for displaying various tournament-related
    information either in HTML format (using Jinja2 templates) or as plain text in the console.

    Attributes:
        env (Environment): Jinja2 environment for template rendering
        console (Console): Rich library console instance for formatted output
        display_mode (str): Current display mode ('html' or 'console')

    Methods:
        choose_display_mode(): Prompts user to select display format
        render_html(template_name, **kwargs): Renders HTML template and converts to markdown
        show_players_list(players): Displays list of players
        show_all_tournaments(tournaments): Shows all tournaments
        show_tournament_details(tournament): Displays details of a specific tournament
        show_tournament_players(players, tournament_name): Shows players in a tournament
        show_tournament_rounds(rounds, tournament_name): Displays tournament rounds and matches
        get_tournament_name(): Gets tournament name from user input

        view = ReportView()
        view.show_players_list([{'last_name': 'Doe', 'first_name': 'John'}])
    """
    def __init__(self):
        super().__init__()
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.console = Console()
        self.display_mode = self.choose_display_mode()

    def choose_display_mode(self) -> str:
        """Prompts user to select display format for reports.
        This method allows user to choose between HTML and console output format
        through command line interface.
        Returns:
            str: 'html' if user selects HTML format (1),
                'console' if user selects console format (2)
        """

        while True:
            print("\nChoose display mode:")
            print("1. Console HTML format")
            print("2. Console text format")
            choice = input("Enter your choice (1 or 2): ").strip()
            if choice in ['1', '2']:
                return 'html' if choice == '1' else 'console'
            print("Invalid choice. Please enter 1 or 2.")

    def render_html(self, template_name: str, **kwargs):
        """Render HTML template and convert it to markdown format for console display.
        This method takes a template file and optional keyword arguments, renders it using
        Jinja2 templating engine, and converts the HTML output to markdown format for
        pretty console printing using Rich library.
        Args:
            template_name (str): Name of the template file to render
            **kwargs: Variable keyword arguments to pass to the template renderer
        Returns:
            None: Prints the formatted markdown to console
        Example:
            render_html('tournament.html', tournament_name='Chess Cup 2023',
                        players=['John', 'Jane'])
        """

        template = self.env.get_template(template_name)

        template.environment.trim_blocks = True
        template.environment.lstrip_blocks = True

        html_content = template.render(**kwargs)
        markdown = html_content.replace('<h2>', '## ') \
            .replace('</h2>', '\n') \
            .replace('<h3>', '### ') \
            .replace('</h3>', '\n') \
            .replace('<h4>', '#### ') \
            .replace('</h4>', '\n') \
            .replace('<ul>', '') \
            .replace('</ul>', '') \
            .replace('<li>', '* ') \
            .replace('</li>', '') \
            .replace('<p>', '') \
            .replace('</p>', '\n') \
            .replace('<div class="round">', '') \
            .replace('</div>', '') \
            .replace('<div class="tournament-rounds">', '') \
            .replace('\n\n\n', '\n') \
            .replace('\n\n', '\n') \
            .replace('* * ', '* ')
        self.console.print(Markdown(markdown.strip()))

    def show_players_list(self, players: list):
        """
        Display a list of players either in HTML format or as plain text based on the display mode.

        Args:
            players (list): A list of dictionaries containing player information.
                           Each dictionary should have 'last_name' and 'first_name' keys.

        Notes:
            - If display_mode is 'html', renders the players_list.html template
            - If display_mode is not 'html', prints a plain text list of players sorted alphabetically
            - Players are displayed in "Last Name, First Name" format in plain text mode
        """

        if self.display_mode == 'html':
            self.render_html('players_list.html', players=players)
        else:
            print("\n=== Players List (Alphabetical) ===")
            for player in players:
                print(f"• {player['last_name']}, {player['first_name']}")

    def show_all_tournaments(self, tournaments: list):
        """Display a list of all tournaments.

        This method shows all tournaments either in HTML format using a template,
        or in console text format depending on the display_mode setting.

        Args:
            tournaments (list): A list of tournament dictionaries containing tournament details
                               like name, location, startDate and endDate.

        Returns:
            None

        Example:
            For console display mode, outputs:
            === Tournament List (ranked by startDate)===
            • Tournament1, Paris (2023-01-01, 2023-01-02)
            • Tournament2, London (2023-02-01, 2023-02-02)
        """

        if self.display_mode == 'html':
            self.render_html('tournaments_list.html', tournaments=tournaments)
        else:
            print("\n=== Tournament List (ranked by startDate)===")
            for tournament in tournaments:
                print(f"• {tournament['name']}, {tournament['location']} "
                      f"({tournament['startDate']}, {tournament['endDate']})")

    def show_tournament_details(self, tournament):
        """
        Display tournament details in either HTML or console format.

        Args:
            tournament (dict): A dictionary containing tournament information with the following keys:
                - name (str): Name of the tournament
                - location (str): Location where tournament is held
                - startDate (str): Start date of tournament
                - endDate (str): End date of tournament
                - description (str): Tournament description

        Returns:
            None: Prints tournament details to console or renders HTML template

        Notes:
            - If display_mode is 'html', renders tournament_details.html template
            - If display_mode is not 'html', prints formatted tournament details to console
            - If tournament is None, prints "No tournament found" message
        """

        if self.display_mode == 'html':
            self.render_html('tournament_details.html', tournament=tournament)
        else:
            if tournament:
                print(f"\n=== Tournament Details: {tournament['name']} ===")
                print(f"Location: {tournament['location']}")
                print(f"Start Date: {tournament['startDate']}")
                print(f"End Date: {tournament['endDate']}")
                print(f"Description: {tournament['description']}")
            else:
                print("\nNo tournament found with that name.")

    def show_tournament_players(self, players: list, tournament_name: str):
        """Display a list of players in a tournament.

        This method shows the list of players participating in a specific tournament.
        The display format depends on the display_mode setting (HTML or console).

        Args:
            players (list): List of dictionaries containing player information
                           with 'last_name' and 'first_name' keys
            tournament_name (str): Name of the tournament to display players for

        Returns:
            None
                Prints output either in HTML format using a template
                or as plain text to console
        """

        if self.display_mode == 'html':
            self.render_html('tournament_players.html', players=players, tournament_name=tournament_name)
        else:
            if tournament_name:
                print(f"\n=== Players in {tournament_name} ===")
                for player in players:
                    print(f"• {player['last_name']}, {player['first_name']}")
            else:
                print("\nNo tournament found with that name.")

    def show_tournament_rounds(self, rounds: list, tournament_name: str):
        """
        Display tournament rounds and matches information either in HTML or console format.

        Args:
            rounds (list): List of dictionaries containing round information including:
                - roundNumber: Round number
                - startDate: Round start date
                - endDate: Round end date
                - matchList: List of matches with player information and scores
            tournament_name (str): Name of the tournament to display

        Returns:
            None

        Notes:
            If display_mode is 'html', renders data using tournament_rounds.html template.
            Otherwise prints formatted text output to console showing:
            - Tournament name
            - For each round:
                - Round number
                - Start/end dates
                - List of matches with player names and scores
            Displays "No tournament found" message if tournament_name is empty.
        """

        if self.display_mode == 'html':
            self.render_html('tournament_rounds.html', rounds=rounds, tournament_name=tournament_name)
        else:
            if tournament_name:
                print(f"\n=== Rounds and Matches in {tournament_name} ===")
                for round_data in rounds:
                    print(f"\nRound: {round_data['number']}")
                    print(f"Started: {round_data['startDate']}")
                    print(f"Ended: {round_data['endDate']}")
                    print("Matches:")
                    for match in round_data['matchList']:
                        player1 = match['match'][0][0]
                        score1 = match['match'][0][1]
                        player2 = match['match'][1][0]
                        score2 = match['match'][1][1]
                        print(f"  • {player1['first_name']} {player1['last_name']} ({score1}) vs "
                              f"{player2['first_name']} {player2['last_name']} ({score2})")
            else:
                print("\nNo tournament found with that name.")

    def get_tournament_name(self) -> str:
        """
        Gets the tournament name from user input.

        Returns:
            str: The tournament name entered by the user, with leading and trailing whitespace removed.
        """

        return input("Enter tournament name: ").strip()
