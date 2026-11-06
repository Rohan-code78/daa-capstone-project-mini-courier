import unittest

from src.main import CourierService


class CourierServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = CourierService()

    def test_create_order(self):
        order = self.service.create_order(
            sender="Alice",
            recipient="Bob",
            origin="Lagos",
            destination="Abuja",
            weight_kg=4.5,
            fragile=False,
        )

        self.assertEqual(order["status"], "Pending")
        self.assertTrue(order["id"].startswith("CR-"))
        self.assertEqual(len(self.service.list_orders()), 1)

    def test_update_order_status(self):
        order = self.service.create_order(
            sender="Alice",
            recipient="Bob",
            origin="Lagos",
            destination="Abuja",
            weight_kg=2.0,
        )

        updated = self.service.update_status(order["id"], "In Transit")
        self.assertEqual(updated["status"], "In Transit")
        self.assertEqual(self.service.get_order(order["id"])["status"], "In Transit")

    def test_invalid_status_rejected(self):
        order = self.service.create_order(
            sender="Alice",
            recipient="Bob",
            origin="Lagos",
            destination="Abuja",
            weight_kg=5.0,
        )

        with self.assertRaises(ValueError):
            self.service.update_status(order["id"], "Missing")

    def test_total_revenue_matches_orders(self):
        self.service.create_order("A", "B", "X", "Y", 5.0)
        self.service.create_order("C", "D", "Y", "Z", 2.0)

        total = self.service.calculate_total_revenue()
        self.assertGreater(total, 0)
        self.assertEqual(len(self.service.list_orders()), 2)


if __name__ == "__main__":
    unittest.main()
