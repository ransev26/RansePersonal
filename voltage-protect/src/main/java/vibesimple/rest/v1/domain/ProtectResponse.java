package vibesimple.rest.v1.domain;

public class ProtectResponse {
	private Integer badDataCount;
	private Integer badDataIndices;
	private String data;
	private String fullIdentity;
	public Integer getBadDataCount() {
		return badDataCount;
	}
	public void setBadDataCount(Integer badDataCount) {
		this.badDataCount = badDataCount;
	}
	public Integer getBadDataIndices() {
		return badDataIndices;
	}
	public void setBadDataIndices(Integer badDataIndices) {
		this.badDataIndices = badDataIndices;
	}
	public String getData() {
		return data;
	}
	public void setData(String data) {
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
		return "VoltageResponse [badDataCount=" + badDataCount + ", badDataIndices=" + badDataIndices + ", data=" + data
				+ ", fullIdentity=" + fullIdentity + "]";
	}
	
}
