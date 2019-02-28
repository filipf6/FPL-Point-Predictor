package com.pk.fpl_point_predictor.logic.util;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.stereotype.Component;

@Component
public class PlayerSampleBuilder {
    private final int numberOfPreviousMatchesConsidered = 3;

    private ObjectNode buildGeneralStatistics(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectMapper mapper = new ObjectMapper();
        ObjectNode playerSample = mapper.createObjectNode();
        playerSample.set("player_id", playerGeneralInfo.get("id"));//setPlayerId(playerGeneralInfo.get("id").intValue());
        playerSample.set("fixture_id", playerSpecificInfo.get("fixtures_summary").get(0).get("id"));
        playerSample.set("score", null);
        playerSample.set("cost", playerGeneralInfo.get("now_cost"));
        playerSample.set("points_per_game", playerGeneralInfo.get("points_per_game"));
        playerSample.set("form", playerGeneralInfo.get("form"));
        playerSample.set("selected_by_percent", playerGeneralInfo.get("selected_by_percent"));
        playerSample.set("influence", playerGeneralInfo.get("influence"));
        playerSample.set("creativity", playerGeneralInfo.get("creativity"));
        playerSample.set("threat", playerGeneralInfo.get("threat"));
        playerSample.set("ict_index", playerGeneralInfo.get("ict_index"));
        playerSample.set("team_strength", playersTeam.get("strength"));
        playerSample.put("last_season_points_per_minute", countHistoricalSeasonPointsPerMinute(1, playerSpecificInfo));
        playerSample.put("two_seasons_ago_points_per_minute", countHistoricalSeasonPointsPerMinute(2, playerSpecificInfo));
        playerSample.set("fixture_difficulty", playerSpecificInfo.get("fixtures_summary").get(0).get("difficulty"));
        playerSample.set("is_home", playerSpecificInfo.get("fixtures_summary").get(0).get("is_home"));
        playerSample.put("is_slightly_injured", playerGeneralInfo.get("status").textValue().equals("d"));
        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"),
                "total_points",
                "transfers_balance",
                "minutes",
                "bonus",
                "influence",
                "creativity",
                "threat",
                "ict_index",
                "open_play_crosses");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "points");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "transfers_balance");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "minutes");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "bonus");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "influence");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "creativity");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "threat");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "ict_index");
//        buildPreviousMatchesStatistics(playerSample, playerSpecificInfo.get("history_summary"), "open_play_crosses");
        return playerSample;
    }

    public ObjectNode buildGoalkeeperSample(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectNode goalkeeperSample = buildGeneralStatistics(playerGeneralInfo, playerSpecificInfo, playersTeam);
        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"),
                "clean_sheets",
                "goals_conceded",
                "penalties_saved",
                "saves");
//        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"), "clean_sheets");
//        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"), "goals_conceded");
//        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"), "penalties_saved");
//        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"), "saves");
//        goalkeeperSample.setPreviousFixturesCleanSheets(buildPreviousMatchesStatistics(playerSpecificInfo.get("history_summary"), "clean_sheets"));
//        goalkeeperSample.setPreviousFixturesGoalsConceded(buildPreviousMatchesStatistics(playerSpecificInfo.get("history_summary"), "goals_conceded"));
//        goalkeeperSample.setPreviousFixturesPenaltiesSaved(buildPreviousMatchesStatistics(playerSpecificInfo.get("history_summary"), "penalties_saved"));
//        goalkeeperSample.setPreviousFixturesSaves(buildPreviousMatchesStatistics(playerSpecificInfo.get("history_summary"), "saves"));

        return goalkeeperSample;
    }

    public ObjectNode buildDefenderStatisticsSample(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectNode defenderStatisticsSample = buildGeneralStatistics(playerGeneralInfo, playerSpecificInfo, playersTeam);
        buildPreviousMatchesStatistics(defenderStatisticsSample, playerSpecificInfo.get("history_summary"),
                "goals_scored",
                "assists",
                "clean_sheets",
                "goals_conceded",
                "big_chances_created",
                "clearances_blocks_interceptions",
                "recoveries",
                "key_passes",
                "tackles",
                "winning_goals",
                "errors_leading_to_goal",
                "errors_leading_to_goal_attempt",
                "tackled",
                "fouls",
                "dribbles");
//        buildGeneralStatistics(defenderStatisticsSample, playerGeneralInfo, playerSpecificInfo, playersTeam);
//        defenderStatisticsSample.setPreviousFixturesGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "goals_scored"));
//        defenderStatisticsSample.setPreviousFixturesAssists(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "assists"));
//        defenderStatisticsSample.setPreviousFixturesCleanSheets(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "clean_sheets"));
//        defenderStatisticsSample.setPreviousFixturesGoalsConceded(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "goals_conceded"));
//        defenderStatisticsSample.setPreviousFixturesChancesCreated(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "big_chances_created"));
//        defenderStatisticsSample.setPreviousFixturesBlocks(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "clearances_blocks_interceptions"));
//        defenderStatisticsSample.setPreviousFixturesRecoveries(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "recoveries"));
//        defenderStatisticsSample.setPreviousFixturesKeyPasses(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "key_passes"));
//        defenderStatisticsSample.setPreviousFixturesTackles(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "tackles"));
//        defenderStatisticsSample.setPreviousFixturesWinningGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "winning_goals"));
//        defenderStatisticsSample.setPreviousFixturesFatalErrors(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "errors_leading_to_goal"));
//        defenderStatisticsSample.setPreviousFixturesErrors(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "errors_leading_to_goal_attempt"));
//        defenderStatisticsSample.setPreviousFixturesTackled(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "tackled"));
//        defenderStatisticsSample.setPreviousFixturesFouls(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "fouls"));
//        defenderStatisticsSample.setPreviousFixturesDribbles(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "dribbles"));
        return defenderStatisticsSample;
    }

    public ObjectNode buildMidfielderStatisticsSample(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectNode midfielderStatisticsSample = buildGeneralStatistics(playerGeneralInfo, playerSpecificInfo, playersTeam);
        buildPreviousMatchesStatistics(midfielderStatisticsSample, playerSpecificInfo.get("history_summary"),
                "goals_scored",
                "assists",
                "clean_sheets",
                "goals_conceded",
                "big_chances_created",
                "clearances_blocks_interceptions",
                "recoveries",
                "key_passes",
                "tackles",
                "winning_goals",
                "big_chances_missed",
                "errors_leading_to_goal",
                "errors_leading_to_goal_attempt",
                "tackled",
                "fouls",
                "dribbles");

//        buildGeneralStatistics(midfielderStatisticsSample, playerGeneralInfo, playerSpecificInfo, playersTeam);
//        midfielderStatisticsSample.setPreviousFixturesGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "goals_scored"));
//        midfielderStatisticsSample.setPreviousFixturesAssists(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "assists"));
//        midfielderStatisticsSample.setPreviousFixturesCleanSheets(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "clean_sheets"));
//        midfielderStatisticsSample.setPreviousFixturesGoalsConceded(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "goals_conceded"));
//        midfielderStatisticsSample.setPreviousFixturesChancesCreated(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "big_chances_created"));
//        midfielderStatisticsSample.setPreviousFixturesBlocks(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "clearances_blocks_interceptions"));
//        midfielderStatisticsSample.setPreviousFixturesRecoveries(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "recoveries"));
//        midfielderStatisticsSample.setPreviousFixturesKeyPasses(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "key_passes"));
//        midfielderStatisticsSample.setPreviousFixturesTackles(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "tackles"));
//        midfielderStatisticsSample.setPreviousFixturesWinningGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "winning_goals"));
//
//        midfielderStatisticsSample.setPreviousFixturesChancesMissed(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "big_chances_missed"));
//        midfielderStatisticsSample.setPreviousFixturesFatalErrors(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "errors_leading_to_goal"));
//        midfielderStatisticsSample.setPreviousFixturesErrors(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "errors_leading_to_goal_attempt"));
//        midfielderStatisticsSample.setPreviousFixturesTackled(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "tackled"));
//        midfielderStatisticsSample.setPreviousFixturesFouls(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "fouls"));
//        midfielderStatisticsSample.setPreviousFixturesDribbles(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "dribbles"));


        return midfielderStatisticsSample;
    }

    public ObjectNode buildForwardStatisticsSample(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectNode forwardStatisticsSample = buildGeneralStatistics(playerGeneralInfo, playerSpecificInfo, playersTeam);
        buildPreviousMatchesStatistics(forwardStatisticsSample, playerSpecificInfo.get("history_summary"),
                "goals_scored",
                "assists",
                "big_chances_created",
                "key_passes",
                "winning_goals",
                "big_chances_missed",
                "tackled",
                "fouls",
                "dribbles");

//        buildGeneralStatistics(forwardStatisticsSample, playerGeneralInfo, playerSpecificInfo, playersTeam);
//
//        forwardStatisticsSample.setPreviousFixturesGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "goals_scored"));
//        forwardStatisticsSample.setPreviousFixturesAssists(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "assists"));
//        forwardStatisticsSample.setPreviousFixturesChancesCreated(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "big_chances_created"));
//        forwardStatisticsSample.setPreviousFixturesKeyPasses(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "key_passes"));
//        forwardStatisticsSample.setPreviousFixturesWinningGoals(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "winning_goals"));
//        forwardStatisticsSample.setPreviousFixturesChancesMissed(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "big_chances_missed"));
//        forwardStatisticsSample.setPreviousFixturesTackled(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "tackled"));
//        forwardStatisticsSample.setPreviousFixturesFouls(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "fouls"));
//        forwardStatisticsSample.setPreviousFixturesDribbles(buildPreviousMatchesIntegerStatistics(playerSpecificInfo.get("history_summary"), "dribbles"));

        return forwardStatisticsSample;
    }

    private Double countHistoricalSeasonPointsPerMinute(int numberOfSeasonsBack, JsonNode playerSpecificInfo) {
        JsonNode historicalSeasons = playerSpecificInfo.get("history_past");

        int historicalSeasonsSize = historicalSeasons.size();

        if (historicalSeasonsSize < numberOfSeasonsBack) return null;

        int minutesPlayed = historicalSeasons.get(historicalSeasonsSize - numberOfSeasonsBack).get("minutes").intValue();
        if (minutesPlayed == 0) return 0.0;

        return roundPoints(historicalSeasons.get(historicalSeasonsSize - numberOfSeasonsBack).get("total_points").intValue() / (double) minutesPlayed);
    }

    private double roundPoints(double points) {
        return Math.round(points * 1000) / 1000.0;
    }

    private void buildPreviousMatchesStatistics(ObjectNode playerSample, JsonNode previousMatchesStatistics, String... statisticNames) {
        int previousMatchesNumber = previousMatchesStatistics.size();
        int numberOfMatchesConsidered =
                previousMatchesNumber < numberOfPreviousMatchesConsidered ?
                        previousMatchesNumber : numberOfPreviousMatchesConsidered;

        for (String statisticName : statisticNames) {
            for (int i = 0; i < numberOfMatchesConsidered; i++) {
                playerSample.set("previous_fixtures_".concat(statisticName.concat("_").concat(Integer.toString(i))), previousMatchesStatistics.get(i).get(statisticName));
            }
        }
    }
}
