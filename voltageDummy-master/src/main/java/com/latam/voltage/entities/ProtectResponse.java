package com.latam.voltage.entities;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

@JsonInclude(Include.NON_NULL)
public class ProtectResponse {
	private int badDataCount;
	private List<Integer> badDataIndices = new ArrayList<>();
	private List<Object> data;
	private String fullIdentity;

	public int getBadDataCount() {
		return badDataCount;
	}

	public void setBadDataCount(int badDataCount) {
		this.badDataCount = badDataCount;
	}

	public List<Integer> getBadDataIndices() {
		return badDataIndices;
	}

	public void setBadDataIndices(List<Integer> badDataIndices) {
		this.badDataIndices = badDataIndices;
	}

	public List<Object> getData() {
		return data;
	}

	public void setData(List<Object> data) {
		this.data = data;
	}

	public String getFullIdentity() {
		return fullIdentity;
	}

	public void setFullIdentity(String fullIdentity) {
		this.fullIdentity = fullIdentity;
	}

	@Override
	public String toString() {
		return "ProtectResponse [badDataCount=" + badDataCount + ", badDataIndices=" + badDataIndices + ", data=" + data
				+ ", fullIdentity=" + fullIdentity + "]";
	}
}
