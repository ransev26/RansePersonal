package vibesimple.rest.v1.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import vibesimple.rest.v1.domain.AccessRequest;
import vibesimple.rest.v1.domain.AccessResponse;

@RestController
@RequestMapping("access/v1")
@Validated
public class AccessController {
	
	private static final String CC = "cc";
	private static final String APPLICATION_JSON = "application/json";
	private static final String X_APPLICATION_NAME = "X-Application-Name";
	private static final int SUCCESSFUL = 0;
	private static final String MISSING_DATAFORMAT = "Missing dataformat";
	
	
	/**
	 * this method allow Access data of CC
	 * 
	 * @param request
	 * @param applicationName
	 * @return
	 */
	@RequestMapping(produces = APPLICATION_JSON, method = RequestMethod.POST, value = "access")
	public ResponseEntity<AccessResponse> token(@RequestBody AccessRequest request,
	@RequestHeader(value = X_APPLICATION_NAME) String applicationName) {
		AccessResponse accessResponse = new AccessResponse();
		
	
		if (!CC.equals(request.getFormat())) {
			accessResponse.setBadDataCount(1);
			accessResponse.setData(MISSING_DATAFORMAT);
			;
			return ResponseEntity.badRequest().body(accessResponse);
		} else {
			accessResponse.setBadDataCount(SUCCESSFUL);
			accessResponse.setData(request.getData());
			return ResponseEntity.ok(accessResponse);
		}
	
	}
	
}
