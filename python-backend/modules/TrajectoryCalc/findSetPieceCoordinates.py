from models.events import *
from models.challenges import *
from constants.columnAndFieldNames import *

def findSetPieceCoordinates(setPiece: Event(), eventData: Events()):
    index = setPiece.id
    newX = eventData[index + 1].start.x
    newY = eventData[index + 1].start.y
    newStart = Coordinates(newX, newY)
    return newStart