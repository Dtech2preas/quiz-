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
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

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
