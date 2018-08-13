package vibesimple.rest.v1.domain;

public class AccessRequest {
	
	private String format;
	private String data;
	private Boolean applyMasking;
	private String primaryNamespace;
	private String secondaryNamespace;
	private String tweak;
	private Boolean acceptBadData;
	public String getFormat() {
		return format;
	}
	public void setFormat(String format) {
		this.format = format;
	}
	public String getData() {
		return data;
	}
	public void setData(String data) {
		this.data = data;
	}
	public Boolean getApplyMasking() {
		return applyMasking;
	}
	public void setApplyMasking(Boolean applyMasking) {
		this.applyMasking = applyMasking;
	}
	public String getPrimaryNamespace() {
		return primaryNamespace;
	}
	public void setPrimaryNamespace(String primaryNamespace) {
		this.primaryNamespace = primaryNamespace;
	}
	public String getSecondaryNamespace() {
		return secondaryNamespace;
	}
	public void setSecondaryNamespace(String secondaryNamespace) {
		this.secondaryNamespace = secondaryNamespace;
	}
	public String getTweak() {
		return tweak;
	}
	public void setTweak(String tweak) {
		this.tweak = tweak;
	}
	public Boolean getAcceptBadData() {
		return acceptBadData;
	}
	public void setAcceptBadData(Boolean acceptBadData) {
		this.acceptBadData = acceptBadData;
	}
	@Override
	public String toString() {
		return "VolatgeRequest [format=" + format + ", data=" + data + ", applyMasking=" + applyMasking
				+ ", primaryNamespace=" + primaryNamespace + ", secondaryNamespace=" + secondaryNamespace + ", tweak="
				+ tweak + ", acceptBadData=" + acceptBadData + "]";
	}
	

}
