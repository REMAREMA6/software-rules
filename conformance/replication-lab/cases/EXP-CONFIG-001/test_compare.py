import copy, unittest
from compare import compare

class ConfigurationMutationTests(unittest.TestCase):
    def setUp(self):
        self.source={"scenarios":[
          {"label":"defaults","decisions":[{"path":"/Report","status":200},{"path":"/report","status":200},{"path":"/Report/","status":200},{"path":"/report/","status":200}]},
          {"label":"case-sensitive","decisions":[{"path":"/Report","status":200},{"path":"/report","status":404},{"path":"/Report/","status":200},{"path":"/report/","status":404}]},
          {"label":"strict","decisions":[{"path":"/Report","status":200},{"path":"/report","status":200},{"path":"/Report/","status":404},{"path":"/report/","status":404}]},
          {"label":"case-sensitive-and-strict","decisions":[{"path":"/Report","status":200},{"path":"/report","status":404},{"path":"/Report/","status":404},{"path":"/report/","status":404}]},
          {"label":"late-case-sensitive-change","decisions":[{"path":"/Report","status":200},{"path":"/report","status":200}]}]}
        self.replica=copy.deepcopy(self.source)
    def test_equivalent_configuration(self): self.assertEqual(compare(self.source,self.replica)["result"],"match")
    def test_case_sensitivity_mutation(self):
        self.replica["scenarios"][1]["decisions"][1]["status"]=200
        self.assertEqual(compare(self.source,self.replica)["result"],"mismatch")
    def test_strict_routing_mutation(self):
        self.replica["scenarios"][2]["decisions"][2]["status"]=200
        self.assertEqual(compare(self.source,self.replica)["result"],"mismatch")
    def test_late_setting_mutation(self):
        self.replica["scenarios"][4]["decisions"][1]["status"]=404
        self.assertEqual(compare(self.source,self.replica)["result"],"mismatch")
if __name__=="__main__": unittest.main()
