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
                                PlayerSampleBuilder playerSampleBuilder) {
        this.goalkeeperSamplesRepository = goalkeeperSamplesRepository;
        this.defenderSamplesRepository = defenderSamplesRepository;
        this.midfielderSamplesRepository = midfielderSamplesRepository;
        this.forwardSamplesRepository = forwardSamplesRepository;
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
                                goalkeeperSamplesRepository.save(playerSampleBuilder.buildGoalkeeperSample(playerGeneralInfo, playerSpecificInfo, team));
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
                                defenderSamplesRepository.save(playerSampleBuilder.buildDefenderStatisticsSample(playerGeneralInfo, playerSpecificInfo, team));
                                break;
                            case MIDFIELDER_STATISTICS_SAMPLE_NUMBER:
                                midfielderSamplesRepository.save(playerSampleBuilder.buildMidfielderStatisticsSample(playerGeneralInfo, playerSpecificInfo, team));
                                break;
                            case FORWARD_STATISTICS_SAMPLE_NUMBER:
                                forwardSamplesRepository.save(playerSampleBuilder.buildForwardStatisticsSample(playerGeneralInfo, playerSpecificInfo, team));
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

    }
}
