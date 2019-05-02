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
        playerSample.set("player_id", playerGeneralInfo.get("id"));
        playerSample.set("fixture_id", playerSpecificInfo.get("fixtures_summary").get(0).get("id"));
        playerSample.set("score", null);
        playerSample.set("cost", playerGeneralInfo.get("now_cost"));
        playerSample.set("points_per_game", playerGeneralInfo.get("points_per_game"));
        playerSample.set("form", playerGeneralInfo.get("form"));
        playerSample.set("selected_by_percent", playerGeneralInfo.get("selected_by_percent"));
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
        return playerSample;
    }

    public ObjectNode buildGoalkeeperSample(JsonNode playerGeneralInfo, JsonNode playerSpecificInfo, JsonNode playersTeam) {
        ObjectNode goalkeeperSample = buildGeneralStatistics(playerGeneralInfo, playerSpecificInfo, playersTeam);
        buildPreviousMatchesStatistics(goalkeeperSample, playerSpecificInfo.get("history_summary"),
                "clean_sheets",
                "goals_conceded",
                "penalties_saved",
                "saves");
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
        if (previousMatchesNumber == 0) return;
        int numberOfMatchesConsidered =
                previousMatchesNumber < numberOfPreviousMatchesConsidered ?
                        previousMatchesNumber : numberOfPreviousMatchesConsidered;

        for (String statisticName : statisticNames) {
            double sum = 0.0;
            for (int i = 0; i < numberOfMatchesConsidered; i++) {
                sum += previousMatchesStatistics.get(i).get(statisticName).asDouble();
                playerSample.set("previous_fixtures_".concat(statisticName).concat("_").concat(Integer.toString(i)), previousMatchesStatistics.get(i).get(statisticName));
            }
            playerSample.put("previous_fixtures_".concat(statisticName).concat("_average"), roundPoints(sum / (double) numberOfMatchesConsidered));
        }
    }
}
