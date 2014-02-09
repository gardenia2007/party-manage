/**
 * 
 */
package com.example.qr_codescan;

import java.io.UnsupportedEncodingException;
import java.net.URI;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.util.Log;

/**
 * @author y
 * 
 */
public class Network {
	private String host = "http://partyonline.sinaapp.com/";

	/**
	 * 从远程服务器获取字符串
	 * 
	 * @return String
	 */
	private String fetchRemoteUrl(String path) {
		URI url = URI.create(path);
		HttpPost request = new HttpPost(url);
		String retSrc = null;
		try {
			// 发送请求
			HttpResponse httpResponse = new DefaultHttpClient()
					.execute(request);
			// 得到应答的字符串，这也是一个 JSON 格式保存的数据
			retSrc = EntityUtils.toString(httpResponse.getEntity());
		} catch (Exception e) {
			e.printStackTrace();
		}
		return retSrc;
	}

	/**
	 * POST数据到远程
	 */
	public int postRemote(String path, JSONObject param) {
		HttpPost request = new HttpPost(path);
		StringEntity se;
		int token = -1;
		try {
			se = new StringEntity(param.toString());
			// 绑定到请求 Entry
			request.setEntity(se);
			// 发送请求
			HttpResponse httpResponse = new DefaultHttpClient()
					.execute(request);
			// 得到应答的字符串，这也是一个 JSON 格式保存的数据
			String retSrc = EntityUtils.toString(httpResponse.getEntity());
			Log.v("ret", retSrc);
			// 生成 JSON 对象
			JSONObject result = new JSONObject(retSrc);
			token = result.optInt("status"); // 默认返回0
		} catch (Exception e) {
			e.printStackTrace();
		}
		return token;

	}
	/**
	 * 更新信息列表
	 */
	public int updateInfoList(JSONObject param){
		return postRemote(host+"update_info.php", param);
	}
	/**
	 * 获取个人信息列表
	 */
	public JSONArray fetchInfoList(String ID) {
		String str = fetchRemoteUrl(host + "info.php?id=" + ID);
		// String str = "["
		// +
		// "{\"filed\":\"sqs_fz\", \"name\":\"申请书\",   \"value\":\"2010-09-12\",\"type\":\"date\"},"
		// +
		// "{\"filed\":\"xskc_fz\",\"name\":\"写实考察表\",\"value\":\"2010-11-02\",\"type\":\"date\"},"
		// +
		// "{\"filed\":\"sxhb_fz\",\"name\":\"思想汇报\",  \"value\":\"2\"			,\"type\":\"count\"},"
		// +
		// "{\"filed\":\"zys_fz\", \"name\":\"志愿书\",    \"value\":\"\"			,\"type\":\"date\"}"
		// + "]";
		try {
			return new JSONArray(str);
		} catch (JSONException e) {
			e.printStackTrace();
			return new JSONArray();
		}
	}

	/**
	 * 获取基本信息
	 * 
	 * @return JSONObject
	 */
	public JSONObject fetchUserInfo() {
		String r = fetchRemoteUrl(host + "basic_info.php");
		// String r = "{\"name\":\"李洪祥\"}";
		try {
			return new JSONObject(r);
		} catch (JSONException e) {
			e.printStackTrace();
			return new JSONObject();
		}
	}
}
