from solver.solver import Solver
from techniques.biValueUniversalGrave import BiValueUniversalGrave
from techniques.claiming import Claiming
from techniques.emptyRectangle import EmptyRectangle
from techniques.hiddenPair import HiddenPair
from techniques.nakedPair import NakedPair
from techniques.pointing import Pointing
from techniques.scan import Scan
from techniques.simpleColoring import SimpleColoring
from techniques.singleCandidate import SingleCandidate
from techniques.solverBase import SolverBase
from techniques.xCycle import XCycle
from techniques.xWing import XWing
from techniques.yWing import YWing


class SolverFactory:
    def create_solver(self, solver: Solver) -> SolverBase:
        if solver.name == "Scan":
            return Scan()
        elif solver.name == "Single Candidate":
            return SingleCandidate()
        elif solver.name == "Naked Pair":
            return NakedPair()
        elif solver.name == "Pointing":
            return Pointing()
        elif solver.name == "Claiming":
            return Claiming()
        elif solver.name == "Hidden Pair":
            return HiddenPair()
        elif solver.name == "X-Wing":
            return XWing()
        elif solver.name == "Simple Coloring":
            return SimpleColoring()
        elif solver.name == "Y-Wing":
            return YWing()
        elif solver.name == "Empty Rectangle":
            return EmptyRectangle()
        elif solver.name == "Bi-Value Universal Grave":
            return BiValueUniversalGrave()
        elif solver.name == "X-Cycle":
            return XCycle()
