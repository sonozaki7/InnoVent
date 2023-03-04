#include <ArduinoSpeech.h>
#include <LiquidCrystal.h>

// LCD pins
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Microphone pin
const int micPin = A0;

void setup() {
  // Serial Monitor baud rate
  Serial.begin(9600);
 
  //____________________
  
  // Initialize LCD module
  lcd.begin(16, 2);

  // Initialize speech recognition
  Speech.begin(micPin);

  // Clear the LCD display
  lcd.clear();

  // Display "Speak now..." message
  lcd.print("Speak now...");
}

void loop() {
  // Listen for speech and get transcribed phrase
  String phrase = Speech.listen();

  // Print the transcribed phrase to the serial monitor
  Serial.println(phrase);
  //____________________
  
  
  // Clear the LCD display
  lcd.clear();

  // Display the transcribed phrase on the LCD
  lcd.print("You said:");
  lcd.setCursor(0, 1);
  lcd.print(phrase);

  // Delay for a short period to allow the user to read the display
  delay(2000);
}


