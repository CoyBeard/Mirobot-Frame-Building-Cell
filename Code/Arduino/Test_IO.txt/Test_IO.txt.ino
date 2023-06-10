#include <Servo.h>
#include <Stepper.h>

#include <AccelStepper.h>
#include <MultiStepper.h>

const int GlueExtrudeMotorStepsPerRevolution = 200;
int stepCount = 0;

int RunProgram1 = true;
int RunProgram2 = false;
int RunProgram3 = false;


//Stepper Pins
const int stepX = 4;
const int dirX  = 5;
//const int enPinX = 27;

const int stepY = 6;
const int dirY  = 7;
//const int enPinY = 30;

const int stepZ = 8;
const int dirZ  = 9;
//const int enPinZ = 30;

const int step1 = 10;
const int dir1  = 44;
//const int enPin1 = 30;

const int step2 = 12;
const int dir2  = 13;
//const int enPin2 = 30;

const int step3 = 31;
const int dir3  = 32;
//const int enPin3 = 30;


//INPUTS
const int AxisXLimit = 2;
const int AxisYLimit = 3;
const int AxisZLimit = 53;
const int MiroAtGlue = 52;
const int StickPresent = 2;

int AxisXLimitState = 0;
int AxisYLimitState = 0;
int AxisZLimitState = 0;
int MiroAtGlueState = 0;
int StickPresentState = 0;


//OUTPUTS
const int PumpMotor = 46;
const int SunctionCupsRelease = 47;
const int SpareOP5 = 48;
const int SpareOP6 = 49;


//Bolean
int RobotHomed = false;


// Define some steppers and the pins the will use
AccelStepper AxisX(AccelStepper::DRIVER, stepX, dirX); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

AccelStepper AxisY(AccelStepper::DRIVER, stepY, dirY); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

AccelStepper AxisZ(AccelStepper::DRIVER, stepZ, dirZ); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

AccelStepper Axis1(AccelStepper::DRIVER, step1, dir1); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

AccelStepper Axis2(AccelStepper::DRIVER, step2, dir2); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

AccelStepper Axis3(AccelStepper::DRIVER, step3, dir3); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5

Stepper GlueExtrudeMotor(GlueExtrudeMotorStepsPerRevolution, 33, 34, 35, 36);

Servo Wrist;

//const byte enablePinB = enPinB;  // ***** pin 8 is the enable pin
//const byte enablePinC = enPinC;  // ***** pin 8 is the enable pin


void setup() {
  Serial.begin(9600);
  while (!Serial);

  //Steppers
  //pinMode(enablePinB, OUTPUT); // **** set the enable pin to output
  //pinMode(enablePinC, OUTPUT); // **** set the enable pin to output
  
  //digitalWrite(enablePinB, LOW); // *** set the enable pin low
  //digitalWrite(enablePinC, LOW); // *** set the enable pin low

  pinMode(stepX,OUTPUT);
  pinMode(dirX,OUTPUT);

  pinMode(stepY,OUTPUT);
  pinMode(dirY,OUTPUT);

  pinMode(stepZ,OUTPUT);
  pinMode(dirZ,OUTPUT);

  pinMode(step1,OUTPUT);
  pinMode(dir1,OUTPUT);

  pinMode(step2,OUTPUT);
  pinMode(dir2,OUTPUT);

  pinMode(step3,OUTPUT);
  pinMode(dir3,OUTPUT);

  Wrist.attach(11);

  digitalWrite(dirX,HIGH);

  digitalWrite(dirY,LOW);

  digitalWrite(dirZ,HIGH);

  digitalWrite(dir1,LOW);

  digitalWrite(dir2,LOW);

  digitalWrite(dir3,LOW);

  AxisX.setMaxSpeed(1000000000.0);
  AxisX.setAcceleration(100.0);
    
  AxisY.setMaxSpeed(100000000.0);
  AxisY.setAcceleration(10000.0);

  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);

  Axis1.setMaxSpeed(100000000.0);
  Axis1.setAcceleration(10000.0);

  Axis2.setMaxSpeed(100000000.0);
  Axis2.setAcceleration(10000.0);

  Axis3.setMaxSpeed(100000000.0);
  Axis3.setAcceleration(10000.0);

  //Setup IO
  //INPUTS
  pinMode (AxisXLimit, INPUT_PULLUP);
  pinMode (AxisYLimit, INPUT_PULLUP);
  pinMode (AxisZLimit, INPUT_PULLUP);
  pinMode (MiroAtGlue, INPUT_PULLUP);
  pinMode (StickPresent, INPUT_PULLUP);

  //OUTPUTS
  pinMode (PumpMotor, OUTPUT);
  pinMode (SunctionCupsRelease, OUTPUT);
  pinMode (SpareOP5, OUTPUT);
  pinMode (SpareOP6, OUTPUT);

  //Set Outputs To High
  digitalWrite (PumpMotor, LOW);
  digitalWrite (SunctionCupsRelease, LOW);
  digitalWrite (SpareOP5, LOW);
  digitalWrite (SpareOP6, LOW);
}

void StepperMove (int Degrees, int Direction, int SSpeed, int stepPin, int dirPin) {
  //convert steps to degrees 
  Degrees = Degrees * (14000 / 711);
  
  //Sets Direction
  if (Direction == 0) {
    digitalWrite(dirPin,LOW);
  }else if (Direction == 1) {
    digitalWrite(dirPin,HIGH);
  }

  //Enables the motor to move in a particular direction
  //Makes 200 pulses for making one full cycle rotation
  
  for(int x = 0; x < Degrees; x++) {
    digitalWrite(stepPin,HIGH);

    delayMicroseconds(pow(1.06,((SSpeed * -1) + 139.5)));//800 home speed, 10 == 100%, 100 = 50%, 3000 = 1%

    digitalWrite(stepPin,LOW);

    delayMicroseconds(pow(1.06,((SSpeed * -1) + 139.5)));//1000
  }
}

void robotHome (){
  Serial.println("Robot Homing");

  digitalWrite(dirY, LOW);
  AxisYLimitState = digitalRead(AxisYLimit);
  while (AxisYLimitState == 1){
    digitalWrite(stepY, HIGH);
    delayMicroseconds(200);
    digitalWrite(stepY, LOW);
    delayMicroseconds(200);

    AxisYLimitState = digitalRead(AxisYLimit);
  }

  //Read Inputs
  AxisXLimitState = digitalRead(AxisXLimit);
  AxisYLimitState = digitalRead(AxisYLimit);
  AxisZLimitState = digitalRead(AxisZLimit);
    
  //Print Inputs
  Serial.print("Axis X LS: ");
  Serial.println(AxisXLimitState);
  Serial.print("Axis Y LS: ");
  Serial.println(AxisYLimitState);
  Serial.print("Axis Z LS: ");
  Serial.println(AxisZLimitState);

  delay(100);

  AxisYLimitState = digitalRead(AxisYLimit);
  if (AxisYLimitState == 0){
    Serial.println("Axis Y Zero Found");
    AxisY.setMaxSpeed(1000000000.0);
    AxisY.setAcceleration(10000.0);
    AxisY.move(500);
    while (AxisY.distanceToGo() != 0) {
      AxisY.run();
    }
    if (AxisY.distanceToGo() == 0) {
      Serial.println("Axis Y At Zero");
    }
  }

  digitalWrite(dirX, HIGH);
  AxisXLimitState = digitalRead(AxisXLimit);
  while (AxisXLimitState == 1){
    digitalWrite(stepX, HIGH);
    delayMicroseconds(200);
    digitalWrite(stepX, LOW);
    delayMicroseconds(200);

    AxisXLimitState = digitalRead(AxisXLimit);
  }

  //Read Inputs
  AxisXLimitState = digitalRead(AxisXLimit);
  AxisYLimitState = digitalRead(AxisYLimit);
  AxisZLimitState = digitalRead(AxisZLimit);
    
  //Print Inputs
  Serial.print("Axis X LS: ");
  Serial.println(AxisXLimitState);
  Serial.print("Axis Y LS: ");
  Serial.println(AxisYLimitState);
  Serial.print("Axis Z LS: ");
  Serial.println(AxisZLimitState);

  delay(100);
  
  AxisXLimitState = digitalRead(AxisXLimit);
  if (AxisXLimitState == 0){
    Serial.println("Axis X Zero Found");
    AxisX.setMaxSpeed(1000000000.0);
    AxisX.setAcceleration(10000.0);
    AxisX.move(-500);
    while (AxisX.distanceToGo() != 0) {
      AxisX.run();
    }
    if (AxisX.distanceToGo() == 0) {
      Serial.println("Axis X At Zero");
    }
  }

  Serial.println("Move to Z Home Pos");
  AxisX.setMaxSpeed(1000000000000.0);
  AxisX.setAcceleration(10000.0);
  AxisY.setMaxSpeed(1000000000000.0);
  AxisY.setAcceleration(10000.0);
  AxisX.move(-8000);
  AxisY.move(7000);
  while (AxisX.distanceToGo() != 0 || AxisY.distanceToGo() != 0) {
    AxisX.run();
    AxisY.run();
  }
  if (AxisX.distanceToGo() == 0 && AxisY.distanceToGo() == 0) {
    Serial.println("At Z Home Pos");
  }

  digitalWrite(dirZ, LOW);
  AxisZLimitState = digitalRead(AxisZLimit);
  while (AxisZLimitState == 1){
    digitalWrite(stepZ, HIGH);
    delayMicroseconds(200);
    digitalWrite(stepZ, LOW);
    delayMicroseconds(200);

    AxisZLimitState = digitalRead(AxisZLimit);
  }

  //Read Inputs
  AxisXLimitState = digitalRead(AxisXLimit);
  AxisYLimitState = digitalRead(AxisYLimit);
  AxisZLimitState = digitalRead(AxisZLimit);
    
  //Print Inputs
  Serial.print("Axis X LS: ");
  Serial.println(AxisXLimitState);
  Serial.print("Axis Y LS: ");
  Serial.println(AxisYLimitState);
  Serial.print("Axis Z LS: ");
  Serial.println(AxisZLimitState);

  delay(100);
  
  AxisZLimitState = digitalRead(AxisZLimit);
  if (AxisZLimitState == 0){
    Serial.println("Axis Z Zero Found");
    AxisZ.setMaxSpeed(1000000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.move(75000);
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("Axis Z At Zero");
    }
  }

  Serial.println("Wrist= 0deg");
  Wrist.write(0);
  delay(15);

  Serial.println("Robot Homed");
  RobotHomed = true;
}

void loop() {
  if(Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');

    //Outputs
    if (input.equals("h")) {
      robotHome();
    }
    if (input.equals("k3")) {
      digitalWrite(PumpMotor, HIGH);
      Serial.println("Output D44 HIGH");
      delay(2000);
      digitalWrite(PumpMotor, LOW);
      Serial.println("Output D44 LOW");
    }
    else if (input.equals("k4")) {
      digitalWrite(SunctionCupsRelease, HIGH);
      Serial.println("Output D45 HIGH");
      delay(2000);
      digitalWrite(SunctionCupsRelease, LOW);
      Serial.println("Output D45 LOW");
    }
    else if (input.equals("k5")) {
      digitalWrite(SpareOP5, HIGH);
      Serial.println("Output D46 HIGH");
      delay(2000);
      digitalWrite(SpareOP5, LOW);
      Serial.println("Output D46 LOW");
    }
    else if (input.equals("k6")) {
      digitalWrite(SpareOP6, HIGH);
      Serial.println("Output D47 HIGH");
      delay(2000);
      digitalWrite(SpareOP6, LOW);
      Serial.println("Output D47 LOW");
    }
    else if (input.equals("k3.5")) {
      digitalWrite(PumpMotor, HIGH);
      Serial.println("Output D44 HIGH");
      delay(5000);
      digitalWrite(PumpMotor, LOW);
      Serial.println("Output D44 LOW");
    }
    else if (input.equals("sx")) {
      Serial.println("Stepper X Move");
      StepperMove(20,1,20, stepX, dirX);
      Serial.println("Stepper X Move Complete");
    }
    else if (input.equals("sy")) {
      Serial.println("Stepper Y Move");
      StepperMove(20,1,20, stepY, dirY);
      Serial.println("Stepper Y Move Complete");
    }
    else if (input.equals("ax-")) {
      Serial.println("Jog Axis X= -500");
      AxisX.move(-500);
      while (AxisX.distanceToGo() != 0) {
        AxisX.run();
      }
      if (AxisX.distanceToGo() == 0) {
        Serial.println("Axis X Move Complete");
      }
    }
    else if (input.equals("ax")) {
      Serial.println("Jog Axis X= 500");
      AxisX.move(500);
      while (AxisX.distanceToGo() != 0) {
        AxisX.run();
      }
      if (AxisX.distanceToGo() == 0) {
        Serial.println("Axis X Move Complete");
      }
    }
    else if (input.equals("ay-")) {
      Serial.println("Jog Axis Y= -300");
      AxisY.move(-300);
      while (AxisY.distanceToGo() != 0) {
        AxisY.run();
      }
      if (AxisY.distanceToGo() == 0) {
        Serial.println("Axis Y Move Complete");
      }
    }
    else if (input.equals("ay")) {
      Serial.println("Jog Axis Y= 300");
      AxisY.move(300);
      while (AxisY.distanceToGo() != 0) {
        AxisY.run();
      }
      if (AxisY.distanceToGo() == 0) {
        Serial.println("Axis Y Move Complete");
      }
    }
    else if (input.equals("az-")) {
      Serial.println("Jog Axis Z= -300");
      AxisZ.move(-300);
      while (AxisZ.distanceToGo() != 0) {
        AxisZ.run();
      }
      if (AxisZ.distanceToGo() == 0) {
        Serial.println("Axis Z Move Complete");
      }
    }
    else if (input.equals("az")) {
      Serial.println("Jog Axis Z= 300");
      AxisZ.move(300);
      while (AxisZ.distanceToGo() != 0) {
        AxisZ.run();
      }
      if (AxisZ.distanceToGo() == 0) {
        Serial.println("Axis Z Move Complete");
      }
    }
    else if (input.equals("a1-")) {
      Serial.println("Jog Axis 1= -1000");
      Axis1.move(-1000);
      while (Axis1.distanceToGo() != 0) {
        Axis1.run();
      }
      if (Axis1.distanceToGo() == 0) {
        Serial.println("Axis 1 Move Complete");
      }
    }
    else if (input.equals("a1")) {
      Serial.println("Jog Axis 1= 1000");
      Axis1.move(1000);
      while (Axis1.distanceToGo() != 0) {
        Axis1.run();
      }
      if (Axis1.distanceToGo() == 0) {
        Serial.println("Axis 1 Move Complete");
      }
    }
    else if (input.equals("a2-")) {
      Serial.println("Jog Axis 2= -1000");
      Axis2.move(-1000);
      while (Axis2.distanceToGo() != 0) {
        Axis2.run();
      }
      if (Axis2.distanceToGo() == 0) {
        Serial.println("Axis 2 Move Complete");
      }
    }
    else if (input.equals("a2")) {
      Serial.println("Jog Axis 2= 1000");
      Axis2.move(1000);
      while (Axis2.distanceToGo() != 0) {
        Axis2.run();
      }
      if (Axis2.distanceToGo() == 0) {
        Serial.println("Axis 2 Move Complete");
      }
    }
    else if (input.equals("a3-")) {
      Serial.println("Jog Axis 3= -1000");
      Axis3.move(-1000);
      while (Axis3.distanceToGo() != 0) {
        Axis3.run();
      }
      if (Axis3.distanceToGo() == 0) {
        Serial.println("Axis 3 Move Complete");
      }
    }
    else if (input.equals("a3")) {
      Serial.println("Jog Axis 3= 1000");
      Axis3.move(1000);
      while (Axis3.distanceToGo() != 0) {
        Axis3.run();
      }
      if (Axis3.distanceToGo() == 0) {
        Serial.println("Axis 3 Move Complete");
      }
    }
    else if (input.equals("ge-")) {
      Serial.println("Jog Glue Extruder= -1000");
      for (int x = 0; x < 400000; x++) {
        GlueExtrudeMotor.step(1);
        delay(5);
      }
      Serial.println("Glue Extruder Move Complete");
      
    }
    else if (input.equals("ge")) {
      Serial.println("Jog Glue Extruder= 1000");
      GlueExtrudeMotor.step(10000);
      Serial.println("Glue Extruder Move Complete");
    }
    else if (input.equals("w0")) {
      Serial.println("Wrist= 0deg");
      Wrist.write(0);
      delay(1500);
    }
    else if (input.equals("w90")) {
      Serial.println("Wrist= 90deg");
      Wrist.write(90);
      delay(1500);
    }
    else if (input.equals("w180")) {
      Serial.println("Wrist= 180deg");
      Wrist.write(180);
      delay(15);
    }
    else if (input.equals("w60")) {
      Serial.println("Wrist= 60deg");
      Wrist.write(60);
      delay(15);
    }
    else if (input.equals("w220")) {
      Serial.println("Wrist= 220deg");
      Wrist.write(220);
      delay(15);
    }
    else if (input.equals("w240")) {
      Serial.println("Wrist= 240deg");
      Wrist.write(240);
      delay(15);
    }
    else if (input.equals("w250")) {
      Serial.println("Wrist= 250deg");
      Wrist.write(250);
      delay(15);
    }else if (input.equals("w260")) {
      Serial.println("Wrist= 260deg");
      Wrist.write(260);
      delay(15);
    }

    //Read Inputs
    AxisXLimitState = digitalRead(AxisXLimit);
    AxisYLimitState = digitalRead(AxisYLimit);
    AxisZLimitState = digitalRead(AxisZLimit);
    MiroAtGlueState = digitalRead(MiroAtGlue);
    StickPresentState = digitalRead(StickPresent);
  
    //Print Inputs
    Serial.print("Axis X LS: ");
    Serial.println(AxisXLimitState);
    Serial.print("Axis Y LS: ");
    Serial.println(AxisYLimitState);
    Serial.print("Axis Z LS: ");
    Serial.println(AxisZLimitState);
    Serial.print("MiroAtGlueState LS: ");
    Serial.println(MiroAtGlueState);
    Serial.print("StickPresentState: ");
    Serial.println(StickPresentState);

  }
  
}
