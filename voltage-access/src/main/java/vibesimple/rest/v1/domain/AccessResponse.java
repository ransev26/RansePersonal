package vibesimple.rest.v1.domain;


public class AccessResponse {
	
	private Integer badDataCount;
	private Integer badDataIndices;
	private String data;
	
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
	@Override
	public String toString() {
		return "VoltageResponse [badDataCount=" + badDataCount + ", badDataIndices=" + badDataIndices + ", data=" + data
				+ "]";
	}
	

}
