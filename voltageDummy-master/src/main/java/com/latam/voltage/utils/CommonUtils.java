package com.latam.voltage.utils;

import java.util.Random;

public class CommonUtils {

	public static boolean validateCard(String creditCard) {
		if (creditCard.length() == 16) {
			return true;
		}
		return false;
	}

	public static String ofusCard(String creditCard) {

		return creditCard.substring(0, 4) + "********" + creditCard.substring(creditCard.toCharArray().length - 4);

	}

	public static String desofusCard(String ofuscard) {
		String response = "";

		for (String element : ofuscard.split("")) {
			if (element.equalsIgnoreCase("*")) {
				response += new Random().nextInt(10);
			} else {
				response += element;
			}
		}
		return response;
	}

}
