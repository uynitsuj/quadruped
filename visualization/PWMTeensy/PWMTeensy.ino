const int BR_hip = 2;
const int BR_shoulder = 3;
const int BR_wrist = 4;

const int BL_hip = 5;
const int BL_shoulder = 6;
const int BL_wrist = 7;

const int FR_hip = 8;
const int FR_shoulder = 9;
const int FR_wrist = 10;

const int FL_hip =  11;
const int FL_shoulder = 12;
const int FL_wrist = 13;

String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
String commandString = "";
String i = "";

void setup()   {             
  Serial.begin(115200);   
  Serial.println("connection established");
  
  pinMode(BR_hip, OUTPUT);
  pinMode(BR_shoulder, OUTPUT);
  pinMode(BR_wrist, OUTPUT);
  analogWriteFrequency(BR_hip, 400);
  analogWriteFrequency(BR_shoulder, 400);
  analogWriteFrequency(BR_wrist, 400);
  analogWrite(BR_hip, 85);
  analogWrite(BR_shoulder, 50);
  analogWrite(BR_wrist, 40);
  
  pinMode(BL_hip, OUTPUT);
  pinMode(BL_shoulder, OUTPUT);
  pinMode(BL_wrist, OUTPUT);
  analogWriteFrequency(BL_hip, 400);
  analogWriteFrequency(BL_shoulder, 400);
  analogWriteFrequency(BL_wrist, 400);
  analogWrite(BL_hip, 175);
  analogWrite(BL_shoulder, 215);
  analogWrite(BL_wrist, 210);
  
  pinMode(FL_hip, OUTPUT);
  pinMode(FL_shoulder, OUTPUT);
  pinMode(FL_wrist, OUTPUT);
  analogWriteFrequency(FL_hip, 400);
  analogWriteFrequency(FL_shoulder, 400);
  analogWriteFrequency(FL_wrist, 400);
  analogWrite(FL_hip, 175);
  analogWrite(FL_shoulder, 215);
  analogWrite(FL_wrist, 210);
  
  pinMode(FR_hip, OUTPUT);
  pinMode(FR_shoulder, OUTPUT);
  pinMode(FR_wrist, OUTPUT);
  analogWriteFrequency(FR_hip, 400);
  analogWriteFrequency(FR_shoulder, 400);
  analogWriteFrequency(FR_wrist, 400);
  analogWrite(FR_hip, 85);
  analogWrite(FR_shoulder, 50);
  analogWrite(FR_wrist, 50);
}

void loop()                     
{
  if (stringComplete) {
    stringComplete = false;
    getCommand();
    i = getStep();
    if(commandString.equals("BRHM")){
      analogWrite(BR_hip, i.toInt());
    }
    if(commandString.equals("BRSM")){
      analogWrite(BR_shoulder, i.toInt());
    }
    if(commandString.equals("BRWM")){
      analogWrite(BR_wrist, i.toInt());
    }
    
    if(commandString.equals("BLHM")){
      analogWrite(BL_hip, i.toInt());
    }
    if(commandString.equals("BLSM")){
      analogWrite(BL_shoulder, i.toInt());
    }
    if(commandString.equals("BLWM")){
      analogWrite(BL_wrist, i.toInt());
    }
    
    if(commandString.equals("FLHM")){
      analogWrite(FL_hip, i.toInt());
    }
    if(commandString.equals("FLSM")){
      analogWrite(FL_shoulder, i.toInt());
    }
    if(commandString.equals("FLWM")){
      analogWrite(FL_wrist, i.toInt());
    }
    
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
