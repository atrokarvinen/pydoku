class CustomAsserts():
    def assertListEqualNoOrder(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        self.assertEqual(sorted(list1), sorted(list2))
