package com.example.qr_codescan;


import java.net.URI;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;


public class MainActivity extends Activity {
	private final static int SCANNIN_GREQUEST_CODE = 1;
	private TextView usernameView; // 用户名字
	private Button showBtn; // 显示详细信息按钮
	private String result; // 扫描得到的结果字符串

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		usernameView = (TextView) findViewById(R.id.username);
		showBtn = (Button) findViewById(R.id.show_info);
		
		//点击按钮跳转到二维码扫描界面，这里用的是startActivityForResult跳转
		//扫描完了之后调到该界面
		Button mButton = (Button) findViewById(R.id.button1);
		mButton.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View v) {
				Intent intent = new Intent();
				intent.setClass(MainActivity.this, MipcaActivityCapture.class);
				intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
				startActivityForResult(intent, SCANNIN_GREQUEST_CODE);
			}
		});
	}
	
	
	@Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        switch (requestCode) {
		case SCANNIN_GREQUEST_CODE:
			if(resultCode == RESULT_OK){
				Bundle bundle = data.getExtras();
				result = bundle.getString("result"); // 扫描得到的内容
				afterScan();
			}
			break;
		}
    }
	// 测试按钮
	public void testButton(View view){
		result = "Test";
		afterScan();
	}
	/**
	 * 扫描完成后的操作，显示基本信息等
	 */
	private void afterScan(){
		Network net = new Network();
		// 从服务器上获取基本信息
		String username = "";
		try {
			username = "你好："+net.fetchUserInfo().getString("name");
		} catch (JSONException e) {
			e.printStackTrace();
		}
		usernameView.setText(username);
		showBtn.setVisibility(View.VISIBLE);
	}
	/**
	 * 显示完整的信息列表
	 */
	public void showInfoList(View view){
		// 显示信息
		Intent intent = new Intent();
		intent.setClass(MainActivity.this, InfoShowActivity.class);
		intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
		intent.putExtra("user", result); // 把扫描结果传递过去
		startActivity(intent);
	}

}
