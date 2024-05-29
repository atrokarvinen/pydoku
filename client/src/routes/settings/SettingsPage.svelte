<script lang="ts">
	import RestoreDefaultsButton from './RestoreDefaultsButton.svelte';
	import SaveButton from './SaveButton.svelte';
	import type { Settings } from './settings';
	import type { Solver } from './solver';

	export let settings: Settings;

	$: solvers = settings.solvers;

	const priorityUp = (current: Solver[], index: number) => {
		if (index === 0) return;
		solvers = current.map((solver, i) => {
			if (i === index - 1) return { ...solvers[index], priority: i };
			else if (i === index) return { ...solvers[index - 1], priority: i };
			return solver;
		});
	};

	const priorityDown = (current: Solver[], index: number) => {
		if (index === solvers.length - 1) return;
		solvers = current.map((solver, i) => {
			if (i === index + 1) return { ...solvers[index], priority: i };
			else if (i === index) return { ...solvers[index + 1], priority: i };
			return solver;
		});
	};

	const enabledChanged = (current: Solver[], index: number) => {
		solvers = current.map((solver, i) => {
			if (i === index) return { ...solvers[index], enabled: !solvers[index].enabled };
			return solver;
		});
	};

	const onDefaultsRestored = (defaults: Solver[]) => {
		solvers = defaults;
	};
</script>

<div class="flex flex-col gap-2 justify-start w-full">
	<p>Adjust solver priorities.</p>
	<p>
		<i class="fas fa-warning" />
		<span>Warning: Moving complex techniques to the top of the list can slow down solve time.</span>
	</p>
	{#each solvers as solver, index (solver.id)}
		<div class="flex flex-row gap-2 items-center">
			<p class="w-6">{index + 1}</p>
			<p class="grow">{solver.name}</p>
			<input
				type="checkbox"
				class="checkbox"
				checked={solver.enabled}
				on:change={() => enabledChanged(solvers, index)}
			/>
			<div class="flex flex-row gap-1">
				<button class="btn-icon-sm variant-filled" on:click={() => priorityUp(solvers, index)}
					><i class="fas fa-arrow-up" /></button
				>
				<button class="btn-icon-sm variant-filled" on:click={() => priorityDown(solvers, index)}
					><i class="fas fa-arrow-down" /></button
				>
			</div>
		</div>
	{/each}
	<div class="flex flex-row justify-end gap-2">
		<RestoreDefaultsButton {onDefaultsRestored} />
		<SaveButton {solvers} />
	</div>
</div>
