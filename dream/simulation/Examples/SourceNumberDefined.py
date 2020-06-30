from __future__ import absolute_import
from __future__ import print_function

from dream.simulation.Globals import runSimulation

from dream.simulation.imports import (Machine, Source, Exit)

# Source constrained by 30 products
Sp = Source(
    "SP",
    "Parts",
    interArrivalTime={"Fixed": {"mean": 0.25}},
    entity="Dream.Part",
    number=30,
)

M = Machine(
    "M", "Machine",
    processingTime={"Triangular": {"min": 0.5, "mean": 1, "max": 1.5}}
)

EP = Exit("E1", "Exit")

Sp.defineRouting([M])
M.defineRouting([Sp], [EP])
EP.defineRouting([M])


def main(test=0):
    objectList = [Sp, M, EP]
    maxSimTime = 1440.0

    runSimulation(objectList, maxSimTime, console="Yes", trace="Yes")

    if test:
        return {"parts": EP.numOfExits}

    print("The system produced", EP.numOfExits, "parts.")
    from dream.simulation.Globals import G
    from pathlib import Path
    G.traceFile.save(str(Path.home()) + "/trace.xls")


if __name__ == "__main__":
    main()
