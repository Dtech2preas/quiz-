package com.dtech.quizzes

import android.annotation.SuppressLint
import android.content.ContentValues
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.os.Message
import android.provider.MediaStore
import android.util.Base64
import android.view.ViewGroup
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream

class MainActivity : AppCompatActivity() {

    lateinit var webView: WebView
    lateinit var downloadBanner: LinearLayout
    lateinit var downloadText: TextView
    lateinit var downloadProgressBar: ProgressBar

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_main)

        val webViewContainer = findViewById<FrameLayout>(R.id.webViewContainer)
        webView = WebView(this)
        webViewContainer.addView(webView)

        downloadBanner = findViewById(R.id.downloadBanner)
        downloadText = findViewById(R.id.downloadText)
        downloadProgressBar = findViewById(R.id.downloadProgressBar)

        val webSettings: WebSettings = webView.settings
        webSettings.javaScriptEnabled = true
        webSettings.domStorageEnabled = true
        webSettings.allowFileAccess = true
        webSettings.allowContentAccess = true
        webSettings.databaseEnabled = true
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        webSettings.setSupportMultipleWindows(true)
        webSettings.javaScriptCanOpenWindowsAutomatically = true


        // Add Javascript interface for base64 downloads
        webView.addJavascriptInterface(AndroidDownloader(this), "AndroidDownloader")
        // Add Javascript interface for dataset caching
        webView.addJavascriptInterface(AndroidCacher(this, this), "AndroidCacher")


        webView.webViewClient = object : WebViewClient() {
            private fun handleUrlLoading(url: String): Boolean {
                // Let all http/https URLs load inside the main WebView.
                if (url.startsWith("http://") || url.startsWith("https://")) {
                    return false
                } else {
                    // For other links (like shein://, intent://, mailto:, tel:, market://, etc.), try to launch an Intent
                    try {
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                        startActivity(intent)
                        return true
                    } catch (e: Exception) {
                        e.printStackTrace()
                        // Fallback or ignore if no app can handle the intent
                        return true
                    }
                }
            }

            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                val url = request?.url.toString()
                return handleUrlLoading(url)
            }

            @Deprecated("Deprecated in Java")
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                if (url != null) {
                    return handleUrlLoading(url)
                }
                return false
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                // Inject a flag into the window object to notify the web app it's running in Android
                view?.evaluateJavascript("window.IS_ANDROID_APP = true; if(window.onAndroidAppDetected) { window.onAndroidAppDetected(); }", null)
            }

            override fun shouldInterceptRequest(
                view: WebView?,
                request: WebResourceRequest?
            ): android.webkit.WebResourceResponse? {
                val urlString = request?.url?.toString() ?: return null

                // Check if device is offline
                val cm = getSystemService(Context.CONNECTIVITY_SERVICE) as android.net.ConnectivityManager
                val networkInfo = cm.activeNetworkInfo
                val isOffline = networkInfo == null || !networkInfo.isConnected

                // Only intercept our domain and only if offline
                if (isOffline && urlString.startsWith("https://quiz.dtech-services.co.za")) {
                    try {
                        val path = request.url.path ?: "/"
                        val cleanPath = if (path == "" || path == "/") "/index.html" else path

                        // Check if file exists in internal storage
                        val localFile = java.io.File(filesDir, cleanPath)
                        if (localFile.exists()) {
                            // Determine mime type
                            val mimeType = when {
                                cleanPath.endsWith(".html") -> "text/html"
                                cleanPath.endsWith(".js") -> "application/javascript"
                                cleanPath.endsWith(".css") -> "text/css"
                                cleanPath.endsWith(".json") -> "application/json"
                                cleanPath.endsWith(".png") -> "image/png"
                                cleanPath.endsWith(".jpg") || cleanPath.endsWith(".jpeg") -> "image/jpeg"
                                cleanPath.endsWith(".ico") -> "image/x-icon"
                                else -> "text/plain"
                            }

                            val inputStream = java.io.FileInputStream(localFile)
                            return android.webkit.WebResourceResponse(mimeType, "UTF-8", inputStream)
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }

                return super.shouldInterceptRequest(view, request)
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            @SuppressLint("SetJavaScriptEnabled")
            override fun onCreateWindow(
                view: WebView?,
                isDialog: Boolean,
                isUserGesture: Boolean,
                resultMsg: Message?
            ): Boolean {
                if (view == null || resultMsg == null) return false

                val newWebView = WebView(this@MainActivity)
                val newSettings = newWebView.settings
                newSettings.javaScriptEnabled = true
                newSettings.domStorageEnabled = true
                newSettings.setSupportMultipleWindows(true)
                newSettings.javaScriptCanOpenWindowsAutomatically = true

                newWebView.webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(
                        v: WebView?,
                        request: WebResourceRequest?
                    ): Boolean {
                        val url = request?.url.toString()
                        if (url.startsWith("http://") || url.startsWith("https://")) {
                            return false // Load in this new WebView
                        } else {
                            try {
                                val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                startActivity(intent)
                                return true
                            } catch (e: Exception) {
                                e.printStackTrace()
                                return true
                            }
                        }
                    }

                    @Deprecated("Deprecated in Java")
                    override fun shouldOverrideUrlLoading(v: WebView?, url: String?): Boolean {
                        if (url != null) {
                            if (url.startsWith("http://") || url.startsWith("https://")) {
                                return false
                            } else {
                                try {
                                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                    startActivity(intent)
                                    return true
                                } catch (e: Exception) {
                                    e.printStackTrace()
                                    return true
                                }
                            }
                        }
                        return false
                    }
                }

                newWebView.webChromeClient = object : WebChromeClient() {
                    override fun onCloseWindow(window: WebView?) {
                        super.onCloseWindow(window)
                        if (window != null) {
                            (window.parent as? ViewGroup)?.removeView(window)
                            window.destroy()
                        }
                    }
                }

                newWebView.layoutParams = FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
                )

                // Add to the main view hierarchy over the current WebView
                (webView.parent as? ViewGroup)?.addView(newWebView)

                val transport = resultMsg.obj as WebView.WebViewTransport
                transport.webView = newWebView
                resultMsg.sendToTarget()

                return true
            }
        }

        // Handle normal downloads (if any)
        webView.setDownloadListener { url, userAgent, contentDisposition, mimetype, contentLength ->
            try {
                val intent = Intent(Intent.ACTION_VIEW)
                intent.data = Uri.parse(url)
                startActivity(intent)
            } catch (e: Exception) {
                Toast.makeText(this@MainActivity, "Cannot download this file", Toast.LENGTH_SHORT).show()
            }
        }

        webView.loadUrl("https://quiz.dtech-services.co.za")
    }

    override fun onBackPressed() {
        // If there's a secondary WebView added on top, we should handle going back in it or closing it
        val parent = webView.parent as? ViewGroup
        if (parent != null && parent.childCount > 1) {
            val topView = parent.getChildAt(parent.childCount - 1)
            if (topView is WebView && topView != webView) {
                if (topView.canGoBack()) {
                    topView.goBack()
                } else {
                    parent.removeView(topView)
                    topView.destroy()
                }
                return
            }
        }

        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}

class AndroidDownloader(private val context: Context) {
    @JavascriptInterface
    fun saveBase64Image(base64Data: String, filename: String) {
        val uiHandler = android.os.Handler(android.os.Looper.getMainLooper())
        try {
            val base64Image = base64Data.split(",")[1]
            val decodedBytes = Base64.decode(base64Image, Base64.DEFAULT)

            val outputStream: OutputStream?
            val resolver = context.contentResolver

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                val contentValues = ContentValues().apply {
                    put(MediaStore.MediaColumns.DISPLAY_NAME, "$filename.png")
                    put(MediaStore.MediaColumns.MIME_TYPE, "image/png")
                    put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_PICTURES + "/DTechQuizzes")
                }
                val imageUri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
                outputStream = imageUri?.let { resolver.openOutputStream(it) }
            } else {
                // Check if we have permission first, if not we will just notify the user.
                if (androidx.core.content.ContextCompat.checkSelfPermission(
                        context,
                        android.Manifest.permission.WRITE_EXTERNAL_STORAGE
                    ) != android.content.pm.PackageManager.PERMISSION_GRANTED
                ) {
                    uiHandler.post {
                        Toast.makeText(context, "Storage permission is required to download certificates.", Toast.LENGTH_LONG).show()
                    }
                    if (context is MainActivity) {
                        context.requestPermissions(arrayOf(android.Manifest.permission.WRITE_EXTERNAL_STORAGE), 100)
                    }
                    return
                }

                val imagesDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES)
                val appDir = File(imagesDir, "DTechQuizzes")
                if (!appDir.exists()) {
                    appDir.mkdirs()
                }
                val imageFile = File(appDir, "$filename.png")
                outputStream = FileOutputStream(imageFile)
            }

            outputStream?.use {
                it.write(decodedBytes)
                uiHandler.post {
                    Toast.makeText(context, "Certificate saved to Pictures/DTechQuizzes", Toast.LENGTH_LONG).show()
                }
            } ?: run {
                uiHandler.post {
                    Toast.makeText(context, "Failed to create file for certificate", Toast.LENGTH_SHORT).show()
                }
            }

        } catch (e: Exception) {
            e.printStackTrace()
            uiHandler.post {
                Toast.makeText(context, "Failed to save certificate", Toast.LENGTH_SHORT).show()
            }
        }
    }
}


class AndroidCacher(private val context: Context, private val activity: MainActivity) {
    @JavascriptInterface
    fun cacheGradeDatasets(grade: String) {
        val uiHandler = android.os.Handler(android.os.Looper.getMainLooper())

        // Show banner immediately
        uiHandler.post {
            activity.downloadBanner.visibility = android.view.View.VISIBLE
            activity.downloadText.text = "Starting offline cache for $grade..."
            activity.downloadProgressBar.progress = 0
        }

        Thread {
            try {
                // Core files to download
                val coreFiles = listOf(
                    "/", "/index.html", "/login.html", "/signup.html", "/dashboard.html",
                    "/quiz.html", "/weekly_quiz.html", "/test.html", "/test_run_grades.html",
                    "/test_run_subjects.html", "/test_run_quiz.html", "/leaderboard.html",
                    "/global_leaderboard.html", "/profile.html", "/public_profile.html",
                    "/store.html", "/earn_points.html", "/stats.html", "/admin.html",
                    "/map.json", "/dtech_cosmetics.js", "/offline_mode.js"
                )

                val baseUrl = "https://quiz.dtech-services.co.za"
                val allFilesToDownload = mutableListOf<String>()
                allFilesToDownload.addAll(coreFiles)

                // First download map.json to parse it
                val mapJsonFile = downloadFile(baseUrl, "/map.json")
                if (mapJsonFile != null && mapJsonFile.exists()) {
                    val mapJsonStr = mapJsonFile.readText()
                    try {
                        val jsonObject = org.json.JSONObject(mapJsonStr)
                        if (jsonObject.has(grade)) {
                            val gradeObj = jsonObject.getJSONObject(grade)
                            val subjects = gradeObj.keys()
                            while (subjects.hasNext()) {
                                val subject = subjects.next()
                                val filesArray = gradeObj.getJSONArray(subject)
                                for (i in 0 until filesArray.length()) {
                                    val fileObj = filesArray.getJSONObject(i)
                                    val fileName = fileObj.getString("file")
                                    allFilesToDownload.add("/dataset/$grade/$subject/$fileName")
                                }
                            }
                        }
                    } catch (e: Exception) {
                        e.printStackTrace()
                    }
                }

                // Download everything sequentially
                val total = allFilesToDownload.size
                var count = 0
                var hasFailures = false
                for (path in allFilesToDownload) {
                    val downloadedFile = downloadFile(baseUrl, path)
                    if (downloadedFile == null) {
                        hasFailures = true
                        break // Stop downloading if one fails
                    }
                    count++
                    val percentage = ((count.toFloat() / total) * 100).toInt()
                    uiHandler.post {
                        activity.downloadText.text = "Downloading offline datasets... $percentage% ($count/$total)"
                        activity.downloadProgressBar.progress = percentage
                    }
                }

                if (!hasFailures) {
                    // Finished successfully
                    uiHandler.post {
                        activity.downloadText.text = "Download complete!"
                        activity.downloadProgressBar.progress = 100

                        // Tell JS it was successful so it won't trigger again
                        activity.webView.evaluateJavascript("localStorage.setItem('dtech_datasets_cached_$grade', 'true');", null)

                        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                            activity.downloadBanner.visibility = android.view.View.GONE
                        }, 2000)
                    }
                } else {
                    uiHandler.post {
                        activity.downloadText.text = "Download failed."
                        android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                            activity.downloadBanner.visibility = android.view.View.GONE
                        }, 3000)
                    }
                }

            } catch (e: Exception) {
                e.printStackTrace()
                uiHandler.post {
                    activity.downloadText.text = "Download failed."
                    android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                        activity.downloadBanner.visibility = android.view.View.GONE
                    }, 3000)
                }
            }
        }.start()
    }

    private fun downloadFile(baseUrl: String, path: String): File? {
        val cleanPath = if (path == "/") "/index.html" else path
        val targetFile = File(context.filesDir, cleanPath)

        // Ensure directory exists
        targetFile.parentFile?.mkdirs()

        try {
            val url = java.net.URL(baseUrl + path)
            val connection = url.openConnection() as java.net.HttpURLConnection
            connection.requestMethod = "GET"
            connection.connectTimeout = 10000
            connection.readTimeout = 10000

            if (connection.responseCode == java.net.HttpURLConnection.HTTP_OK) {
                val inputStream = connection.inputStream
                val outputStream = FileOutputStream(targetFile)
                val buffer = ByteArray(4096)
                var bytesRead: Int
                while (inputStream.read(buffer).also { bytesRead = it } != -1) {
                    outputStream.write(buffer, 0, bytesRead)
                }
                outputStream.close()
                inputStream.close()
                return targetFile
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return null
    }
}
