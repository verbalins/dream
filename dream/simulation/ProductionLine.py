from __future__ import absolute_import
from __future__ import print_function

from dream.simulation.Globals import runSimulation

# if runSimulation is imported first, the program runs,
# else it errors on importing Machine
from dream.simulation.imports import (
    CoreObject,
    Source,
    Exit,
    Frame,
    Queue,
    Assembly,
    Dismantle,
    Failure,
    ParallelMachine,
)


class ProductionLine(CoreObject):
    class_name = "Dream.ProductionLine"

    def __init__(
        self,
        id="",
        name="",
        processingTime=None,
        avb=None,
        mdt=None,
        maxWIP=None,
        avgWIP=None,
        minLT=None,
        **kw
    ):
        self.type = "ProductionLine"                         # String that shows the type of object
        super().__init__(id, name)

        self.processingTime = processingTime
        self.avb = avb
        self.mdt = mdt
        self.maxWIP = maxWIP
        self.avgWIP = avgWIP
        self.minLT = minLT

        # Define the objects of the model, create id based on name of Line
        Frame.capacity = 1

        self.WIPSource = Source(
            id=self.name + "_WIPSource",
            name=self.name + "_WIPSource",
            interArrivalTime={"Fixed": {"mean": 1}},
            entity="Dream.Frame",
            number=self.maxWIP - 1,
        )

        self.LineWIP = Queue(
            id=self.name + "_LineWIP",
            name=self.name + "_LineWIP",
            capacity=self.maxWIP,
            gatherWipStat=True
        )

        beta = ((self.maxWIP - self.avgWIP) * self.processingTime) / self.avb

        self.WIPControl = ParallelMachine(
            id=self.name + "_WIPControl",
            name=self.name + "_WIPControl",
            capacity=self.maxWIP + 5,
            beta={'Exp': {'mean': beta}}
        )
        # self.WIPControl = Queue("WIPControl", "WIPControl", capacity=maxWIP)

        self.LineInput = Assembly(
            id=self.name + "_LineInput",
            name=self.name + "_LineInput",
            processingTime={"Fixed": {"mean": self.processingTime}}
        )
        self.LineOutput = Dismantle(
            id=self.name + "_LineOutput",
            name=self.name + "_LineOutput",
            processingTime={"Fixed": {"mean": self.processingTime}}
        )

        F = Failure(
            victim=self.LineInput,
            distribution={
                "TTF": {"Fixed": {"mean": self.avb}},
                "TTR": {"Fixed": {"mean": self.mdt}},
            },
        )

        self.objectList = [self.LineInput, self.WIPSource, self.WIPControl, self.LineWIP, self.LineOutput]
        self.interruptionList = [F]

    def initialize(self):
        CoreObject.initialize(self)
        self.LineInput.initialize()
        self.LineOutput.initialize()
        self.WIPControl.initialize()
        self.WIPSource.initialize()

        # Statistics

    def defineRouting(self, predecessorList=[], successorList=[]):
        # Define the routing, sets entry to LineInput and exits to LineOutput
        self.previous = predecessorList
        self.next = successorList

        # Define predecessors and successors for the objects
        self.WIPSource.defineRouting([self.WIPControl])
        self.LineInput.defineRouting(self.previous + [self.WIPControl], [self.LineWIP])

        self.LineWIP.defineRouting([self.LineInput], [self.LineOutput])

        self.LineOutput.defineRouting(
            predecessorList=[self.LineWIP],
            successorList=self.next + [self.WIPControl],
            definePartFrameRouting=[self.next, [self.WIPControl]],
        )
        self.WIPControl.defineRouting([self.WIPSource, self.LineOutput], [self.LineInput])

    def run(self):
        # Run periodical log outputs
        while True:
            yield self.env.timeout(60)
            print("========== Objects in Queue:", len(self.WIPControl.getActiveObjectQueue()))

    def getActiveObjectQueue(self):
        return []
