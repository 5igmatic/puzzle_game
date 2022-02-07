from tile import Tile

class World:
    def __init__(self):
        self.levels = [["tttttt",
                        "t    t",
                        "t    t",
                        "tttttt"]]
        self.tiles = [[]]

    def load(self, currentLevel, offset, size):
        leveldata = self.levels[currentLevel]
        rowindex = 0
        for row in leveldata:
            print(rowindex)
            tileindex = 0
            for tile in row:
                print(tileindex)
                self.tiles[rowindex].append(Tile(offset, (rowindex, tileindex), size))
                tileindex += 1
            self.tiles.append([])
            rowindex += 1


