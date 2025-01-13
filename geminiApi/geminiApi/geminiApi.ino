#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "Audio.h"

#define I2S_DOUT      25
#define I2S_BCLK      27
#define I2S_LRC       26

Audio audio;

//Gemini API endpoint and key
const char* apiKey = "AIzaSyBOXYHnVv6_Bkp619iaRt_slyo4iSXz6_o";
String endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=";

const char* ssid = "dmk";
const char* password = "disala12";

void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

String Speech2Text() {
  Serial.println("\"");
  Serial.print("Getting input from the mic");
  Serial.println("\"");
  return "who is mahinda rajapaksha";  // Placeholder for actual speech recognition function
}

String queryGemini(String userQuery) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi connection error");
    return "";
  }

  HTTPClient http;
  http.setTimeout(15000);
  http.begin(endpoint + apiKey);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"contents\":[{\"parts\":[{\"text\":\"" + userQuery + "\"}]}]}";
  int httpResponseCode = http.POST(payload);

  if (httpResponseCode > 0) {
    String response = http.getString();
    DynamicJsonDocument doc(4096);
    DeserializationError error = deserializeJson(doc, response);

    if (!error) {
      const char* text = doc["candidates"][0]["content"]["parts"][0]["text"];
      return String(text);
    } else {
      Serial.print("Error parsing JSON: ");
      Serial.println(error.c_str());
    }
  } else {
    Serial.print("Request error: ");
    Serial.println(httpResponseCode);
    Serial.print("HTTP error: ");
    Serial.println(http.errorToString(httpResponseCode).c_str());
  }

  http.end();
  return "";
}

void say(const char* text) {
  // Placeholder for actual text-to-speech function
  Serial.println("Attempting to play speech...");
  Serial.print("Saying: ");
  Serial.println(text);
  audio.connecttospeech(text, "en");
  Serial.println("Done playing speech.");
}

void task1(String x) {
  for (int i = 0; i < 1; i++) {

    String userQuery = x;
    if (userQuery.length() == 0) {
      continue;
    }

    if (userQuery == "task1") {
      Serial.println("do task 1");
    } else if (userQuery == "task2") {
      Serial.println("do task 2");
    } else if (userQuery == "task3") {
      Serial.println("do task 3");
    } else {
      String geminiResponse = queryGemini(userQuery);
      if (geminiResponse.length() > 0) {
        //Serial.print("You: \"");
        //Serial.print(userQuery);
        //Serial.print("\"");
        //Serial.print("Gemini: \"");
        //Serial.print(geminiResponse);
        //Serial.println("\"");
        say(geminiResponse.c_str());  // Say the response using the Audio library
      } else {
        Serial.println("Failed to retrieve response from Gemini.");
        say("Failed to retrieve response from Gemini.");
      }
    }
    Serial.println("*************************************************************************************");

    // vTaskDelay(1000 / portTICK_PERIOD_MS);  // Delay to prevent spamming
  }
}

void setup() {
  Serial.begin(115200);
  connectToWiFi();
  audio.setPinout(I2S_BCLK, I2S_LRC, I2S_DOUT);
  audio.setVolume(100);
  

    // Pass the input to the task1 function
}

void loop() {
  Serial.println("Enter a question:");

  String x = "";  // Variable to store the serial input

  while (true) {
    if (Serial.available() > 0) {
      // Read the input string from serial
      x = Serial.readString();

      // Print the received string
      Serial.print("question is: ");
      Serial.println(x);
      task1(x);
      break;  // Break out of the loop once we have the input
    }
    
    delay(1000);  // Small delay to prevent overwhelming the serial buffer
  }
  
}
