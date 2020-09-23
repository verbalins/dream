from __future__ import absolute_import
from __future__ import print_function

from dream.simulation.Globals import runSimulation

# if runSimulation is imported first, the program runs,
# else it errors on importing Machine
from dream.simulation.imports import (
    NonStarvingEntry,
    ProductionLine,
    Source,
    Exit
)

def main(test=0):
    # Define the objects of the model
    Sp = NonStarvingEntry("SP", "In")
    Line = ProductionLine("Line1", "Line1", processingTime=60, avb=98, mdt=300, maxWIP=50, avgWIP=45, minLT=5)
    EP = Exit("E1", "Out")

    # define predecessors and successors for the objects
    Sp.defineRouting([Line.LineInput])
    Line.defineRouting([Sp], [EP])
    EP.defineRouting([Line.LineOutput])

    # add all the objects in a list
    objectList = [Sp, Line, EP]

    # set the length of the experiment
    maxSimTime = 3600.0

    # call the runSimulation giving the objects and the length of the experiment
    runSimulation(objectList, maxSimTime, console="Yes")

    if test:
        return {
            "parts": EP.numOfExits,
            "frames": Line.WIPSource.numberOfArrivals,
            "workingRatio": Line.LineInput.Working,
            "failureRation": Line.LineInput.Failure
        }

    # Print the results for debugging
    print("The system produced", EP.numOfExits, "parts")
    print("Number of Frames produced", Line.WIPSource.numberOfArrivals)
    print("Working time of LineInput", Line.LineInput.Working)
    print("Failure time of LineInput", Line.LineInput.Failure)


if __name__ == "__main__":
    main()
