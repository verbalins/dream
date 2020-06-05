from __future__ import absolute_import
from __future__ import print_function

from dream.simulation.Globals import runSimulation

# if runSimulation is imported first, the program runs,
# else it errors on importing Machine
from dream.simulation.imports import (
    Machine,
    Source,
    Exit,
    Part,
    Frame,
    Queue,
    Assembly,
    Dismantle,
    NonStarvingEntry,
    Failure
)

# Define the objects of the model
Sp = Source(
    "SP",
    "Parts",
    interArrivalTime={"Fixed": {"mean": 0.25}},
    entity="Dream.Part",
    number=30,
)
# Sp = NonStarvingEntry('ProdSource', "In", threshold=1, initialWIPLevel=1, number=30)

Frame.capacity = 2

Sf = Source(
    "WIPSource",
    "Frames",
    interArrivalTime={"Fixed": {"mean": 0.1}},
    entity="Dream.Frame",
    number=30,
)
LineWIP = Queue("Q1", "LineWIP", capacity=30)
WIPControl = Queue("Q2", "WIPControl", capacity=30)

M = Machine(
    "M", "Machine",
    processingTime={"Triangular": {"min": 0.5, "mean": 1, "max": 1.5}}
)
LineInput = Assembly(
    "A", "Assembly",
    processingTime={"Triangular": {"min": 1, "mean": 2, "max": 3}}
)
LineOutput = Dismantle(
    "D", "Dismantle",
    processingTime={"Fixed": {"mean": 2}}
)

EP = Exit("E1", "Exit")

# F=Failure(victim=M, distribution={'TTF':{'Fixed':{'mean':60.0}},'TTR':{'Fixed':{'mean':5.0}}})

# define predecessors and successors for the objects
Sp.defineRouting([LineInput])

Sf.defineRouting([LineInput])
LineInput.defineRouting([Sp, Sf], [LineWIP])
# Sf.defineRouting([WIPControl])
# LineInput.defineRouting([Sp, WIPControl], [LineWIP])

LineWIP.defineRouting([LineInput], [LineOutput])

LineOutput.defineRouting([LineWIP])
LineOutput.definePartFrameRouting(
    successorPartList=[EP], successorFrameList=[WIPControl]
)
WIPControl.defineRouting([LineOutput], [LineInput])
EP.defineRouting([LineOutput])


def main(test=0):
    # add all the objects in a list
    objectList = [Sp, Sf, LineInput, WIPControl, LineWIP, LineOutput, EP]

    # set the length of the experiment
    maxSimTime = 1440.0  # 7*24*60
    
    from dream.simulation.Globals import G
    G.console = "Yes"

    # call the runSimulation giving the objects and the length of the experiment
    runSimulation(objectList, maxSimTime)

    # calculate metrics
    working_ratio = (LineInput.totalWorkingTime / maxSimTime) * 100

    if test:
        return {"parts": EP.numOfExits, "working_ratio": working_ratio}

    # print the results
    print("the system produced", EP.numOfExits, "parts")
    print("Total working time for", LineInput.objName, "is", LineInput.totalWorkingTime)
    print("the working ratio of", LineInput.objName, "is", working_ratio, "%")


if __name__ == "__main__":
    main()
