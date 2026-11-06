# Mini Courier Service

A simple Python courier management app for creating orders, updating delivery status, and tracking revenue.

## Features

- Create new courier orders
- Track package status: Pending, Picked Up, In Transit, Delivered
- View all orders in the system
- Calculate total revenue from active bookings
- Run from an interactive command-line menu

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the app

```bash
python src/main.py
```

## Menu options

1. Create order
2. View all orders
3. Update status
4. Show summary
5. Exit

## Run tests

```bash
python -m unittest discover -s tests
```

## Project structure

- `src/` - application logic and CLI entry point
- `tests/` - unit tests for core behavior
- `requirements.txt` - project dependencies
- `README.md` - setup and usage guide
