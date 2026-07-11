package com.dtech.quizzes

import android.app.Activity
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Handler
import android.os.Looper
import android.webkit.JavascriptInterface
import android.widget.Toast
import androidx.core.content.FileProvider
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

class AppUpdater(private val activity: Activity) {

    private val client = OkHttpClient()

    @JavascriptInterface
    fun getAppVersion(): String {
        return BuildConfig.GIT_TAG
    }

    @JavascriptInterface
    fun checkForUpdates(callbackName: String) {
        val request = Request.Builder()
            .url("https://quiz.dtech-services.co.za/version.json")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                notifyFrontend(callbackName, "error", "Network error checking for updates")
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    notifyFrontend(callbackName, "error", "Failed to check update: HTTP ${response.code}")
                    return
                }

                try {
                    val responseBody = response.body?.string()
                    if (responseBody == null) {
                        notifyFrontend(callbackName, "error", "Empty response from server")
                        return
                    }

                    val json = JSONObject(responseBody)
                    val newVersion = json.optString("version", "")

                    val currentVersion = BuildConfig.GIT_TAG

                    // If dev-build or matches, no update
                    if (currentVersion == "dev-build") {
                        notifyFrontend(callbackName, "no_update", "Dev build, skipping update check.")
                        return
                    }

                    if (newVersion == currentVersion || newVersion.isEmpty()) {
                        notifyFrontend(callbackName, "no_update", "App is up to date.")
                        return
                    }

                    val downloadUrl = json.optString("apk", "")
                    if (downloadUrl.isNotEmpty()) {
                        // Display release notes if available
                        val releaseNotesArray = json.optJSONArray("releaseNotes")
                        var releaseNotes = "Downloading update..."
                        if (releaseNotesArray != null && releaseNotesArray.length() > 0) {
                            val notesList = mutableListOf<String>()
                            for (i in 0 until releaseNotesArray.length()) {
                                notesList.add(releaseNotesArray.getString(i))
                            }
                            releaseNotes = notesList.joinToString("\n")
                        }

                        notifyFrontend(callbackName, "update_available", releaseNotes)
                        notifyFrontend(callbackName, "downloading", "Downloading update...")
                        downloadAndInstallApk(downloadUrl, callbackName)
                    } else {
                        notifyFrontend(callbackName, "error", "No APK URL found in release.")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    notifyFrontend(callbackName, "error", "Failed to parse update info.")
                }
            }
        })
    }

    private fun downloadAndInstallApk(url: String, callbackName: String) {
        val request = Request.Builder().url(url).build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                notifyFrontend(callbackName, "error", "Failed to download update.")
            }

            override fun onResponse(call: Call, response: Response) {
                if (!response.isSuccessful) {
                    notifyFrontend(callbackName, "error", "Download failed: HTTP ${response.code}")
                    return
                }

                try {
                    val apkFile = File(activity.cacheDir, "update.apk")
                    if (apkFile.exists()) {
                        apkFile.delete()
                    }

                    val inputStream = response.body?.byteStream()
                    val outputStream = FileOutputStream(apkFile)

                    val buffer = ByteArray(4096)
                    var bytesRead: Int
                    while (inputStream?.read(buffer).also { bytesRead = it ?: -1 } != -1) {
                        outputStream.write(buffer, 0, bytesRead)
                    }

                    outputStream.close()
                    inputStream?.close()

                    notifyFrontend(callbackName, "ready", "Update downloaded. Installing...")
                    installApk(apkFile)

                } catch (e: Exception) {
                    e.printStackTrace()
                    notifyFrontend(callbackName, "error", "Error saving APK file.")
                }
            }
        })
    }

    private fun installApk(apkFile: File) {
        activity.runOnUiThread {
            try {
                val intent = Intent(Intent.ACTION_VIEW)
                intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION

                val uri = FileProvider.getUriForFile(
                    activity,
                    "${activity.packageName}.fileprovider",
                    apkFile
                )

                intent.setDataAndType(uri, "application/vnd.android.package-archive")
                activity.startActivity(intent)
            } catch (e: Exception) {
                e.printStackTrace()
                Toast.makeText(activity, "Failed to start installation.", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun notifyFrontend(callbackName: String, status: String, message: String) {
        if (activity is MainActivity) {
            val safeMessage = message.replace("'", "\\'")
            val script = "if(window['$callbackName']) { window['$callbackName']('$status', '$safeMessage'); }"
            activity.runOnUiThread {
                activity.webView.evaluateJavascript(script, null)
            }
        }
    }
}
