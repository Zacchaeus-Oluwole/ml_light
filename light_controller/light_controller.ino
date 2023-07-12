int pwm = 11;
int value = 0;
void setup() {
  pinMode(pwm, OUTPUT);
  Serial.begin(9600);
  Serial.setTimeout(1);
  // put your setup code here, to run once:
}

void loop() {
  if (Serial.available()){
    String ll = "1.3";
    String oc = "1";
    int command = read_write(ll,oc);
      switch(command){
          case 0 : Serial.println(command); power_level(0);      // maximum brightness (0%)
          case 1 : Serial.println(command); power_level(1);      // maximum brightness (20%)
          case 2 : Serial.println(command); power_level(2);      // maximum brightness (40%)
          case 3 : Serial.println(command); power_level(3);      // maximum brightness (60%)
          case 4 : Serial.println(command); power_level(4);      // maximum brightness (80%)
          case 5 : Serial.println(command); power_level(5);      // maximum brightness (100%)
          default: break;
        }
    }
}

int read_write(String light_level, String occupancy) {
  
  String data;
  data = light_level + " " + occupancy;
  Serial.write(data.c_str());
  
  delay(15);
  int command = Serial.readStringUntil('\n').toInt();
  return command;
}

void power_level(int level){
    value = (level)*255/5;
    analogWrite(pwm, value);
}
