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
import android.provider.MediaStore
import android.util.Base64
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
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

        // Add Javascript interface for base64 downloads
        webView.addJavascriptInterface(AndroidDownloader(this), "AndroidDownloader")

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                val url = request?.url.toString()
                if (url.startsWith("http://") || url.startsWith("https://")) {
                    return false // Let WebView handle normal links
                }

                // For other links (like shein://, intent://, market://, etc.), try to launch an Intent
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

            @Deprecated("Deprecated in Java")
            override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                if (url != null) {
                    if (url.startsWith("http://") || url.startsWith("https://")) {
                        return false
                    }
                    try {
                        val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                        startActivity(intent)
                        return true
                    } catch (e: Exception) {
                        e.printStackTrace()
                        return true
                    }
                }
                return false
            }
        }

        webView.webChromeClient = WebChromeClient()

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

    @JavascriptInterface
    fun openLink(url: String) {
        val uiHandler = android.os.Handler(android.os.Looper.getMainLooper())
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            context.startActivity(intent)
        } catch (e: Exception) {
            e.printStackTrace()
            uiHandler.post {
                Toast.makeText(context, "Failed to open link", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
