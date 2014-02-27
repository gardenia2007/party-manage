package cn.edu.hit.csparty;


import org.json.JSONObject;
import cn.edu.hit.csparty.R;
import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class BeforeLogin extends Activity {
	protected static final Exception Execption = null;
	private TextView login_name, login_pw; // 用户登录用户名、密码
	private Button login_btn; // 显示详细信息按钮
	private JSONObject result; // 扫描得到的结果字符串

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_login);

		login_name = (TextView) findViewById(R.id.login_name);
//		login_name.setText("红红");
		login_pw = (TextView) findViewById(R.id.login_pw);
//		login_pw.setText("123");
		login_btn = (Button) findViewById(R.id.login_btn);
		// 验证密码是否正确，获取党支部信息
		// 跳转到MainActivity
		login_btn.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				JSONObject param = new JSONObject();
				try {
//					param.put("name", URLEncoder.encode(login_name.getText().toString(), "utf-8"));
					param.put("name", login_name.getText().toString());
					param.put("pw", login_pw.getText());
					Network net = new Network();
					result = net.loginAction(param);
					if(result == null){ // network error
						throw Execption;
					}
					Log.v("login", result.toString());
					Log.v("login_name", login_name.getText().toString());

					if (result.getBoolean("status")) { // 登录成功，设置党支部信息
						Toast.makeText(BeforeLogin.this, "登录成功！", Toast.LENGTH_LONG).show();
						Intent intent = new Intent();
						intent.putExtra("zb_id", result.getInt("zb_id"));
						intent.putExtra("zb_name", result.getString("zb_name"));
						intent.putExtra("name", login_name.getText().toString());
						intent.setClass(BeforeLogin.this, MainActivity.class);
						intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
						startActivity(intent);
					}else{
						Toast.makeText(BeforeLogin.this, "登录失败，请检查登录名与密码！", Toast.LENGTH_LONG).show();
					}
				} catch (Exception e) {
					Toast.makeText(BeforeLogin.this, "网络或服务器错误，请重试！", Toast.LENGTH_LONG).show();
					e.printStackTrace();
				}
			}
		});
	}

}
