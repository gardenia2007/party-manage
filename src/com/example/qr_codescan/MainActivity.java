package com.example.qr_codescan;


import java.net.URI;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

public class MainActivity extends Activity {
	private final static int SCANNIN_GREQUEST_CODE = 1;
	/**
	 * 显示扫描结果
	 */
	private TextView mTextView ;
	/**
	 * 显示扫描拍的图片
	 */
	private ImageView mImageView;
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		mTextView = (TextView) findViewById(R.id.result); 
		mImageView = (ImageView) findViewById(R.id.qrcode_bitmap);
		
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
				try{
					URI url = URI.create("http://www.baidu.com");
					HttpPost request = new HttpPost(url);
					// 先封装一个 JSON 对象
					JSONObject param = new JSONObject();
					param.put("name", "rarnu");
					param.put("password", "123456");
					// 绑定到请求 Entry
					StringEntity se = new StringEntity(param.toString()); 
					request.setEntity(se);
					// 发送请求
					HttpResponse httpResponse = new DefaultHttpClient().execute(request);
					// 得到应答的字符串，这也是一个 JSON 格式保存的数据
					String retSrc = EntityUtils.toString(httpResponse.getEntity());
					// 生成 JSON 对象
					JSONObject result = new JSONObject( retSrc);
					String token = (String) result.get("token");
				}catch(Exception e) {
		            e.printStackTrace();
				}
				//显示扫描到的内容
				mTextView.setText(bundle.getString("result"));
				
				//显示
				mImageView.setImageBitmap((Bitmap) data.getParcelableExtra("bitmap"));
			}
			break;
		}
    }	

}
