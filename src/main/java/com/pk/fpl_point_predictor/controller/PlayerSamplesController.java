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

    private PlayerSamplesService playerSamplesService;

    @Autowired
    public PlayerSamplesController(PlayerSamplesService playerSamplesService) {
        this.playerSamplesService = playerSamplesService;
    }

    @RequestMapping(value = "/current-gameweek-stats", method = RequestMethod.POST, consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> collectCurrentGameweekStats() {
        this.playerSamplesService.collectCurrentGameweekPlayerSamplesStats();
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @RequestMapping(value = "/last-gameweek-scores", method = RequestMethod.PATCH, consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE,
            produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> collectLastGameweekScores() {
        this.playerSamplesService.collectLastGameweekPlayerSamplesScores();
        return new ResponseEntity<>(HttpStatus.OK);
    }

    @RequestMapping(value = "/test-url", method = RequestMethod.GET)
    public ResponseEntity<?> testMethod() {
        System.out.println("test Succesful!");
        return new ResponseEntity<>(HttpStatus.OK);
    }
}
