const int FR_hip =  12;
const int FR_shoulder = 11;
const int FR_wrist = 10;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String commandString = "";
String i = "";

void setup()   {             
  Serial.begin(115200);   
  Serial.println("connection established");
  pinMode(FR_hip, OUTPUT);
  pinMode(FR_shoulder, OUTPUT);
  pinMode(FR_wrist, OUTPUT);
  analogWriteFrequency(FR_hip, 400);
  analogWriteFrequency(FR_shoulder, 400);
  analogWriteFrequency(FR_wrist, 400);
  analogWrite(FR_hip, 0);
  analogWrite(FR_shoulder, 0);
  analogWrite(FR_wrist, 0);
}

void loop()                     
{
  if (stringComplete) {
    stringComplete = false;
    getCommand();
    i = getStep();
    
    if(commandString.equals("FRHM")){
      analogWrite(FR_hip, i.toInt());
    }
    if(commandString.equals("FRSM")){
      analogWrite(FR_shoulder, i.toInt());
    }
    if(commandString.equals("FRWM")){
      analogWrite(FR_wrist, i.toInt());
    }
  }
  inputString = "";
}


String getStep()
{
  String value = inputString.substring(5, inputString.length() - 1);
  return value;
}

void getCommand()
{
  if (inputString.length() > 0)
  {
    commandString = inputString.substring(1, 5);
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
