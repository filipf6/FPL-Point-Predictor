package com.pk.fpl_point_predictor.persistence.repository;

import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
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

    //mongoTemplate.insert(on.toString(), "goalkeeper_samples");
    //
    //
    //Query query = new Query();
    //query.addCriteria(Criteria.where("player_id").is(playerGeneralInfo.get("id").intValue()).and("fixture_id").is(playerSpecificInfo.get("fixtures_summary").get(0).get("id").intValue()));
    //Update update = new Update();
    //update.set("score", 10);
    //mongoTemplate.updateFirst(query, update, "goalkeeper_samples");
}
