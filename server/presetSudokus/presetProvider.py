from presetSudokus.difficulty import Difficulty
from presetSudokus.presetSudoku import PresetSudoku


class PresetProvider:
    def get_preset_sudokus(self) -> list[PresetSudoku]:
        easy_sudoku1 = ".785.64.9.69....52...941.6861.2......45.1.....2.....9..567..81..9....6.5281465..3"

        medium_sudoku1 = "6........9..3..864384796....4.9..376..76.45..296..3.8....425713421..7..5........8"

        hard_sudoku1 = ".6...417558......437...6..........89.19..56436.53...........2.819.6....7..75....."

        expert_sudoku1 = "........9..5...17.8....6.3.......8.6....58....9..7...4.7.....659.3.25.....1......"
        expert_sudoku2 = "......92.....67...6.35...........6...78......21..48.9....2....3..73..18..8......."
        expert_sudoku3 = "..7............15.4952...6..1.95...7...8.6..........4......1.....9..35.86...7...."

        x_wing_example = ".93..456..6...314...46.83.9981345...347286951652.7.4834.6..289....4...1..298...34"
        y_wing_example = x_wing_example
        simple_coloring_example = ".3621.84.8...45631.14863..9287.3.456693584...1456723984.8396...35..28.64.6.45..83"
        x_cycle_example1 = "..8..31.2..281.3.631426.98.9236487..4763512981859..634.47.3.82.2.9.8.5..8.17..46."
        x_cycle_example2 = "...8..2.726.3..8......6.....7....3.6.4..8..9.3.1....7.....7......3..8.455.7..9..."

        extreme_sudoku1 = "....9.8...1.....7.2........4..5.7.6.3.9.....4..........5.2.......8...9.....6....."
        extreme_sudoku2 = "7...4..........9.6......1...69..1..8....7..2...........5.8.9...2......4....6....."
        extreme_sudoku3 = ".48.5.......6....9.7.......2..3.9......2..6.........8.....8..4.6.....2......7...."

        presets = [
            PresetSudoku(easy_sudoku1, "Easy sudoku", Difficulty.EASY),
            PresetSudoku(medium_sudoku1, "Medium sudoku", Difficulty.MEDIUM),
            PresetSudoku(hard_sudoku1, "Hard sudoku", Difficulty.HARD),
            PresetSudoku(expert_sudoku1, "Expert sudoku #1",
                         Difficulty.EXPERT),
            PresetSudoku(expert_sudoku2, "Expert sudoku #2",
                         Difficulty.EXPERT),
            PresetSudoku(expert_sudoku3, "Expert sudoku #3",
                         Difficulty.EXPERT),
            PresetSudoku(x_wing_example, "X-wing example", Difficulty.EXTREME),
            PresetSudoku(y_wing_example, "Y-wing example", Difficulty.EXTREME),
            PresetSudoku(simple_coloring_example,
                         "Simple coloring example", Difficulty.EXTREME),
            PresetSudoku(x_cycle_example1, "X-cycle example #1",
                         Difficulty.EXTREME),
            PresetSudoku(x_cycle_example2, "X-cycle example #2",
                         Difficulty.EXTREME),
            PresetSudoku(extreme_sudoku1, "Extreme sudoku #1",
                         Difficulty.EXTREME),
            PresetSudoku(extreme_sudoku2, "Extreme sudoku #2",
                         Difficulty.EXTREME),
            PresetSudoku(extreme_sudoku3, "Extreme sudoku #3",
                         Difficulty.EXTREME)
        ]
        for i, preset in enumerate(presets):
            preset.id = str(i)
        return presets

    def get_preset_sudoku(self, preset_id: str) -> PresetSudoku:
        presets = self.get_preset_sudokus()
        return next(preset for preset in presets if preset.id == preset_id)
