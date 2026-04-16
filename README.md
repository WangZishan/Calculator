# Calculator

A modern web-based calculator built with **FastAPI** (Python) on the backend and a clean **HTML/CSS/JavaScript** frontend.

## Features

- **Basic arithmetic** — addition, subtraction, multiplication, and division
- **Advanced operators** — exponentiation (`^`), modulo (`%`), floor division
- **Parentheses** — group expressions with `(` and `)`
- **Safe evaluation** — expressions are parsed via Python's `ast` module; no `eval()` is used, preventing code injection
- **Keyboard support** — type expressions and press Enter to evaluate
- **Responsive UI** — dark-themed, mobile-friendly calculator interface

## Tech Stack

| Layer    | Technology          |
| -------- | ------------------- |
| Backend  | FastAPI, Uvicorn    |
| Frontend | HTML, CSS, JavaScript |

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
pip install -r requirements.txt
```

### Running the App

```bash
uvicorn Calculator:app --reload
```

Or run directly:

```bash
python Calculator.py
```

The app will be available at **http://127.0.0.1:8000**.

## API

### `POST /api/calc`

Evaluate a math expression.

**Request body:**

```json
{
  "expression": "2 + 3 * 4"
}
```

**Response:**

```json
{
  "result": 14
}
```

Interactive API docs are available at `/api/docs`.

## Project Structure

```
├── Calculator.py      # FastAPI app & safe expression evaluator
├── requirements.txt   # Python dependencies
└── static/
    ├── index.html     # Calculator UI
    ├── style.css      # Dark-theme styles
    └── app.js         # Frontend logic & API calls
```

## License

This project is provided as-is for educational and personal use.
