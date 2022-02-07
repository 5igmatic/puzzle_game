from tile import Tile

class World:
    def __init__(self, size):
        self.traversableTiles = [" "]
        self.levels = [["tttttt",
                        "t    t",
                        "t    t",
                        "tttttt"]]
        self.tiles = [[]]
        self.size = size
        self.playerLocation = [3, 2]
        self.currentLevel = 0

    def load(self, currentLevel, offset):
        self.currentLevel = currentLevel
        levelData = self.levels[currentLevel]
        rowIndex = 0
        for row in levelData:
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

    #update for jump compatability
    def updateLocation(self, right):
        if right:
            print("right")
            self.playerLocation[0] += 1
        else:
            print("left")
            self.playerLocation[0] -= 1
        print(self.playerLocation)

    #update for jump compatability
    def isBlocked(self, right):
        moveLocation = list(self.playerLocation)
        if right:
            moveLocation[0] += 1
        else:
            moveLocation[0] -= 1
        print(self.playerLocation)
        if self.levels[self.currentLevel][moveLocation[1]][moveLocation[0]] in self.traversableTiles:
            return False
        return True

