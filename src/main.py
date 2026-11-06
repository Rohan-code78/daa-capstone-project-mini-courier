from __future__ import annotations

from datetime import datetime

VALID_STATUSES = ["Pending", "Picked Up", "In Transit", "Delivered"]


class CourierService:
    def __init__(self):
        self._orders = {}

    def create_order(
        self,
        sender: str,
        recipient: str,
        origin: str,
        destination: str,
        weight_kg: float,
        fragile: bool = False,
        priority: str = "standard",
    ) -> dict:
        order_id = self._next_order_id()
        fee = self._calculate_fee(weight_kg, fragile, priority)
        order = {
            "id": order_id,
            "sender": sender.strip(),
            "recipient": recipient.strip(),
            "origin": origin.strip(),
            "destination": destination.strip(),
            "weight_kg": float(weight_kg),
            "fragile": bool(fragile),
            "priority": priority.strip().lower() or "standard",
            "status": "Pending",
            "fee": round(fee, 2),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self._orders[order_id] = order
        return dict(order)

    def get_order(self, order_id: str) -> dict:
        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order {order_id} not found.")
        return dict(order)

    def update_status(self, order_id: str, status: str) -> dict:
        order = self._orders.get(order_id)
        if order is None:
            raise KeyError(f"Order {order_id} not found.")

        normalized_status = self._normalize_status(status)
        order["status"] = normalized_status
        return dict(order)

    def list_orders(self) -> list[dict]:
        return [dict(order) for order in self._orders.values()]

    def calculate_total_revenue(self) -> float:
        return round(sum(order["fee"] for order in self._orders.values()), 2)

    def summary(self) -> dict:
        counts = {status: 0 for status in VALID_STATUSES}
        for order in self._orders.values():
            counts[order["status"]] = counts.get(order["status"], 0) + 1
        return {
            "total_orders": len(self._orders),
            "total_revenue": self.calculate_total_revenue(),
            "status_counts": counts,
        }

    def _next_order_id(self) -> str:
        next_number = len(self._orders) + 1
        return f"CR-{next_number:04d}"

    @staticmethod
    def _calculate_fee(weight_kg: float, fragile: bool, priority: str) -> float:
        fee = 12.0 + (weight_kg * 4.5)
        if fragile:
            fee += 8.0
        if priority.lower() == "express":
            fee += 15.0
        return fee

    @staticmethod
    def _normalize_status(status: str) -> str:
        normalized = status.strip().lower()
        mapping = {
            "pending": "Pending",
            "picked up": "Picked Up",
            "in transit": "In Transit",
            "delivered": "Delivered",
        }
        if normalized not in mapping:
            valid = ", ".join(VALID_STATUSES)
            raise ValueError(f"Invalid status. Choose one of: {valid}")
        return mapping[normalized]


def _display_order(order: dict) -> None:
    print("-" * 60)
    print(f"Order ID: {order['id']}")
    print(f"Sender: {order['sender']} -> Recipient: {order['recipient']}")
    print(f"Route: {order['origin']} to {order['destination']}")
    print(f"Weight: {order['weight_kg']} kg | Status: {order['status']}")
    print(f"Fee: ${order['fee']:.2f} | Priority: {order['priority']}")
    print("-" * 60)


def run_cli() -> None:
    service = CourierService()

    service.create_order("Maya", "John", "Lagos", "Abuja", 3.0)
    service.create_order("Tolu", "Grace", "Kaduna", "Kano", 6.5, fragile=True, priority="express")

    while True:
        print("\nMini Courier Service")
        print("1. Create order")
        print("2. View all orders")
        print("3. Update status")
        print("4. Show summary")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            try:
                sender = input("Sender name: ").strip()
                recipient = input("Recipient name: ").strip()
                origin = input("Pickup city: ").strip()
                destination = input("Destination city: ").strip()
                weight = float(input("Package weight in kg: ").strip())
                fragile = input("Fragile package? (y/n): ").strip().lower() in {"y", "yes"}
                priority = input("Priority (standard/express): ").strip().lower() or "standard"
                order = service.create_order(
                    sender=sender,
                    recipient=recipient,
                    origin=origin,
                    destination=destination,
                    weight_kg=weight,
                    fragile=fragile,
                    priority=priority,
                )
                print("Order created successfully!")
                _display_order(order)
            except ValueError:
                print("Please enter valid numeric values.")
        elif choice == "2":
            orders = service.list_orders()
            if not orders:
                print("No orders available.")
                continue
            for order in orders:
                _display_order(order)
        elif choice == "3":
            order_id = input("Enter order ID: ").strip()
            status = input("Enter new status (Pending/Picked Up/In Transit/Delivered): ").strip()
            try:
                order = service.update_status(order_id, status)
                print(f"Status updated for {order_id}.")
                _display_order(order)
            except (KeyError, ValueError) as exc:
                print(exc)
        elif choice == "4":
            summary = service.summary()
            print(f"Total orders: {summary['total_orders']}")
            print(f"Total revenue: ${summary['total_revenue']:.2f}")
            for key, value in summary["status_counts"].items():
                print(f"{key}: {value}")
        elif choice == "5":
            print("Thanks for using Mini Courier Service.")
            break
        else:
            print("Invalid option. Please choose again.")


def main() -> None:
    print("Welcome to the Mini Courier Service!")
    run_cli()


if __name__ == "__main__":
    main()
