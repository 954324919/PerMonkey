/**
 * Project Name:AndroidCrash
 * File Name:CrashApplication.java
 * Package Name:com.example.androidcrash
 * Date:2015-12-17上午11:02:01
 * Copyright (c) 2015, chenzhou1025@126.com All Rights Reserved.
 *
*/

package com.example.androidcrash;

import java.util.LinkedList;
import java.util.List;

import android.app.Activity;
import android.app.Application;

/**
 * ClassName:CrashApplication <br/>
 * Function: TODO ADD FUNCTION. <br/>
 * Reason:	 TODO ADD REASON. <br/>
 * Date:     2015-12-17 上午11:02:01 <br/>
 * @author   godma
 * @version  
 * @since    JDK 1.7
 * @see 	 
 */
public class CrashApplication extends Application {

	
	private List<Activity> mList = new LinkedList<Activity>();
	private static CrashApplication instance;
	public static CrashApplication getInstance() {
		return instance;
	}
	@Override
	public void onCreate() {
		// TODO Auto-generated method stub
		super.onCreate();
		instance = this;
		 CrashHandler crashHandler = CrashHandler.getInstance();  
	     crashHandler.init(this);  
	}
	
	public void exit(){
		
		 for(Activity activity:mList){
			 activity.finish();
		 }
		 android.os.Process.killProcess(android.os.Process.myPid());
		 System.exit(0);
	}
	/**
	 * 新建了一个activity
	 * 
	 * @param activity
	 */
	public void addActivity(Activity activity) {
		mList.add(activity);
		//ActionBarColor.initSystemBar(activity);//状态栏和标题栏的颜色保持一致
	}
}

