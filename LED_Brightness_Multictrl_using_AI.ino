int ledPins[] = {9, 10, 11};
int brightness[3] = {0, 0, 0};

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int sep = input.indexOf(':');
    if (sep != -1) {
      int pin = input.substring(0, sep).toInt();
      int val = input.substring(sep + 1).toInt();
      analogWrite(pin, val);
    }
  }
}