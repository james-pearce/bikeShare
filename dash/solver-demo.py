from ortools.constraint_solver import pywrapcp

solver = pywrapcp.Solver("jp-test")

#x = solver.NumVar(-solver.Infinity(), solver.Infinity(), 'x')
x = solver.