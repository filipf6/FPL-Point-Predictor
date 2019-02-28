package com.pk.fpl_point_predictor.persistence.repository;

import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Repository;

@Repository
public class MidfielderSamplesRepository {
    private MongoTemplate mongoTemplate;

    @Autowired
    public MidfielderSamplesRepository(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
    }

    public void save(ObjectNode goalkeeperSample) {
        mongoTemplate.insert(goalkeeperSample.toString(), "midfielder-samples");
    }
}
