package com.example.myapplication

import android.os.Bundle
import android.widget.ImageView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val miImagen: ImageView = findViewById(R.id.miImagen)
        miImagen.setOnClickListener {
            Toast.makeText(this, "¡Hiciste clic en Cheto!", Toast.LENGTH_SHORT).show()
        }
    }
}
