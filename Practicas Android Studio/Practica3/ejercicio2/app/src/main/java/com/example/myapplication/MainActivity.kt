package com.example.myapplication

import android.media.AudioAttributes
import android.media.MediaPlayer
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.TextView

class MainActivity : AppCompatActivity() {

    private var mediaPlayer: MediaPlayer? = null
    private lateinit var btnPrev: Button
    private lateinit var btnPlayPause: Button
    private lateinit var btnNext: Button
    private lateinit var txtTitle: TextView

    // Lista de canciones (archivos en res/raw)
    private val playlist = intArrayOf(R.raw.flashinglights, R.raw.iwonder)
    private val titles = arrayOf("flashinglights.mp3", "iwonder.mp3")
    // Indice de la cancion actual
    private var index = 0
    private var isPrepared = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Referencias a los botones y texto
        txtTitle = findViewById(R.id.txtTitle)
        btnPrev = findViewById(R.id.btnPrev)
        btnPlayPause = findViewById(R.id.btnPlayPause)
        btnNext = findViewById(R.id.btnNext)

        //boton anterior

        btnPrev.setOnClickListener { prev() }

        //boton siguiente
        btnNext.setOnClickListener { next() }

        //boton de play y pause
        btnPlayPause.setOnClickListener {
            val mp = mediaPlayer
            if (mp?.isPlaying == true) {
                //si esta sonando , pausamos
                mp.pause()
                btnPlayPause.text = "Reproducir"
            } else {
                //si esta pausado o no esta listo , reproducimos
                if (isPrepared) {
                    mp?.start()
                    btnPlayPause.text = "Pausar"
                } else {
                    prepareAndPlay(playlist[index])
                }
            }
        }
        //mostramos el nombre de la primera cancion
        txtTitle.text = titles[index]
        //reproducimos la primera cancion al abrir
        prepareAndPlay(playlist[index]) // empieza al abrir
    }

    //prepara y reproduce una cancion
    private fun prepareAndPlay(resId: Int) {
        releasePlayer()
        mediaPlayer = MediaPlayer().apply {
            setAudioAttributes(
                AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build()
            )

            val afd = resources.openRawResourceFd(resId)
            setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
            afd.close()

            setOnPreparedListener {
                isPrepared = true
                setVolume(1.0f, 1.0f)
                start()
                btnPlayPause.text = "Pausar"
            }
            setOnCompletionListener { next() }

            prepareAsync()
        }
    }
    //funcion de cambiar a la siguiente  cancion
    private fun next() {
        index = (index + 1) % playlist.size
        txtTitle.text = titles[index]
        prepareAndPlay(playlist[index])
    }
    //funcion de cambiar a la anterior cancion
    private fun prev() {
        index = if (index - 1 < 0) playlist.size - 1 else index - 1
        txtTitle.text = titles[index]
        prepareAndPlay(playlist[index])
    }
    //liberamos el reproductor para evitar errores
    private fun releasePlayer() {
        isPrepared = false
        mediaPlayer?.release()
        mediaPlayer = null
    }
    //pausa la musica si la app se minimiza
    override fun onPause() {
        super.onPause()
        if (mediaPlayer?.isPlaying == true) {
            mediaPlayer?.pause()
            btnPlayPause.text = "Reproducir"
        }
    }
    //el reproductor se cierra al cerrar la app
    override fun onDestroy() {
        super.onDestroy()
        releasePlayer()
    }
}
