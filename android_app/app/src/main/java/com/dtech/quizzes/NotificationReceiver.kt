package com.dtech.quizzes

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import androidx.core.app.NotificationCompat
import java.util.Random

class NotificationReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val type = intent.getStringExtra("NOTIFICATION_TYPE")
        val notificationManager = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

        // Create Notification Channels
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val dailyChannel = NotificationChannel("DAILY_REMINDERS", "Daily Study Reminders", NotificationManager.IMPORTANCE_DEFAULT)
            val weeklyChannel = NotificationChannel("WEEKLY_EXAMS", "Weekly Exams", NotificationManager.IMPORTANCE_HIGH)
            val dtechChannel = NotificationChannel("DTECH_NOTIFICATIONS", "Future D-TECH Notifications", NotificationManager.IMPORTANCE_DEFAULT)

            notificationManager.createNotificationChannel(dailyChannel)
            notificationManager.createNotificationChannel(weeklyChannel)
            notificationManager.createNotificationChannel(dtechChannel)
        }

        if (type == "WEEKLY_EXAM") {
            val notifyIntent = Intent(context, MainActivity::class.java).apply {
                action = Intent.ACTION_VIEW
                data = Uri.parse("https://quiz.dtech-services.co.za/weekly_quiz.html")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            }
            val pendingIntent = PendingIntent.getActivity(context, 0, notifyIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)

            val builder = NotificationCompat.Builder(context, "WEEKLY_EXAMS")
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("\uD83D\uDCDD New Weekly Exam Available!")
                .setContentText("Test your knowledge before its rewards begin decreasing.")
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true)

            notificationManager.notify(1001, builder.build())

            // Reschedule for next week
            NotificationHelper.scheduleWeeklyExamNotification(context)

        } else if (type == "DAILY_REMINDER") {
            val notifyIntent = Intent(context, MainActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            }
            val pendingIntent = PendingIntent.getActivity(context, 0, notifyIntent, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)

            val messages = listOf(
                "\uD83D\uDCDA Time to sharpen your knowledge!",
                "\uD83C\uDFAF Your next quiz is waiting!",
                "\uD83D\uDD25 Keep your learning streak alive!",
                "\uD83D\uDCD6 Complete today's quiz and climb the leaderboard!",
                "\uD83E\uDDE0 Every quiz makes you stronger."
            )
            val randomMessage = messages[Random().nextInt(messages.size)]

            val builder = NotificationCompat.Builder(context, "DAILY_REMINDERS")
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("D-TECH Quizzes")
                .setContentText(randomMessage)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true)

            notificationManager.notify(1002, builder.build())

            // Reschedule for next day
            val sharedPrefs = context.getSharedPreferences("AppPrefs", Context.MODE_PRIVATE)
            val hour = sharedPrefs.getInt("reminder_hour", 18)
            val minute = sharedPrefs.getInt("reminder_minute", 0)
            NotificationHelper.scheduleDailyReminder(context, hour, minute)
        }
    }
}
