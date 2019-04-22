package com.pk.fpl_point_predictor.logic;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.pk.fpl_point_predictor.logic.util.PlayerSampleBuilder;
import com.pk.fpl_point_predictor.persistence.repository.PlayerSamplesRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Service
public class PlayerSamplesService {

    private PlayerSamplesRepository playerSamplesRepository;

    private PlayerSampleBuilder playerSampleBuilder;

    private final int GOALKEEPER_STATISTICS_SAMPLE_NUMBER = 1;
    private final int DEFENDER_STATISTICS_SAMPLE_NUMBER = 2;
    private final int MIDFIELDER_STATISTICS_SAMPLE_NUMBER = 3;
    private final int FORWARD_STATISTICS_SAMPLE_NUMBER = 4;

    private final String allInformationResourceUrl = "https://fantasy.premierleague.com/drf/bootstrap-static";
    private final String playersResourceUrl = "https://fantasy.premierleague.com/drf/element-summary/";

    @Autowired
    public PlayerSamplesService(PlayerSamplesRepository playerSamplesRepository,
                                PlayerSampleBuilder playerSampleBuilder) {
        this.playerSamplesRepository = playerSamplesRepository;
        this.playerSampleBuilder = playerSampleBuilder;
    }

    public void collectCurrentGameweekPlayerSamplesStats() {
        RestTemplate restTemplate = new RestTemplate();
        String teamsResourceUrl = "https://fantasy.premierleague.com/drf/teams";

        ResponseEntity<String> allInformationResponse = restTemplate.getForEntity(allInformationResourceUrl, String.class);
        ResponseEntity<String> teamsResponse = restTemplate.getForEntity(teamsResourceUrl, String.class);

        ObjectMapper mapper = new ObjectMapper();

        try {
            JsonNode playersRoot = mapper.readTree(allInformationResponse.getBody());
            JsonNode teamsRoot = mapper.readTree(teamsResponse.getBody());
            JsonNode playersArray = playersRoot.get("elements");

            for (JsonNode playerGeneralInfo : playersArray) {
                JsonNode playerSpecificInfo = mapper
                        .readTree(restTemplate
                                .getForEntity(playersResourceUrl.concat(playerGeneralInfo.get("id").asText()), String.class)
                                .getBody());

                if ((!playerGeneralInfo.get("status").textValue().equals("d")
                        && !playerGeneralInfo.get("status").textValue().equals("a"))
                        || playerSpecificInfo.get("fixtures_summary").get(0).get("event").intValue()
                        != playersRoot.get("next-event").intValue()) {
                    continue;
                }

                for (JsonNode team : teamsRoot) {
                    if (team.get("id").intValue() == playerGeneralInfo.get("team").intValue()) {
                        switch (playerGeneralInfo.get("element_type").intValue()) {
                            case GOALKEEPER_STATISTICS_SAMPLE_NUMBER:
                                playerSamplesRepository.save(
                                        playerSampleBuilder.buildGoalkeeperSample(playerGeneralInfo, playerSpecificInfo, team),
                                        "goalkeeper-samples");
                                break;
                            case DEFENDER_STATISTICS_SAMPLE_NUMBER:
                                playerSamplesRepository.save(
                                        playerSampleBuilder.buildDefenderStatisticsSample(playerGeneralInfo, playerSpecificInfo, team),
                                        "defender-samples");
                                break;
                            case MIDFIELDER_STATISTICS_SAMPLE_NUMBER:
                                playerSamplesRepository.save(
                                        playerSampleBuilder.buildMidfielderStatisticsSample(playerGeneralInfo, playerSpecificInfo, team),
                                        "midfielder-samples");
                                break;
                            case FORWARD_STATISTICS_SAMPLE_NUMBER:
                                playerSamplesRepository.save(
                                        playerSampleBuilder.buildForwardStatisticsSample(playerGeneralInfo, playerSpecificInfo, team),
                                        "forward-samples");
                                break;
                        }
                        break;
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void collectLastGameweekPlayerSamplesScores() {
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> allInformationResponse = restTemplate.getForEntity(allInformationResourceUrl, String.class);
        ObjectMapper mapper = new ObjectMapper();

        try {
            JsonNode playersRoot = mapper.readTree(allInformationResponse.getBody());
            JsonNode playersArray = playersRoot.get("elements");

            for (JsonNode player : playersArray) {
                JsonNode playerSpecificInfo = mapper
                        .readTree(restTemplate
                                .getForEntity(playersResourceUrl.concat(player.get("id").asText()), String.class)
                                .getBody());

                JsonNode playerHistory = playerSpecificInfo.get("history_summary");
                int playerHistorySize = playerHistory.size();

                // skip if player didn't play last gameweek
                if (playerHistorySize == 0
                        || playerHistory.get(playerHistorySize - 1).get("round").intValue()
                        != playersRoot.get("current-event").intValue()) {
                    continue;
                }

                int matchesBack = isDoubleGameweek(playerHistory) ? 2 : 1;

                int playerId = player.get("id").intValue();
                int fixtureId = playerHistory.get(playerHistorySize - matchesBack).get("fixture").intValue();
                int playerScore = playerHistory.get(playerHistorySize - matchesBack).get("total_points").intValue();

                switch (player.get("element_type").intValue()) {
                    case GOALKEEPER_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                playerScore,
                                "goalkeeper-samples");
                        break;
                    case DEFENDER_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                playerScore,
                                "defender-samples");
                        break;
                    case MIDFIELDER_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                playerScore,
                                "midfielder-samples");
                        break;
                    case FORWARD_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                playerScore,
                                "forward-samples");
                        break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private boolean isDoubleGameweek(JsonNode playerHistory) {
        return playerHistory.size() >= 3 && playerHistory.get(2).get("round").intValue() == playerHistory.get(1).get("round").intValue();
    }
}
