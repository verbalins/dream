# import pytest


class TestSimulations:
    def test_SingleServer(self):
        from dream.simulation.Examples.SingleServer import main

        result = main(test=1)
        assert result["parts"] == 2880
        assert 49.99 < result["working_ratio"] < 50.01

    def test_TwoServers(self):
        from dream.simulation.Examples.TwoServers import main

        result = main(test=1)
        assert result["parts"] == 732
        assert 78.17 < result["blockage_ratio"] < 78.18
        assert 26.73 < result["working_ratio"] < 27.74

    def test_AssemblyLine(self):
        from dream.simulation.Examples.AssemblyLine import main

        result = main(test=1)
        assert result["frames"] == 664
        assert 92.36 < result["working_ratio"] < 93.37

    def test_AssemblyDismantle(self):
        from dream.simulation.Examples.AssemblyDismantle import main

        result = main(test=1)
        assert result["parts"] > 0

    def test_DefineNumberSource(self):
        from dream.simulation.Examples.SourceNumberDefined import main

        result = main(test=1)
        assert result["parts"] == 30

    def test_ClearBatchLines(self):
        from dream.simulation.Examples.ClearBatchLines import main

        result = main(test=1)
        assert result["batches"] == 89
        assert 0.069 < result["waiting_ratio_M1"] < 0.07
        assert 0.104 < result["waiting_ratio_M2"] < 0.105
        assert 93.81 < result["waiting_ratio_M3"] < 93.82

    def test_DecompositionOfBatches(self):
        from dream.simulation.Examples.DecompositionOfBatches import main

        result = main(test=1)
        assert result["subbatches"] == 2302
        assert 79.96 < result["working_ratio"] < 79.97
        assert result["blockage_ratio"] == 0
        assert 20.03 < result["waiting_ratio"] < 20.04

    def test_SerialBatchProcessing(self):
        from dream.simulation.Examples.SerialBatchProcessing import main

        result = main(test=1)
        assert result["batches"] == 359
        assert 0.104 < result["waiting_ratio_M1"] < 0.105
        assert 0.104 < result["waiting_ratio_M2"] < 0.105
        assert 75.06 < result["waiting_ratio_M3"] < 75.07

    def test_ParallelServers1(self):
        from dream.simulation.Examples.ParallelServers1 import main

        result = main(test=1)
        assert result["parts"] == 2880
        assert 23.09 < result["working_ratio_M1"] < 23.1
        assert 26.9 < result["working_ratio_M2"] < 26.91

    def test_ParallelServers2(self):
        from dream.simulation.Examples.ParallelServers3 import main

        result = main(test=1)
        assert result["parts"] == 2880
        assert 46.18 < result["working_ratio_M1"] < 46.19
        assert 3.81 < result["working_ratio_M2"] < 3.82

    # NOTE: testParallelServers4 is extension of testParallelServers4
    # so this test really tests if they both run
    def test_ParallelServers4(self):
        from dream.simulation.Examples.ParallelServers4 import main

        result = main(test=1)
        assert result["parts"] == 2880
        assert 46.18 < result["working_ratio_M1"] < 46.19
        assert 3.81 < result["working_ratio_M2"] < 3.82
        assert result["NumM1"] == 2660
        assert result["NumM2"] == 220

    def test_ServerWithShift1(self):
        from dream.simulation.Examples.ServerWithShift1 import main

        result = main(test=1)
        assert result["parts"] == 3
        assert 49.99 < result["working_ratio"] < 50.01

    def test_ServerWithShift2(self):
        from dream.simulation.Examples.ServerWithShift2 import main

        result = main(test=1)
        assert result["parts"] == 16
        assert 49.99 < result["working_ratio"] < 50.01

    def test_ServerWithShift3(self):
        from dream.simulation.Examples.ServerWithShift3 import main

        result = main(test=1)
        assert result["parts"] == 4
        assert 59.99 < result["working_ratio"] < 60.01

    def test_ServerWithShift4(self):
        from dream.simulation.Examples.ServerWithShift4 import main

        result = main(test=1)
        assert result["parts"] == 2
        assert 29.99 < result["working_ratio"] < 30.01

    def test_SettingWip1(self):
        from dream.simulation.Examples.SettingWip1 import main

        result = main(test=1)
        assert result["parts"] == 1
        assert result["simulationTime"] == 0.25
        assert result["working_ratio"] == 100

    def test_SettingWip2(self):
        from dream.simulation.Examples.SettingWip2 import main

        result = main(test=1)
        assert result["parts"] == 2
        assert result["simulationTime"] == 0.50
        assert result["working_ratio"] == 100

    def test_SettingWip3(self):
        from dream.simulation.Examples.SettingWip3 import main

        result = main(test=1)
        assert result["parts"] == 2
        assert result["simulationTime"] == 0.35
        assert result["working_ratio"] == 100

    def test_BalancingABuffer(self):
        from dream.simulation.Examples.BalancingABuffer import main

        result = main(test=1)
        assert result["parts"] == 13
        assert result["working_ratio"] == 80

    def test_ChangingPredecessors(self):
        from dream.simulation.Examples.ChangingPredecessors import main

        result = main(test=1)
        assert result["parts"] == 10
        assert result["simulationTime"] == 36.0
        assert 83.32 < result["working_ratio"] < 83.34

    def test_NonStarvingLine(self):
        from dream.simulation.Examples.NonStarvingLine import main

        result = main(test=1)
        assert result["parts"] == 9
        assert result["working_ratio"] == 100

    def test_NonStarvingLineBatches(self):
        from dream.simulation.Examples.NonStarvingLineBatches import main

        result = main(test=1)
        assert result["batches"] == 4
        assert result["working_ratio"] == 100

    def test_CompoundMachine(self):
        from dream.simulation.Examples.CompoundMachine import main

        result = main(test=1)
        assert 5.8 < result < 5.92

    def test_BufferAllocation(self):
        from dream.simulation.Examples.BufferAllocation import main

        result = main(test=1)
        assert 80 < result["parts"] < 1000


class TestJobShop:
    def test_JobShop1(self):
        from dream.simulation.Examples.JobShop1 import main

        result = main(test=1)
        expectedResult = [
            ["Queue1", 0],
            ["Machine1", 0],
            ["Queue3", 1.0],
            ["Machine3", 1.0],
            ["Queue2", 4.0],
            ["Machine2", 4.0],
            ["Exit", 6.0],
        ]
        assert result == expectedResult

    def test_JobShop2EDD(self):
        from dream.simulation.Examples.JobShop2EDD import main

        result = main(test=1)
        expectedResult = [
            ["Queue1", 0],
            ["Machine1", 2.0],
            ["Queue3", 3.0],
            ["Machine3", 3.0],
            ["Queue2", 6.0],
            ["Machine2", 6.0],
            ["Exit", 8.0],
            ["Queue1", 0],
            ["Machine1", 0],
            ["Queue2", 2.0],
            ["Machine2", 2.0],
            ["Queue3", 6.0],
            ["Machine3", 6.0],
            ["Exit", 12.0],
            ["Queue1", 0],
            ["Machine1", 3.0],
            ["Queue3", 13.0],
            ["Machine3", 13.0],
            ["Exit", 16.0],
        ]
        assert result == expectedResult

    def test_JobShop2MC(self):
        from dream.simulation.Examples.JobShop2MC import main

        result = main(test=1)
        expectedResult = [
            ["Queue1", 0],
            ["Machine1", 12.0],
            ["Queue3", 13.0],
            ["Machine3", 13.0],
            ["Queue2", 16.0],
            ["Machine2", 16.0],
            ["Exit", 18.0],
            ["Queue1", 0],
            ["Machine1", 10.0],
            ["Queue2", 12.0],
            ["Machine2", 12.0],
            ["Queue3", 16.0],
            ["Machine3", 16.0],
            ["Exit", 22.0],
            ["Queue1", 0],
            ["Machine1", 0],
            ["Queue3", 10.0],
            ["Machine3", 10.0],
            ["Exit", 13.0],
        ]
        assert result == expectedResult

    def test_JobShop2Priority(self):
        from dream.simulation.Examples.JobShop2Priority import main

        result = main(test=1)
        expectedResult = [
            ["Queue1", 0],
            ["Machine1", 10.0],
            ["Queue3", 11.0],
            ["Machine3", 13.0],
            ["Queue2", 16.0],
            ["Machine2", 17.0],
            ["Exit", 19.0],
            ["Queue1", 0],
            ["Machine1", 11.0],
            ["Queue2", 13.0],
            ["Machine2", 13.0],
            ["Queue3", 17.0],
            ["Machine3", 17.0],
            ["Exit", 23.0],
            ["Queue1", 0],
            ["Machine1", 0],
            ["Queue3", 10.0],
            ["Machine3", 10.0],
            ["Exit", 13.0],
        ]
        assert result == expectedResult

    def test_JobShop2RPC(self):
        from dream.simulation.Examples.JobShop2RPC import main

        result = main(test=1)
        expectedResult = [
            ["Queue1", 0],
            ["Machine1", 12.0],
            ["Queue3", 13.0],
            ["Machine3", 13.0],
            ["Queue2", 16.0],
            ["Machine2", 16.0],
            ["Exit", 18.0],
            ["Queue1", 0],
            ["Machine1", 10.0],
            ["Queue2", 12.0],
            ["Machine2", 12.0],
            ["Queue3", 16.0],
            ["Machine3", 16.0],
            ["Exit", 22.0],
            ["Queue1", 0],
            ["Machine1", 0],
            ["Queue3", 10.0],
            ["Machine3", 10.0],
            ["Exit", 13.0],
        ]
        assert result == expectedResult

    def test_JobShop2ScenarioAnalysis(self):
        from dream.simulation.Examples.JobShop2ScenarioAnalysis import main

        result = main(test=1)
        assert result == 2
