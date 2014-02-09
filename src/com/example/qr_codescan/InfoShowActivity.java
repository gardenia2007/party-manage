package com.example.qr_codescan;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.DatePicker.OnDateChangedListener;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.SimpleAdapter;
import android.widget.Toast;

public class InfoShowActivity extends Activity implements OnItemClickListener {
	private ListView list;
	private DatePicker datePicker = null;
	private EditText edit;
	private Button reloadBtn, saveBtn;
	private JSONArray data;
	private SimpleAdapter adapter;
	private String userID;
	private List<HashMap<String, String>> dataList = new ArrayList<HashMap<String, String>>();

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		Intent intent = getIntent();
		userID = intent.getStringExtra("user"); // 获取用户ID（扫描结果）
		setContentView(R.layout.activity_list);
		list = (ListView) findViewById(R.id.info_list);
		reloadBtn = (Button) findViewById(R.id.button_reload);
		saveBtn = (Button) findViewById(R.id.button_save);
		reloadBtn.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				initDataList();
				adapter.notifyDataSetChanged();
			}
		});
		// 保存操作
		saveBtn.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				JSONObject param = new JSONObject();
				try {
					JSONArray infoList = genrateJSONArray();
					param.put("data", infoList);
					param.put("id", userID);
					Log.v("param", param.toString());
				} catch (JSONException e) {
					e.printStackTrace();
				}
				Network net = new Network();
				int status = net.updateInfoList(param);
				if(status == 0){
					showMsgDialog("保存成功！", true);
				}else{
					showMsgDialog("保存失败，请重试！", false);
				}
				Log.v("status", status + "");
			}
		});
		initDataList();
		adapter = new SimpleAdapter(this, dataList, R.layout.info_item,
				new String[] { "name", "value" }, new int[] { R.id.item_name,
						R.id.item_value });
		list.setAdapter(adapter);
		list.setOnItemClickListener(this);
	}
	
	/**
	 * 弹出信息对话框
	 * @param msg 
	 * @param finsh 是否关闭本activity
	 */
	private void showMsgDialog(String msg, final boolean finsh) {
		// 创建对话框
		AlertDialog dlg = new AlertDialog.Builder(InfoShowActivity.this)
				.setTitle("提示").setMessage(msg)
				.setPositiveButton("确定", new DialogInterface.OnClickListener() {// 设置监听事件
							@Override
							public void onClick(DialogInterface dialog,
									int which) {
								dialog.dismiss();
								if(finsh)
									InfoShowActivity.this.finish();
							}
						}).create();// 创建对话框

		dlg.show();// 显示对话框
	}

	/**
	 * 从dataList生成JSONObject
	 * 
	 * @throws JSONException
	 */
	private JSONArray genrateJSONArray() throws JSONException {
		JSONArray data = new JSONArray();
		for (int i = 0; i < dataList.size(); i++) {
			HashMap<String, String> item_list = dataList.get(i);
			JSONObject item = new JSONObject();
			Iterator<String> iterator = item_list.keySet().iterator();
			while (iterator.hasNext()) {
				Object key = iterator.next();
				item.put((String) key, item_list.get(key));
			}
			data.put(item);
		}
		Log.v("data", data.toString());
		return data;
	}

	/**
	 * 设置/更新列表数据
	 */
	private void initDataList() {
		// 显示Progress对话框
		final Dialog myDialog = ProgressDialog.show(InfoShowActivity.this,
				"提示", "正在加载中");
		Network net = new Network();
		data = net.fetchInfoList(userID);
		new Thread() {
			@Override
			public void run() {
				try {
					sleep(500);
				} catch (Exception e) {
					e.printStackTrace();
				} finally { // 卸除所建立的myDialog对象。
					myDialog.dismiss();
				}
			}
		}.start(); /* 开始执行线程 */

		dataList.clear();
		try {
			for (int i = 0; i < data.length(); i++) {
				HashMap<String, String> map = new HashMap<String, String>();
				JSONObject item = (JSONObject) data.get(i);
				map.put("name", item.getString("name"));
				map.put("value", item.getString("value"));
				map.put("filed", item.getString("filed"));
				map.put("type", item.getString("type"));
				dataList.add(map);
			}
		} catch (JSONException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void onItemClick(AdapterView<?> parent, View view,
			final int position, long id) {
		HashMap<String, String> item = dataList.get(position);
		Log.v("item", item.toString());
		LayoutInflater factory = LayoutInflater.from(InfoShowActivity.this);
		final View DialogView; // 自定义对话框
		if (item.get("type").equals("date")) {
			DialogView = factory.inflate(R.layout.dialog_date, null);
			datePicker = (DatePicker) DialogView.findViewById(R.id.date_picker);
			datePicker.updateDate(2014, 1, 1);
		} else {
			DialogView = factory.inflate(R.layout.dialog_count, null);
			edit = (EditText) DialogView.findViewById(R.id.count_edit);
			edit.setText(item.get("value"));
		}
		// 创建对话框
		AlertDialog dlg = new AlertDialog.Builder(InfoShowActivity.this)
				.setTitle("填写").setView(DialogView)
				// 设置自定义对话框样式
				.setPositiveButton("确定", new DialogInterface.OnClickListener() {// 设置监听事件
							@Override
							public void onClick(DialogInterface dialog,
									int which) {
								String value;
								HashMap<String, String> item = dataList
										.get(position);
								if (item.get("type").equals("date")) {
									value = datePicker.getYear() + "-"
											+ (datePicker.getMonth() + 1) + "-"
											+ datePicker.getDayOfMonth();
								} else {
									value = edit.getText().toString();
								}
								item.put("value", value);
								Log.v("item", item.toString());
								dataList.set(position, item);
								adapter.notifyDataSetChanged();
								Toast.makeText(InfoShowActivity.this,
										dataList.toString(), Toast.LENGTH_SHORT)
										.show();
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
}
