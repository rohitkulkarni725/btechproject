#include <LiquidCrystal.h>

// numbers of lcd interface pins
LiquidCrystal lcd(8,9,10,11,12,13); // RS, E, D4, D5, D6, D7
// RW, VSS, VEE to ground, VDD to supply

char TEMP[6];
char HUMI[6];
char MOIS[7];

void setup() {
  // lcd rows and columns
  lcd.begin(16,4);
}

void loop() {
  // reading inputs
  int V1 = analogRead(A0);
  int V2 = analogRead(A1);
  int V3 = analogRead(A2);
  
  // scaling
  float Vin1 = V1 * 5.0 / 1023.0;
  float Vin2 = V2 * 5.0 / 1023.0;
  float Vin3 = V3 * 5.0 / 1023.0;
  
  // defining calculation variables
  float T, RHsensor, H, Rsensor;
  int Vsupply = 5;
  
  // temperature calculation
  T = Vin1 / 0.075;
  
  // humidity calculation
  RHsensor = ((Vin3 / Vsupply) - 0.1515) / 0.00636;
  H = RHsensor / (1.0546 - (0.000216 * T));
  
  // moisture calculation
  Rsensor = (Vin2 - 1) * 100000;
  
  // print values
  lcd.setCursor(0,1);
  lcd.print("T: ");
  String TEMP1 = String(T);
  TEMP1.toCharArray(TEMP,6);
  lcd.print(TEMP);
  lcd.print(" deg.C");

  lcd.setCursor(0,2);
  lcd.print("H: ");
  String HUMI1 = String(H);
  HUMI1.toCharArray(HUMI,6);
  lcd.print(HUMI);
  lcd.print(" %RH");

  lcd.setCursor(0,3);
  lcd.print("M: ");
  String MOIS1 = String(Rsensor);
  MOIS1.toCharArray(MOIS,7);
  lcd.print(MOIS);
  lcd.print(" ohm");
  
  // wait for 5 seconds to take next reading
  delay(5000);
}
