import copy, json, unittest
from pathlib import Path
from compare import compare

class MutationTests(unittest.TestCase):
    def setUp(self):
        base={"runs":[{"uniqueSeries":200,"scrapes":100,"totalSamples":20000,"wallSeconds":1.0,"samplesPerSecond":20000.0} for _ in range(3)]}
        self.source=copy.deepcopy(base); self.replica=copy.deepcopy(base)
    def test_equivalent_workload_passes(self):
        self.assertEqual(compare(self.source,self.replica),[])
    def test_dropped_scrape_is_detected(self):
        for run in self.replica["runs"]:
            run["scrapes"]=99; run["totalSamples"]=19800
        self.assertTrue(compare(self.source,self.replica))
    def test_missing_repeat_is_detected(self):
        self.replica["runs"].pop()
        self.assertTrue(compare(self.source,self.replica))

if __name__=="__main__": unittest.main()
