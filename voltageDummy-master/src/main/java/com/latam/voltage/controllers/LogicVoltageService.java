package com.latam.voltage.controllers;

import java.util.ArrayList;
import java.util.List;

import com.latam.voltage.entities.ProtectRequest;
import com.latam.voltage.entities.ProtectResponse;
import com.latam.voltage.utils.CommonUtils;

public class LogicVoltageService {

	public LogicVoltageService() {
		super();
	}

	protected void pseudoLogicVoltageService(ProtectResponse response, ProtectRequest request, boolean obfuscate) {
		int badDataAccount = 0;
		List<Integer> badDataIndexs = new ArrayList<>();
	
		response.setData(new ArrayList<>());
	
		for (int i = 0; i < request.getData().size(); i++) {
			String data = request.getData().get(i);
	
			if (CommonUtils.validateCard(data)) {
				if(obfuscate) {
					response.getData().add(CommonUtils.ofusCard(data));
				}else{
					response.getData().add(CommonUtils.desofusCard(data));
				}
				
			} else {
				badDataIndexs.add(i);
				badDataAccount++;
				response.getData().add(
						"{\"errorCode\":400,\"errorMessage\":\"error de tarjeta\",\"skippedData\":\"" + data + "\"}");
			}
		}
	
		response.setBadDataCount(badDataAccount);
		response.setBadDataIndices(badDataIndexs);
	
	}

}