package com.pk.fpl_point_predictor.controller;

import com.pk.fpl_point_predictor.logic.PlayerSamplesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/player-samples")
public class PlayerSamplesController {

    private PlayerSamplesService dataCollectorService;

    @Autowired
    public PlayerSamplesController(PlayerSamplesService dataCollectorService) {
        this.dataCollectorService = dataCollectorService;
    }

    @RequestMapping(value = "/current-gameweek-samples", method = RequestMethod.POST, consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> collectCurrentGameweekSamples() {
        this.dataCollectorService.collectCurrentGameweekSamples();
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @RequestMapping(value = "/last-gameweek-samples-scores", method = RequestMethod.PATCH, consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> collectLastGameweekSamplesScores() {
        this.dataCollectorService.collectLastGameweekSamplesScores();
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
