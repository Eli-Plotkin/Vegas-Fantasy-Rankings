from src.betting_rankings import bettingFantasyRankings


def test_getData():
    tester = bettingFantasyRankings()
    tester.outputAllData("input.txt")
