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

    def test_AssemblyDismantle(self):
        from dream.simulation.Examples.AssemblyDismantle import main
        result = main(test=1)
        assert result["parts"] > 0

    def test_DefineNumberSource(self):
        from dream.simulation.Examples.SourceNumberDefined import main
        result = main(test=1)
        assert result["parts"] == 30

    def test_AssemblyLine(self):
        from dream.simulation.Examples.AssemblyLine import main
        result = main(test=1)
        assert result['frames'] == 664
        assert 92.36 < result["working_ratio"] < 93.37

    def test_ClearBatchLines(self):
        from dream.simulation.Examples.ClearBatchLines import main

        result = main(test=1)
        assert result["batches"] == 89
        assert 0.069 < result["waiting_ratio_M1"] < 0.07
        assert 0.104 < result["waiting_ratio_M2"] < 0.105
        assert 93.81 < result["waiting_ratio_M3"] < 93.82
