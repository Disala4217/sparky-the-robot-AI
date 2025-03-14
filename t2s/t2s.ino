#include "Arduino.h"
#include "WiFi.h"
#include "Audio.h"

#define I2S_DOUT      25
#define I2S_BCLK      27
#define I2S_LRC       26

Audio audio;

void setup() {
  Serial.begin(115200);
  
  WiFi.disconnect();
  WiFi.mode(WIFI_STA);
  WiFi.begin("dmk", "disala12");

  while (WiFi.status() != WL_CONNECTED)
    delay(1500);

  audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
  audio.setVolume(100);

  Serial.println("Attempting to play speech...");
  audio.connecttospeech("Hello From Sachin Soni", "en");
  Serial.println("Done playing speech.");
}

void loop() {
  audio.loop();
}

void audio_info(const char *info) {
  Serial.print("Audio info: ");
  Serial.println(info);
}
