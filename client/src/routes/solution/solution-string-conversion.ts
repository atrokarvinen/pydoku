export const strategyToString = (strategy: string) => {
	switch (strategy) {
		case 'claiming':
			return 'Claiming';
		case 'empty-rectangle':
			return 'Empty Rectangle';
		case 'hidden-pair':
			return 'Hidden Pair';
		case 'hidden-quad':
			return 'Hidden Quadruple';
		case 'hidden-triple':
			return 'Hidden Triple';
		case 'jellyfish':
			return 'Jellyfish';
		case 'naked-pair':
			return 'Naked Pair';
		case 'naked-quad':
			return 'Naked Quadruple';
		case 'naked-triple':
			return 'Naked Triple';
		case 'pointing':
			return 'Pointing';
		case 'scan':
			return 'Scan';
		case 'single-candidate':
			return 'Single Candidate';
		case 'simple-coloring':
			return 'Simple Coloring';
		case 'swordfish':
			return 'Swordfish';
		case 'x-cycle':
			return 'X-Cycle';
		case 'x-wing':
			return 'X-Wing';
		case 'xy-wing':
			return 'XY-Wing';
		case 'y-wing':
			return 'Y-Wing';
		default:
			return strategy;
	}
};
