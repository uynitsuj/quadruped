/* RGB Analog Example, Teensyduino Tutorial #2
   http://www.pjrc.com/teensy/tutorial2.html

   This example code is in the public domain.
*/

const int redPin =  12;

void setup()   {                
  pinMode(redPin, OUTPUT);
  analogWriteFrequency(redPin, 400);
}

void loop()                     
{
  // fade in from min to max in increments of 5 points:
  for (int fadeValue = 51 ; fadeValue <= 220; fadeValue += 1) {
    // sets the value (range from 0 to 255):
    analogWrite(redPin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(20);
  }

  // fade out from max to min in increments of 5 points:
  for (int fadeValue = 220 ; fadeValue >= 51; fadeValue -= 1) {
    // sets the value (range from 0 to 255):
    analogWrite(redPin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(20);
  }
}
