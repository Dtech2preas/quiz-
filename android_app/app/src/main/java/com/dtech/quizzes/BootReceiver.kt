package com.dtech.quizzes

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            val sharedPrefs = context.getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
            val isDailyReminderEnabled = sharedPrefs.getBoolean("is_daily_reminder_enabled", false)

            if (isDailyReminderEnabled) {
                val hour = sharedPrefs.getInt("reminder_hour", 18)
                val minute = sharedPrefs.getInt("reminder_minute", 0)
                NotificationHelper.scheduleDailyReminder(context, hour, minute)
            }

            // Always schedule weekly exams
            NotificationHelper.scheduleWeeklyExamNotification(context)
        }
    }
}
