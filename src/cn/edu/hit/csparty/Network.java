/**
 * 
 */
package cn.edu.hit.csparty;

import java.net.URI;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
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
	private String host = "http://csparty.sinaapp.com/m/";

	/**
	 * 从远程服务器获取字符串
	 * 
	 * @return String
	 */
	private String fetchRemoteUrl(String path) {
		URI url = URI.create(path);
		HttpGet request = new HttpGet(url);
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
	public int postRemote(String path, String param) {
		HttpPost request = new HttpPost(path);
		StringEntity se;
		int token = -1;
		try {
			se = new StringEntity(param);
			Log.v("path", path);
			Log.v("param", param);
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
	public int updateInfoList(String ID, JSONArray param){
		return postRemote(host+ ID +"/info/update", param.toString());
	}
	/**
	 * 获取个人信息列表
	 */
	public JSONArray fetchInfoList(String ID) {
		String str = fetchRemoteUrl(host + ID + "/info");
		Log.v("url", host + ID + "/info");
		Log.v("str", str);
		// String str = "["{\"filed\":\"sqs_fz\", \"name\":\"申请书\",   \"value\":\"2010-09-12\",\"type\":\"date\"}]";
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
	public JSONObject fetchUserInfo(String ID) {
		String str = fetchRemoteUrl(host + ID + "/info/basic");
		// String r = "{\"name\":\"李洪祥\"}";
		Log.v("url", host + ID + "/info");
		Log.v("str", str);
		try {
			return new JSONObject(str);
		} catch (JSONException e) {
			e.printStackTrace();
			return new JSONObject();
		}
	}
}
