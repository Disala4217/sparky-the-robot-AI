#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_DC     8
#define OLED_CS     10
#define OLED_RESET  9
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &SPI, OLED_DC, OLED_RESET, OLED_CS);

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Initialize the display
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_CS, OLED_DC, OLED_RESET)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Clear the buffer
  display.clearDisplay();
  display.display();
}

void loop() {
  int x=1;
  //lowBatt();
  //delay(5000); // Display the low battery icon for 5 seconds
  eye_open(x);
  delay(2000); // Keep the eye open for 2 seconds
  eye_close(x);
  delay(2000); // Keep the eye closed for 2 seconds
}

void eye_open(int x) {
  // Animate from the second state back to the initial state
  for (int i = 60; i >= 0; i--) {
    // Clear the display
    display.clearDisplay();

    // Draw the first fixed rectangle
    display.fillRect(1, 1, 125, 61, 0xFFFF);

    // Interpolate values for the second rectangle
    int x2 = 67 + (60 - i); // Starts at 67, ends at 127
    int width2 = 61 - (60 - i); // Starts at 61, ends at 1

    display.fillRect(x2, -1, width2, 65, 0x0);

    // Interpolate values for the third rectangle
    int width3 = 56 - (60 - i); // Starts at 56, ends at 0

    display.fillRect(0, 0, width3, 64, 0x0);

    // Update the display
    display.display();

    // Small delay to control animation speed
    delay(x); // Adjust the delay as needed
  }
}

void eye_close(int x) {
  // Animate from the initial state to the second state
  for (int i = 0; i <= 60; i++) {
    // Clear the display
    display.clearDisplay();

    // Draw the first fixed rectangle
    display.fillRect(1, 1, 125, 61, 0xFFFF);

    // Interpolate values for the second rectangle
    int x2 = 127 - i; // Starts at 127, ends at 67
    int width2 = 1 + i; // Starts at 1, ends at 61

    display.fillRect(x2, -1, width2, 65, 0x0);

    // Interpolate values for the third rectangle
    int width3 = i; // Starts at 0, ends at 56

    display.fillRect(0, 0, width3, 64, 0x0);

    // Update the display
    display.display();

    // Small delay to control animation speed
    delay(x); // Adjust the delay as needed
  }
}

void lowBatt() {
  display.clearDisplay();  // Clear the internal memory

  // Draw the battery outline
  display.drawRect(34, 20, 60, 30, SSD1306_WHITE); // Main battery rectangle
  display.fillRect(94, 28, 4, 14, SSD1306_WHITE); // Battery tip

  // Draw the low battery level inside the outline
  display.fillRect(36, 22, 20, 26, SSD1306_WHITE); // Low battery level

  // Draw the 'LOW' text
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(58, 28);
  display.print("LOW");

  display.display();  // Transfer internal memory to the display
}
