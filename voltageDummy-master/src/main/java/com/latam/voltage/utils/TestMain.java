package com.latam.voltage.utils;

import org.slf4j.LoggerFactory;

public class TestMain {

	public static void main(String[] args) {
		final org.slf4j.Logger logger = LoggerFactory
	            .getLogger(TestMain.class);
		
		if(CommonUtils.validateCard("4697720585000063")) {
//			System.out.println(CommonUtils.ofusCard("4697720585000063"));
			logger.info(CommonUtils.ofusCard("4697720585000063"));
		}
		
//		System.out.println(CommonUtils.desofusCard(CommonUtils.ofusCard("4697720585000063")));
		logger.info(CommonUtils.desofusCard(CommonUtils.ofusCard("4697720585000063")));
//		System.out.println(CommonUtils.desofusCard("**44*******44**5"));
		CommonUtils.desofusCard(CommonUtils.desofusCard("**44*******44**5"));
		

	}

}
