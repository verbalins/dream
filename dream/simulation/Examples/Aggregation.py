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
    Assembly,
    Dismantle,
    NonStarvingEntry,
    Failure
)

# Define the objects of the model
# Sp = NonStarvingEntry("S1", "In", threshold=1, initialWIPLevel=1)
Sp = Source(
    "SP",
    "In",
    interArrivalTime={"Fixed": {"mean": 0.25}},
    entity="Dream.Part"
)

Frame.capacity = 1

WIPSource = Source(
    "SF",
    "WIPSource",
    interArrivalTime={"Fixed": {"mean": 0.1}},
    entity="Dream.Frame",
    # number=30
)
LineWIP = Queue("Q1", "LineWIP", capacity=30)
WIPControl = Queue("Q2", "WIPControl", capacity=25)

LineInput = Assembly(
    "A", "LineInput", processingTime={"Triangular": {"min": 1, "mean": 2, "max": 3}}
)
LineOutput = Dismantle("D", "LineOutput", processingTime={"Fixed": {"mean": 2}})

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

LineOutput.defineRouting(predecessorList=[LineWIP], successorList=[EP, WIPControl])
LineOutput.definePartFrameRouting(
    successorPartList=[EP], successorFrameList=[WIPControl]
)
WIPControl.defineRouting([LineOutput, WIPSource], [LineInput])

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
    print("Total working time for", LineInput.objName, "is", LineInput.totalWorkingTime)
    print("The working ratio of", LineInput.objName, "is", working_ratio, "%")


if __name__ == "__main__":
    main()
