"""
Crater Object: Holds its x,y coordinate, and its radiusR (radius x-direction) and radiusC (radius y-direction)
Also handles the fill function which turns off the entries in the matrix corisponding to the crater
"""
class Crater:
    def __init__(self, x, y, radiusR, radiusC):
        self.radiusR = radiusR
        self.radiusC = radiusC
        self.x = x
        self.y = y
        self.covered = 0
    def fill(self, surface):
        surface[(self.x - self.radiusR):(self.x + self.radiusR), (self.y - self.radiusC):(self.y + self.radiusC)] = 0
