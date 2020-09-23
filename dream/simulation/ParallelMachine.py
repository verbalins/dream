from __future__ import absolute_import

from dream.simulation.Queue import Queue
from dream.simulation.RandomNumberGenerator import RandomNumberGenerator

# ===========================================================================
# the Parallel Machine object, processes parts in parallel
# ===========================================================================
class ParallelMachine(Queue):
    # =======================================================================
    # initialise the id the capacity, of the resource and the distribution
    # =======================================================================
    def __init__(self, id="", name="", capacity=1, beta={'Exp': {'mean': 1}}, **kw):
        self.type = "ParallelMachine"  # String that shows the type of object
        super().__init__(id, name, capacity)
        self.beta = beta
        self.avgWaitTime = 0.0
        self.rng = RandomNumberGenerator(self, self.beta)
        self.processDone = []

    def getEntity(self):
        return super().getEntity()

    def run(self):
        # check if there is WIP and signal receiver
        while 1:
            self.initialSignalReceiver()
            while 1:
                self.printTrace(self.id, waitEvent="isRequested")
                # wait until the Queue can accept an entity and one predecessor requests it
                self.expectedSignals["canDispose"] = 1
                self.expectedSignals["isRequested"] = 1
                receivedEvent = yield self.env.any_of([self.isRequested, self.canDispose])
                self.printTrace(self.id, received="")
                # if the event that activated the thread is isRequested then getEntity
                if self.isRequested in receivedEvent:
                    transmitter, eventTime = self.isRequested.value
                    self.printTrace(self.id, isRequested=transmitter.id)
                    # reset the isRequested signal parameter
                    self.isRequested = self.env.event()
                    activeEntity = self.getEntity()
                    self.operation(activeEntity)

                if self.canDispose in receivedEvent:
                    transmitter, eventTime = self.canDispose.value
                    self.printTrace(self.id, canDispose="")
                    self.canDispose = self.env.event()

                if self.haveToDispose():
                    if self.receiver:
                        if not self.receiver.entryIsAssignedTo():
                            # try to signal receiver. In case of failure signal giver (for synchronization issues)
                            if not self.signalReceiver():
                                self.signalGiver()
                        continue
                    self.signalReceiver()
                # signal the giver (for synchronization issues)
                self.signalGiver()

    def haveToDispose(self, callerObject=None):
        # Will need to also check for entities which have waiting enough
        return len(self.getActiveObjectQueue()) > 0 and len(self.processDone) > 0

    def operation(self, activeEntity):
        self.printTrace(activeEntity.id, waitEvent="WAITING")
        procTime = self.calculateProcessingTime()
        self.avgWaitTime += procTime
        schedEv = self.env.timeout(delay=procTime, value=activeEntity)
        schedEv.callbacks = [self.operationFinished]

    def operationFinished(self, delayEvent):
        activeEntity = delayEvent.value
        self.printTrace(activeEntity.id, processEnd="WAITING OVER")
        self.processDone.append(activeEntity)

    def postProcessing(self, MaxSimtime=None):
        super().postProcessing(MaxSimtime)
        self.avgWaitTime = self.avgWaitTime / self.numEntries

    def removeEntity(self, entity=None):
        activeEntity = super().removeEntity(entity)
        self.Res.users.remove(activeEntity)
        return activeEntity

    def getActiveObjectQueue(self):
        return self.processDone

    def setBeta(self, newBeta):
        self.beta = newBeta
        self.rng = RandomNumberGenerator(self, self.beta)
