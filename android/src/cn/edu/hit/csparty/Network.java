/**
 * 
 */
package cn.edu.hit.csparty;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URI;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
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
//	private String host = "http://10.0.2.2:8080/m/";

	/**
	 * 从远程服务器获取字符串
	 * 
	 * @return String
	 * @throws IOException
	 * @throws ClientProtocolException
	 */
	private String fetchRemoteUrl(String path) throws ClientProtocolException,
			IOException {
		URI url = URI.create(path);
		HttpGet request = new HttpGet(url);
		String retSrc = null;
		// 发送请求
		HttpResponse httpResponse = new DefaultHttpClient().execute(request);
		// 得到应答的字符串，这也是一个 JSON 格式保存的数据
		retSrc = EntityUtils.toString(httpResponse.getEntity());
		return retSrc;
	}

	/**
	 * POST数据到远程
	 * @throws Exception 
	 */
	public JSONObject postRemote(String path, String param) throws Exception {
		HttpPost request = new HttpPost(path);
		StringEntity se;
		se = new StringEntity(param, "UTF-8");
		Log.v("path", path);
		Log.v("param", param);
		// 绑定到请求 Entry
		request.setEntity(se);
		// 发送请求
		HttpResponse httpResponse = new DefaultHttpClient().execute(request);
		// 得到应答的字符串，这也是一个 JSON 格式保存的数据
		String retSrc = EntityUtils.toString(httpResponse.getEntity());
		Log.v("ret", retSrc);
		// 生成 JSON 对象
		JSONObject result = new JSONObject(retSrc);
		return result;

	}

	/**
	 * 更新信息列表
	 */
	public int updateInfoList(String ID, JSONArray param) {
		int status;
		try {
			JSONObject result = postRemote(host + ID + "/info/update", param.toString());
			status = result.optInt("status");
		} catch (Exception e) {
			e.printStackTrace();
			status = -1;
		}
		return status;
	}
	
	/**
	 * 登录并获取所管理的党支部信息
	 */
	public JSONObject loginAction(JSONObject param){
		JSONObject result;
		try {
			result = postRemote(host + "admin/login", param.toString());
		} catch (Exception e) {
			e.printStackTrace();
			result = null;
		}
		return result;
	}

	/**
	 * 获取个人信息列表
	 */
	public JSONArray fetchInfoList(String ID) {
		// String str =
		// "["{\"filed\":\"sqs_fz\", \"name\":\"申请书\",   \"value\":\"2010-09-12\",\"type\":\"date\"}]";
		try {
			String str = fetchRemoteUrl(host + ID + "/info");
			Log.v("url", host + ID + "/info");
			Log.v("str", str);
			return new JSONArray(str);
		} catch (Exception e) {
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
		try {
			String str = fetchRemoteUrl(host + ID + "/info/basic");
			Log.v("str", str);
			return new JSONObject(str);
		} catch (Exception e) {
			e.printStackTrace();
			return new JSONObject();
		}
	}
}
