from __future__ import absolute_import
from __future__ import print_function

from dream.simulation.Globals import runSimulation

# if runSimulation is imported first, the program runs,
# else it errors on importing Machine
from dream.simulation.imports import (
    Source,
    Exit,
    Frame,
    Queue,
    Machine,
    Assembly,
    Dismantle,
    NonStarvingEntry,
    Failure
)

maxWIP = 30
avgWIP = 20
processingTime = 2
avb = 90

# Define the objects of the model
Sp = NonStarvingEntry("SP", "In")

Frame.capacity = 1

WIPSource = Source(
    "SF",
    "WIPSource",
    interArrivalTime={"Fixed": {"mean": 1}},
    entity="Dream.Frame",
    number=30
)
LineWIP = Queue("LineWIP", "LineWIP", capacity=maxWIP)
# beta = ((maxWIP - avgWIP) * processingTime) / avb
# WIPControl = Machine("WIPControl", "WIPControl", capacity=maxWIP, processingTime={'Exp': {'mean': beta}})
WIPControl = Queue("WIPControl", "WIPControl", capacity=maxWIP)
procDict = {"Triangular": {"min": processingTime - 1, "mean": processingTime, "max": processingTime + 1}}

LineInput = Assembly(
    "A", "LineInput", processingTime=procDict
)
LineOutput = Dismantle("D", "LineOutput", processingTime=procDict)

EP = Exit("E1", "Out")

F = Failure(
    victim=LineInput,
    distribution={"TTF": {"Fixed": {"mean": 60.0}}, "TTR": {"Fixed": {"mean": 5.0}}},
)

# define predecessors and successors for the objects
Sp.defineRouting([LineInput])

WIPSource.defineRouting([WIPControl])
LineInput.defineRouting([Sp, WIPControl], [LineWIP])

LineWIP.defineRouting([LineInput], [LineOutput])

LineOutput.defineRouting(predecessorList=[LineWIP], successorList=[EP, WIPControl], definePartFrameRouting=[[EP], [WIPControl]])
WIPControl.defineRouting([WIPSource, LineOutput], [LineInput])

EP.defineRouting([LineOutput])


def main(test=0):
    # add all the objects in a list
    objectList = [Sp, WIPSource, LineInput, WIPControl, LineWIP, LineOutput, EP]

    # set the length of the experiment
    maxSimTime = 1440.0

    # call the runSimulation giving the objects and the length of the experiment
    runSimulation(objectList, maxSimTime, console="Yes")

    # calculate metrics
    working_ratio = (LineInput.totalWorkingTime / maxSimTime) * 100

    if test:
        return {
            "parts": EP.numOfExits,
            "frames": WIPSource.numberOfArrivals,
            "working_ratio": working_ratio
        }

    # print the results
    print("The system produced", EP.numOfExits, "parts")
    print("The system created", WIPSource.numberOfArrivals, "frames")
    print("Total working time for", LineInput.objName, "is", LineInput.totalWorkingTime)
    print("The working ratio of", LineInput.objName, "is", working_ratio, "%")


if __name__ == "__main__":
    main()
