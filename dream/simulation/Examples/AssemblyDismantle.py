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
    Dismantle
)

# Define the objects of the model
Sp = Source(
    "SP",
    "Parts",
    interArrivalTime={"Fixed": {"mean": 0.25}},
    entity="Dream.Part",
    number=30
)

Frame.capacity = 2

Sf = Source(
    "WIPSource",
    "Frames",
    interArrivalTime={"Fixed": {"mean": 0.1}},
    entity="Dream.Frame",
    number=30
)
Q = Queue("Q1", "Q", capacity=30)

A = Assembly(
    "A", "Assembly", processingTime={"Triangular": {"min": 1, "mean": 2, "max": 3}}
)
D = Dismantle("D", "Dismantle", processingTime={"Fixed": {"mean": 2}})

EP = Exit("E1", "ExitProducts")
EF = Exit("E2", "ExitFrames")

# define predecessors and successors for the objects
Sp.defineRouting([A])
Sf.defineRouting([A])
A.defineRouting([Sp, Sf], [Q])
Q.defineRouting([A], [D])
D.defineRouting([Q])
D.definePartFrameRouting(successorPartList=[EP], successorFrameList=[EF])
EP.defineRouting([D])
EF.defineRouting([D])


def main(test=0):
    # add all the objects in a list
    objectList = [Sp, Sf, A, Q, D, EP, EF]

    # set the length of the experiment
    maxSimTime = 1440.0  # 7*24*60

    # call the runSimulation giving the objects and the length of the experiment
    runSimulation(objectList, maxSimTime)

    # calculate metrics
    working_ratio = (A.totalWorkingTime / maxSimTime) * 100

    if test:
        return {
            "parts": EP.numOfExits,
            "frames": EF.numOfExits,
            "working_ratio": working_ratio
        }

    # print the results
    print("the system produced", EP.numOfExits, "parts")
    print("Total working time for", A.objName, "is", A.totalWorkingTime)
    print("the working ratio of", A.objName, "is", working_ratio, "%")


if __name__ == "__main__":
    main()
