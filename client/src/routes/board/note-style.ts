import type { Elimination } from '$lib/types/elimination';
import { NoteType } from '$lib/types/note-type';
import type { SingleCandidate } from '$lib/types/single-candidate';
import type { Square } from '$lib/types/sudoku';

export const getNoteType = (
	square: Square,
	note: number,
	selectedElimination: Elimination | undefined,
	selectedCandidate: SingleCandidate | undefined
) => {
	if (selectedElimination) {
		const eliminationNoteType = getEliminatedNoteType(selectedElimination, square, note);
		if (eliminationNoteType) {
			return eliminationNoteType;
		}
	}
	if (selectedCandidate) {
		if (
			selectedCandidate.row === square.row &&
			selectedCandidate.column === square.column &&
			selectedCandidate.number === note
		) {
			return NoteType.CANDIDATE;
		}
	}
	return NoteType.NORMAL;
};

const getEliminatedNoteType = (elimination: Elimination, square: Square, note: number) => {
	const eliminatedNote = elimination.eliminatedNotes.find(
		(eliminatedNote) =>
			eliminatedNote.row === square.row &&
			eliminatedNote.column === square.column &&
			eliminatedNote.number === note
	);
	if (eliminatedNote) {
		return NoteType.ELIMINATED;
	}

	const causingNote = elimination.causingNotes.find(
		(causingNote) =>
			causingNote.row === square.row &&
			causingNote.column === square.column &&
			causingNote.number === note
	);
	if (causingNote) {
		if (causingNote.color === 'simple-coloring-1') {
			return NoteType.COLORING_1;
		} else if (causingNote.color === 'simple-coloring-2') {
			return NoteType.COLORING_2;
		} else {
			return NoteType.CAUSING;
		}
	}

	return undefined;
};
