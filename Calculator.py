"""
FastAPI calculator app.

Serves a modern calculator UI from the `static/` folder and exposes
a JSON API at `/api/calc`.

Run:
	pip install -r requirements.txt
	uvicorn Calculator:app --reload
"""
from pathlib import Path
import ast
import operator as op
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


_OPERATORS = {
	ast.Add: op.add,
	ast.Sub: op.sub,
	ast.Mult: op.mul,
	ast.Div: op.truediv,
	ast.Pow: op.pow,
	ast.Mod: op.mod,
	ast.FloorDiv: op.floordiv,
}


def _eval_node(node):
	if isinstance(node, ast.Expression):
		return _eval_node(node.body)
	if isinstance(node, ast.BinOp):
		left = _eval_node(node.left)
		right = _eval_node(node.right)
		oper = type(node.op)
		if oper in _OPERATORS:
			return _OPERATORS[oper](left, right)
		raise ValueError("Unsupported operator")
	if isinstance(node, ast.UnaryOp):
		operand = _eval_node(node.operand)
		if isinstance(node.op, ast.UAdd):
			return +operand
		if isinstance(node.op, ast.USub):
			return -operand
		raise ValueError("Unsupported unary operator")
	if isinstance(node, ast.Constant):
		if isinstance(node.value, (int, float)):
			return node.value
		raise ValueError("Invalid constant")
	if isinstance(node, ast.Num):
		return node.n
	raise ValueError("Unsupported expression")


def safe_eval(expr: str) -> Union[int, float]:
	try:
		parsed = ast.parse(expr, mode="eval")
	except (SyntaxError, ValueError):
		raise ValueError("Invalid expression")
	for n in ast.walk(parsed):
		if isinstance(n, (ast.Call, ast.Name, ast.Attribute, ast.Subscript)):
			raise ValueError("Unsupported expression")
	return _eval_node(parsed)


class CalcRequest(BaseModel):
	expression: str


app = FastAPI(title="Calculator", docs_url="/api/docs", redoc_url=None)


@app.post("/api/calc")
async def calc(body: CalcRequest):
	expr = body.expression
	try:
		result = safe_eval(expr)
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	return {"result": result}


static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


if __name__ == "__main__":
	import uvicorn

	uvicorn.run("Calculator:app", host="127.0.0.1", port=8000, reload=True)
