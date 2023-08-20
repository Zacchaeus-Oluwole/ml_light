#define LDR A6
#define PIR 2
#define Light 3

int led_value = 0;

void setup() {
  pinMode(PIR, INPUT);
  pinMode(Light, OUTPUT);
  Serial.begin(115200);// NOTE THIS BAUD RATE
  Serial.setTimeout(2);// DO NOT TOUCH
}

void loop() {
  int value_ldr = analogRead(A6); // read LDR value
  int value_pir = digitalRead(PIR); // read input value
  
  String ll = String(mapLDR(value_ldr)); // Map LDR value
  
  if (value_pir == HIGH) {
    read_write(ll, "1");
  } else {
    read_write(ll, "0");
  }
}

void read_write(String light_level, String occupancy) {
  String data = light_level + "," + occupancy;
//  Serial.println(data);
  Serial.write(data.c_str());
  Serial.println();
//  Serial.write(data.c_str());

  
  int command = Serial.parseInt();
  
  switch (command) {
    case 0: power_level(0); break;
    case 1: power_level(1); break;
    case 2: power_level(2); break;
    case 3: power_level(3); break;
    case 4: power_level(4); break;
    case 5: power_level(5); break;
    default: break;
  }
}

void power_level(int level) {
  led_value = level * 255 / 5;
  analogWrite(Light, led_value);
  delay(5000);
}

float mapLDR(int value) {
  const int fromLow = 0;
  const int fromHigh = 1023; // Change this to match the ADC resolution
  
  const float toLow = 0.0;
  const float toHigh = 1.0;
  
  int mappedValue = map(value, fromLow, fromHigh, toLow * 100, toHigh * 100);
  float floatMappedValue = (float)mappedValue / 100.0;
  float roundedValue = round(floatMappedValue * 10.0) / 10.0;
  
  return roundedValue;
}


//#define LDR A6
//#define PIR 2
//#define Light 3
//
//int led_value = 0;
//void setup() {
//  pinMode(PIR, INPUT);
//  pinMode(Light, OUTPUT);
//  Serial.begin(9600);
//  Serial.setTimeout(1);
//  // put your setup code here, to run once:
//}
//
//void loop() {
//    int value_ldr = analogRead(A6); // read LDR value
//    int value_pir = digitalRead(PIR); // read input value
//    
//    if(value_pir == HIGH){
//        String ll = String(mapLDR(round(value_ldr)));
////        Serial.println(ll);
//        String oc = "1";
//        read_write(ll,oc);
//      }else{
//        String ll = String(mapLDR(round(value_ldr)));
////        Serial.println(ll);
//        String oc = "0";
//        read_write(ll,oc);
//      }
////   }
//}
//
//void read_write(String light_level, String occupancy) {
//  
//  String data;
//  data = light_level + "," + occupancy;
//  Serial.write(data.c_str());
//  Serial.flush();
////  delay(15);//
//  int command = Serial.readStringUntil('\n').toInt();
//  Serial.flush();
//  
//  switch(command){
//    case 0 : Serial.println(command); power_level(0);      // maximum brightness (0%)
//    case 1 : Serial.println(command); power_level(1);      // maximum brightness (20%)
//    case 2 : Serial.println(command); power_level(2);      // maximum brightness (40%)
//    case 3 : Serial.println(command); power_level(3);      // maximum brightness (60%)
//    case 4 : Serial.println(command); power_level(4);      // maximum brightness (80%)
//    case 5 : Serial.println(command); power_level(5);      // maximum brightness (100%)
//    default: break;
//  }
//  return 0;
//}
//
//void power_level(int level){
//    led_value = (level)*255/5;
//    analogWrite(Light, led_value);
//}
//
//float mapLDR(int value) {
//  // The fromLow and fromHigh parameters define the range of the input value.
//  const int fromLow = 0;
//  const int fromHigh = 1000;
//
//  // The toLow and toHigh parameters define the range of the output value.
//  const float toLow = 0.0;
//  const float toHigh = 1.0;
//
//  // The map() function returns an integer.
//  int mappedValue = map(value, fromLow, fromHigh, toLow * 100, toHigh * 100); // Multiply by 100 to work with integers
//
//  // Cast the result to a float and divide by 100 to restore the decimal place.
//  float floatMappedValue = (float)mappedValue / 100.0;
//  float roundedValue = round(floatMappedValue * 10.0) / 10.0; // Round to 1 decimal place
//
//  return roundedValue;
//}
