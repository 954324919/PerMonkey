package com.example.androidcrash;

import android.app.Activity;
import android.os.Bundle;

public class MainActivity extends Activity {

	String a;
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		CrashApplication.getInstance().addActivity(this);
		init();
	}
	public void init(){
		new Thread(new Runnable() {
			
			@Override
			public void run() {
				
				// TODO Auto-generated method stub
				try {
					Thread.sleep(5000);
				} catch (InterruptedException e) {
					
					// TODO Auto-generated catch block
					e.printStackTrace();
					
				}
				System.out.print(a.equals("asdfsd"));
			}
		}).start();
	}
}
