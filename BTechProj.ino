#include <LiquidCrystal.h>
#include <Stepper.h>
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"


#define STEPS 20
Stepper stepper(STEPS, 4, 5, 6, 7);
static char send_payload[256];
const int min_payload_size = 4;
const int max_payload_size = 32;
const int payload_size_increments_by = 1;
int next_payload_size = min_payload_size;
RF24 radio(9, 10);

const uint64_t pipes[2] = { 0xF0F0F0F0E1LL, 0xF0F0F0F0D2LL };
char receive_payload[max_payload_size + 1];

// numbers of lcd interface pins
LiquidCrystal lcd(8,9,10,11,12,13); // RS, E, D4, D5, D6, D7
// RW, VSS, VEE to ground, VDD to supply

char TEMP[6];
char MOIS[7];
char HUMI[6];
char LINT[7];

float arr[4];
int i;

void setup() {
  // lcd rows and columns
  lcd.begin(16,4);
  // set the speed of the motor to 30 RPMs
  stepper.setSpeed(30);
  //Serial.begin(115200);
  radio.begin();
  // enable dynamic payloads
  radio.enableDynamicPayloads();
  radio.setRetries(5, 15);

  radio.openWritingPipe(pipes[0]);
  radio.openReadingPipe(1, pipes[1]);
  radio.startListening();
}

float prev = 0;

void loop() {
  // set points
  const int SPT = 40;
  const int SPM = 800;
  const int SPHl = 30;
  const int SPHh = 60;
  const int SPLI = 50;

  // control outputs
  const int fan = 0;
  const int pump = 1;
  const int fogger = 2;
  const int dehumidifier = 3;

  pinMode(fan, OUTPUT);
  pinMode(pump, OUTPUT);
  pinMode(fogger, OUTPUT);
  pinMode(dehumidifier, OUTPUT);

 while(1){
  // reading inputs
  int V1 = analogRead(A0);
  int V2 = analogRead(A1);
  int V3 = analogRead(A2);
  int V4 = analogRead(A3);
  
  // scaling
  float Vin1 = V1 * 5.0 / 1023.0;
  float Vin2 = V2 * 5.0 / 1023.0;
  float Vin3 = V3 * 5.0 / 1023.0;
  float Vin4 = V4 * 5.0 / 1023.0;
  
  // defining calculation variables
  float T, RHsensor, H, Rsensor, Rldr, alpha, lux;
  int Vsupply = 5;
  
  // temperature calculation
  T = Vin1 / 0.078;

  // moisture calculation
  Rsensor = (1-(Vin2/5)) * 1000;
  
  // humidity calculation
  RHsensor = ((Vin3 / Vsupply) - 0.1515) / 0.00636;
  H = RHsensor / (1.0546 - (0.000216 * T));

  //light intensity calculation
  Rldr = (12500/Vin4) - 2500;
  alpha = (log(Rldr/1000)-4.125) / (-0.6704);
  lux = exp(alpha);

  arr[0] = T;
  arr[1] = Rsensor;
  arr[2] = H;
  arr[3] = lux;

  for(i=0;i<4;i++)
  {
    String temp = String(arr[i]);
    static char send_payload[50];
    temp.toCharArray(send_payload, 50);
    radio.stopListening();
    radio.write( send_payload, next_payload_size );
  }
  
  // print values
  lcd.setCursor(0,0);
  lcd.print("T: ");
  String TEMP1 = String(T);
  TEMP1.toCharArray(TEMP,6);
  lcd.print(TEMP);
  lcd.print(" deg.C");

  lcd.setCursor(0,1);
  lcd.print("M: ");
  String MOIS1 = String(Rsensor);
  MOIS1.toCharArray(MOIS,7);
  lcd.print(MOIS);
  lcd.print(" ohm");

  lcd.setCursor(0,2);
  lcd.print("H: ");
  String HUMI1 = String(H);
  HUMI1.toCharArray(HUMI,6);
  lcd.print(HUMI);
  lcd.print(" %RH");

  lcd.setCursor(0,3);
  lcd.print("L: ");
  String LINT1 = String(lux);
  LINT1.toCharArray(LINT,7);
  lcd.print(LINT);
  lcd.print(" lux");

  

  // comparing set points
 
  // temperature
  if (T > SPT) {
    digitalWrite(fan, HIGH);
  } else {
    digitalWrite(fan, LOW);
  }
  
  //moisture
  if (Rsensor > SPM) {
    digitalWrite(pump, HIGH);
  } else {
    digitalWrite(pump, LOW);
  }

  //humidity
  if (H < SPHl) {
    digitalWrite(fogger, HIGH);
  } else {
    digitalWrite(fogger, LOW);
  }

  if (H > SPHh) {
    digitalWrite(dehumidifier, HIGH);
  } else {
    digitalWrite(dehumidifier, LOW);
  }

  if (prev != lux){
    stepper.step(lux - SPLI);
    prev = lux;
  }
  
  // wait for 5 seconds to take next reading
  delay(1000);
 }
}
