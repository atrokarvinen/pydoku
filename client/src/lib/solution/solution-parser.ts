import type { Elimination } from '$lib/types/elimination';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Solution } from '$lib/types/solution';
import type { SolutionMenu, SolutionStep } from '$lib/types/solution-menu';

export const getSolutionSteps = (solution: Solution) => {
	const steps: (Elimination | SingleCandidate)[] = [
		...solution.eliminations,
		...solution.singleCandidates
	].sort((a, b) => a.solutionIndex - b.solutionIndex);
	return steps;
};

export const getSolutionStepsCount = (solution: Solution) => {
	return solution.eliminations.length + solution.singleCandidates.length;
};

export const getSolutionStepsByCount = (steps: (Elimination | SingleCandidate)[]) => {
	const menu: SolutionMenu = { groups: [] };
	for (const step of steps) {
		const technique = step.technique;
		const index = step.solutionIndex;
		let group = menu.groups.find((group) => group.technique === technique);
		if (!group) {
			group = { technique, steps: [] };
			menu.groups.push(group);
		}
		const solutionStep: SolutionStep = {
			step: index,
			solution: step
		};
		group.steps.push(solutionStep);
	}
	return menu;
};
