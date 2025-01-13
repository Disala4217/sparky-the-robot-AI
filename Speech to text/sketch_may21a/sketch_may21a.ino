#include <WiFi.h>
#include <HTTPClient.h>
#include <Base64.h>

// Replace with your network credentials
const char* ssid = "dmk";
const char* password = "disala12";

// Analog pin where the MAX4466 output is connected
const int analogPin = 34;

// Replace with your Google Cloud Speech-to-Text API endpoint and key
const char* serverName = "https://speech.googleapis.com/v1/speech:recognize?key=YOUR_API_KEY";

// Flag to ensure speech2txt is called only once
bool calledSpeech2txt = false;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void speech2txt() {
  int16_t audioData[16000];  // Buffer to store audio samples

  // Capture audio data
  for (int i = 0; i < 16000; i++) {
    audioData[i] = analogRead(analogPin);
    delayMicroseconds(62); // Approx 16kHz sampling rate
  }

  // Convert the audio data to base64 using the Base64 library
  String base64Audio = base64::encode((uint8_t*)audioData, sizeof(audioData));

  // Create the JSON request payload
  String jsonRequest = "{"
                       "\"config\": {"
                       "\"encoding\":\"LINEAR16\","
                       "\"sampleRateHertz\":16000,"
                       "\"languageCode\":\"en-US\""
                       "},"
                       "\"audio\": {"
                       "\"content\":\"" + base64Audio + "\""
                       "}"
                       "}";

  // Send audio data to Google Cloud Speech-to-Text API
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Send the audio data
    int httpResponseCode = http.POST(jsonRequest);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }

  delay(5000);
}

void loop() {
  if (!calledSpeech2txt) {
    speech2txt();
    calledSpeech2txt = true;
  }
}
