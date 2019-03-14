package com.pk.fpl_point_predictor.logic;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.pk.fpl_point_predictor.logic.util.PlayerSampleBuilder;
import com.pk.fpl_point_predictor.persistence.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Service
public class PlayerSamplesService {

    private GoalkeeperSamplesRepository goalkeeperSamplesRepository;
    private DefenderSamplesRepository defenderSamplesRepository;
    private MidfielderSamplesRepository midfielderSamplesRepository;
    private ForwardSamplesRepository forwardSamplesRepository;
    private PlayerSamplesRepository playerSamplesRepository;

    private PlayerSampleBuilder playerSampleBuilder;

    private final int GOALKEEPER_STATISTICS_SAMPLE_NUMBER = 1;
    private final int DEFENDER_STATISTICS_SAMPLE_NUMBER = 2;
    private final int MIDFIELDER_STATISTICS_SAMPLE_NUMBER = 3;
    private final int FORWARD_STATISTICS_SAMPLE_NUMBER = 4;

    private final String allInformationResourceUrl = "https://fantasy.premierleague.com/drf/bootstrap-static";
    private final String playersResourceUrl = "https://fantasy.premierleague.com/drf/element-summary/";

    @Autowired
    public PlayerSamplesService(GoalkeeperSamplesRepository goalkeeperSamplesRepository,
                                DefenderSamplesRepository defenderSamplesRepository,
                                MidfielderSamplesRepository midfielderSamplesRepository,
                                ForwardSamplesRepository forwardSamplesRepository,
                                PlayerSamplesRepository playerSamplesRepository,
                                PlayerSampleBuilder playerSampleBuilder) {
        this.goalkeeperSamplesRepository = goalkeeperSamplesRepository;
        this.defenderSamplesRepository = defenderSamplesRepository;
        this.midfielderSamplesRepository = midfielderSamplesRepository;
        this.forwardSamplesRepository = forwardSamplesRepository;
        this.playerSamplesRepository = playerSamplesRepository;
        this.playerSampleBuilder = playerSampleBuilder;
    }

    public void collectLastFixtureStats() {
        RestTemplate restTemplate = new RestTemplate();
        String teamsResourceUrl = "https://fantasy.premierleague.com/drf/teams";

        ResponseEntity<String> allInformationResponse = restTemplate.getForEntity(allInformationResourceUrl, String.class);
        ResponseEntity<String> teamsResponse = restTemplate.getForEntity(teamsResourceUrl, String.class);

        ObjectMapper mapper = new ObjectMapper();

        try {
            JsonNode playersRoot = mapper.readTree(allInformationResponse.getBody());
            JsonNode teamsRoot = mapper.readTree(teamsResponse.getBody());
            JsonNode playersArray = playersRoot.get("elements");

            ObjectNode playerSample;

            for (JsonNode playerGeneralInfo : playersArray) {
                playerSample = mapper.createObjectNode();

                JsonNode playerSpecificInfo = mapper
                        .readTree(restTemplate
                                .getForEntity(playersResourceUrl + playerGeneralInfo.get("id").asText(), String.class)
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
//                                playerSample.set("player_id", playerGeneralInfo.get("id"));
//                                playerSample.set("fixture_id", playerSpecificInfo.get("fixtures_summary").get(0).get("id"));
//                                playerSample.set("cost", playerGeneralInfo.get("now_cost"));
//
//
//                                int previousMatchesNumber = playerSpecificInfo.get("history_summary").size();
//                                int numberOfMatchesConsidered =
//                                        previousMatchesNumber < 3 ?
//                                                previousMatchesNumber : 3;
//
//                                for (int i = 0; i < numberOfMatchesConsidered; i++) {
//                                    playerSample.set("previous_fixture_points_"+i, playerSpecificInfo.get("history_summary").get(i).get("total_points"));
//                                }
//                                playerSample.set("score", null);
//
//                                goalkeeperSamplesRepository.save(playerSample);
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

//            Document doc = Document.parse(playersArray.get(0).toString());
            /// mongoTemplate.insert(playersArray.get(0).toString(), "players");
//            mongoTemplate.insert(doc, "players");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void collectLastFixtureScores() {
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<String> allInformationResponse = restTemplate.getForEntity(allInformationResourceUrl, String.class);
        ObjectMapper mapper = new ObjectMapper();

        JsonNode playersRoot = null;
        try {
            playersRoot = mapper.readTree(allInformationResponse.getBody());
            JsonNode playersArray = playersRoot.get("elements");

            int playerId, fixtureId, playerHistorySize;
            JsonNode playerHistory;

            for (JsonNode player : playersArray) {
                JsonNode playerSpecificInfo = mapper
                        .readTree(restTemplate
                                .getForEntity(playersResourceUrl + player.get("id").asText(), String.class)
                                .getBody());

                playerHistory = playerSpecificInfo.get("history-summary");
                playerHistorySize = playerHistory.size();

                // skip if player didn't play last gameweek
                if (playerHistorySize == 0
                        || playerHistory.get(playerHistorySize - 1).get("round").intValue() + 1
                        != playersRoot.get("next-event").intValue()) {
                    continue;
                }

                playerId = player.get("id").intValue();
                fixtureId = playerHistory.get(playerHistorySize - 1).get("fixture").intValue();

                switch (player.get("element_type").intValue()) {
                    case GOALKEEPER_STATISTICS_SAMPLE_NUMBER:
//                        playerSamplesRepository.updateScore(
//                                playerId,
//                                fixtureId,
//                                playerPoints,
//                                "goalkeeper-samples");

                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                isDoubleGameweek(playerHistory) ? playerHistory.get(1).get("total_points").intValue() : player.get("event_points").intValue(),
                                "goalkeeper-samples");
//                        GoalkeeperStatisticsSample goalkeeper =
//                                this.goalkeeperStatisticsSampleRepository.findFirstByPlayerIdAndFixtureId(playerId, fixtureId);
//                        if(goalkeeper == null) break;
//                        goalkeeper.setScore(player.get("event_points").intValue());
//                        this.goalkeeperStatisticsSampleRepository.save(goalkeeper);
                        break;
                    case DEFENDER_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                isDoubleGameweek(playerHistory) ? playerHistory.get(1).get("total_points").intValue() : player.get("event_points").intValue(),
                                "defender-samples");
//                        DefenderStatisticsSample defender =
//                                this.defenderStatisticsSampleRepository.findFirstByPlayerIdAndFixtureId(playerId, fixtureId);
//                        if(defender == null) break;
//                        defender.setScore(player.get("event_points").intValue());
//                        this.defenderStatisticsSampleRepository.save(defender);
                        break;
                    case MIDFIELDER_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                isDoubleGameweek(playerHistory) ? playerHistory.get(1).get("total_points").intValue() : player.get("event_points").intValue(),
                                "midfielder-samples");
//                        MidfielderStatisticsSample midfielder =
//                                this.midfielderStatisticsSampleRepository.findFirstByPlayerIdAndFixtureId(playerId, fixtureId);
//                        if(midfielder == null) break;
//                        midfielder.setScore(player.get("event_points").intValue());
//                        this.midfielderStatisticsSampleRepository.save(midfielder);
                        break;
                    case FORWARD_STATISTICS_SAMPLE_NUMBER:
                        playerSamplesRepository.updateScore(
                                playerId,
                                fixtureId,
                                isDoubleGameweek(playerHistory) ? playerHistory.get(1).get("total_points").intValue() : player.get("event_points").intValue(),
                                "forward-samples");
//                        ForwardStatisticsSample forward =
//                                this.forwardStatisticsSampleRepository.findFirstByPlayerIdAndFixtureId(playerId, fixtureId);
//                        if(forward == null) break;
//                        forward.setScore(player.get("event_points").intValue());
//                        this.forwardStatisticsSampleRepository.save(forward);
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
