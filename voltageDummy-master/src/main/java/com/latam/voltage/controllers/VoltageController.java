package com.latam.voltage.controllers;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import com.latam.voltage.entities.ProtectRequest;
import com.latam.voltage.entities.ProtectResponse;

@RestController
@RequestMapping("vibesimple/rest/v1")
@Validated
public class VoltageController extends LogicVoltageService {

	private static final String APPLICATION_JSON = "application/json";
	private static final String AUTORIZATION = "Authorization";
//	private static final int SUCCESSFUL = 0;

	/**
	 * wrapper of the function protect on voltage
	 * 
	 * @param request
	 * @param applicationName
	 * @return
	 */
	@RequestMapping(produces = APPLICATION_JSON, method = RequestMethod.POST, value = "protect")
	public ResponseEntity<?> protect(@RequestBody ProtectRequest request,
			@RequestHeader(value = AUTORIZATION) String applicationName) {
		ProtectResponse response = new ProtectResponse();

		if (!request.getFormat().equalsIgnoreCase("CC")) {
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
		}

		pseudoLogicVoltageService(response, request,true);

		if (!request.isAcceptBadData() && response.getBadDataCount() > 0) {
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
		}

		return ResponseEntity.ok(response);

	}

	/**
	 * wrapper of the function access on voltage
	 * 
	 * @param request
	 * @param applicationName
	 * @return
	 */
	@RequestMapping(produces = APPLICATION_JSON, method = RequestMethod.POST, value = "access")
	public ResponseEntity<?> access(@RequestBody ProtectRequest request,
			@RequestHeader(value = AUTORIZATION) String applicationName) {
		ProtectResponse response = new ProtectResponse();

		if (!request.getFormat().equalsIgnoreCase("CC")) {
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
		}

		pseudoLogicVoltageService(response, request,false);

		if (!request.isAcceptBadData() && response.getBadDataCount() > 0) {
			return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
		}

		return ResponseEntity.ok(response);

	}

}