package com.pk.fpl_point_predictor.persistence.repository;

import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Repository;

@Repository
public class GoalkeeperSamplesRepository {

    private MongoTemplate mongoTemplate;

    @Autowired
    public GoalkeeperSamplesRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    public void save(ObjectNode goalkeeperSample) {
        mongoTemplate.insert(goalkeeperSample.toString(), "goalkeeper-samples");
    }

    public void updateScore(int playerId, int fixtureId, int score) {
        //mongoTemplate.insert(on.toString(), "goalkeeper_samples");
        //playerGeneralInfo.get("id").intValue()
        //playerSpecificInfo.get("fixtures_summary").get(0).get("id").intValue()
        Query query = new Query();
        query.addCriteria(Criteria.where("player_id").is(playerId).and("fixture_id").is(fixtureId));
        Update update = new Update();
        update.set("score", score);
        mongoTemplate.updateFirst(query, update, "goalkeeper_samples");
    }


}
