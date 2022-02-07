from tile import Tile

class World:
    def __init__(self, size):
        self.levels = [["tttttt",
                        "t    t",
                        "t    t",
                        "tttttt"]]
        self.tiles = [[]]
        self.size = size

    def load(self, currentLevel, offset):
        levelData = self.levels[currentLevel]
        rowIndex = 0
        for row in levelData:
            print(rowIndex)
            tileIndex = 0
            for tile in row:
                if tile != " ":
                    self.tiles[rowIndex].append(Tile(tile, offset, (tileIndex, rowIndex), self.size))
                tileIndex += 1
            self.tiles.append([])
            rowIndex += 1

    def update(self, WIN):
        for row in self.tiles:
            for tile in row:
                tile.update(WIN)


