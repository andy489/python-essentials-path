from pathlib import Path


class Level:
    def __init__(self, filename: str):
        self._filename = filename

    def read_map(self):
        """Read the map from file"""
        ...

    def read_characters(self):
        """Read the characters from this level"""
        ...

    def get_name(self):
        """Read the name of this level"""
        ...


class Game:
    def __init__(self, dir: Path):
        self.levels = []
        for level_file in dir.glob("*.lvl"):
            self.levels.append(Level(str(level_file)))


class Menu:
    """A menu where the player can choose which level to play"""

    def show(self, game: Game) -> Level:
        """Show the game menu"""
        for i, level in enumerate(game.levels):
            name = level.get_name()
            print(f"{i}: {name}")
        choice = int(input("Choose a level: ")) - 1
        return game.levels[choice]
