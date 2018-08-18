package com.latam.voltage.entities;

import java.util.List;

public class ProtectRequest {
	private String format;
	private List<String> data;
	private boolean acceptBadData;

	public String getFormat() {
		return format;
	}

	public void setFormat(String format) {
		this.format = format;
	}

	public List<String> getData() {
		return data;
	}

	public void setData(List<String> data) {
		this.data = data;
	}

	public boolean isAcceptBadData() {
		return acceptBadData;
	}

	public void setAcceptBadData(boolean acceptBadData) {
		this.acceptBadData = acceptBadData;
	}
}
