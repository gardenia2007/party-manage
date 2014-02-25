package cn.edu.hit.csparty;

import java.util.HashMap;

import org.json.JSONException;
import org.json.JSONObject;

import cn.edu.hit.csparty.R;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity {
	private final static int SCANNIN_GREQUEST_CODE = 1;
	private TextView usernameView; // 用户名字
	private Button showBtn; // 显示详细信息按钮
	private String result; // 扫描得到的结果字符串

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main_new);

		usernameView = (TextView) findViewById(R.id.username);
		showBtn = (Button) findViewById(R.id.show_info);

		// 点击按钮跳转到二维码扫描界面，这里用的是startActivityForResult跳转
		// 扫描完了之后调到该界面
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
			if (resultCode == RESULT_OK) {
				Bundle bundle = data.getExtras();
				result = bundle.getString("result"); // 扫描得到的内容
				afterScan();
			}
			break;
		}
	}

	// 测试按钮
	public void testButton(View view) {
		result = "1100300220";
		afterScan();
	}

	/**
	 * 手动输入编号
	 */
	public void scanInput(View view) {
		LayoutInflater factory = LayoutInflater.from(MainActivity.this);
		final View DialogView; // 自定义对话框
		DialogView = factory.inflate(R.layout.dialog_input_no, null);
		final EditText edit = (EditText) DialogView
				.findViewById(R.id.scan_input);
		edit.setText("1100300220");
		// 创建对话框
		AlertDialog dlg = new AlertDialog.Builder(MainActivity.this)
				.setTitle("填写").setView(DialogView)
				// 设置自定义对话框样式
				.setPositiveButton("确定", new DialogInterface.OnClickListener() {// 设置监听事件
							@Override
							public void onClick(DialogInterface dialog,
									int which) {
								result = edit.getText().toString(); // 获取手动输入的编号
								afterScan();
							}
						}).setNegativeButton("取消",// 设置取消按钮
						new DialogInterface.OnClickListener() {
							@Override
							public void onClick(DialogInterface dialog,
									int which) {
								// 点击取消后退出程序
							}
						}).create();// 创建对话框

		dlg.show();// 显示对话框
	}

	/**
	 * 扫描完成后的操作，显示基本信息等
	 */
	private void afterScan() {
		Network net = new Network();
		// 从服务器上获取基本信息
		JSONObject info = net.fetchUserInfo(result);
		String text = "扫描结果\n编号：" + result;
		try {
			Log.v("info", info.toString());
			Log.v("bool", info.getBoolean("status") + "");
			String t;
			if (info.getBoolean("status")) { // 成功
				t = "\n姓名：" + info.getString("name") + "\n支部："
						+ info.getString("zb");
				showBtn.setVisibility(View.VISIBLE);
			} else {
				t = "\n无相关信息。";
				showBtn.setVisibility(View.INVISIBLE);
			}
			Log.v("t", t);
			String a = text + t;
			Log.v("a", a);
			usernameView.setText(a);
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}

	/**
	 * 显示完整的信息列表
	 */
	public void showInfoList(View view) {
		// 显示信息
		Intent intent = new Intent();
		intent.setClass(MainActivity.this, InfoShowActivity.class);
		intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
		intent.putExtra("user", result); // 把扫描结果传递过去
		startActivity(intent);
	}

}
