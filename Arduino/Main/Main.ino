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
const int StickPresent = 40;//NC

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
bool RobotHomed = false;
bool a1Run = false;
bool a2Run = false;
bool a3Run = false;
int stickSpacingStp = 108;

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

  AxisX.setMaxSpeed(10000.0);
  AxisX.setAcceleration(13000.0);
    
  AxisY.setMaxSpeed(100000000.0);
  AxisY.setAcceleration(5000.0);

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
  pinMode (AxisXLimit, INPUT); //_PULLUP
  pinMode (AxisYLimit, INPUT);
  pinMode (AxisZLimit, INPUT);
  pinMode (MiroAtGlue, INPUT);
  pinMode (StickPresent, INPUT);

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
    delayMicroseconds(1000);//200
    digitalWrite(stepY, LOW);
    delayMicroseconds(1000);//200

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

    AxisY.setCurrentPosition(0);
    
    AxisY.setMaxSpeed(100000000.0);
    AxisY.setAcceleration(5000.0);
    AxisY.moveTo(100);//500
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
    delayMicroseconds(240);//200
    digitalWrite(stepX, LOW);
    delayMicroseconds(240);//200

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

    AxisX.setCurrentPosition(0);
    
    AxisX.setMaxSpeed(1000000.0);
    AxisX.setAcceleration(15000.0);
    AxisX.moveTo(-400);//-500
    while (AxisX.distanceToGo() != 0) {
      AxisX.run();
    }
    if (AxisX.distanceToGo() == 0) {
      Serial.println("Axis X At Zero");
    }
  }

  Serial.println("Move to Z Home Pos");
  AxisX.setMaxSpeed(1000000.0);
  AxisX.setAcceleration(15000.0);
  AxisY.setMaxSpeed(100000.0);//100000000
  AxisY.setAcceleration(1000.0);//5000
  AxisX.moveTo(-6800);//-8000
  AxisY.moveTo(1500);//7000
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
    delayMicroseconds(1000);//200
    digitalWrite(stepZ, LOW);
    delayMicroseconds(1000);//200

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

    AxisZ.setCurrentPosition(0);
    
    AxisZ.setMaxSpeed(100000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.moveTo(15000);//75000
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("Axis Z At Zero");
    }
  }

  Serial.println("Wrist= 64pwm90deg");
  Wrist.write(64);
  delay(15);

  Serial.println("Robot Homed");
  RobotHomed = true;
}

void runProg() {
  /*
  bool firstCycle = true;
  for (int x = 0; x < 11; x++) {//for 11 sticks
    
      
    Serial.println("Move to Stick");
    AxisX.setMaxSpeed(1000000.0);
    AxisX.setAcceleration(15000.0);
    AxisY.setMaxSpeed(100000.0);
    AxisY.setAcceleration(1000.0);
    AxisX.moveTo(-3600);//3200
    AxisY.moveTo(580 + (x * stickSpacingStp));//-920
    while (AxisX.distanceToGo() != 0 || AxisY.distanceToGo() != 0) {
      AxisX.run();
      AxisY.run();
      //Axis1.run();
    }
    if (AxisX.distanceToGo() == 0 && AxisY.distanceToGo() == 0) {
      Serial.println("At Stick 1");
    }
    
    Serial.println("Wrist= 64pwm90deg");
    Wrist.write(64);
    delay(15);
  
    Serial.println("Plunge to Stick");
    AxisZ.setMaxSpeed(100000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.moveTo(23800);//9300
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
      Axis1.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("On Stick");
    }
  
    digitalWrite(PumpMotor, HIGH);
    Serial.println("Pump HIGH");
    delay(500);
  
    Serial.println("Pick up Stick");
    AxisZ.setMaxSpeed(100000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.moveTo(17800);//-6500
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
      Axis1.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("Got Stick 1");
    }
  
    Serial.println("go x to inf conv");
    AxisX.setMaxSpeed(1000000.0);
    AxisX.setAcceleration(15000.0);
    AxisY.setMaxSpeed(100000000.0);
    AxisY.setAcceleration(1000.0);
    AxisX.moveTo(-10500);//-7250
    AxisY.moveTo(580);
    while (AxisX.distanceToGo() != 0 || AxisY.distanceToGo() != 0) {
      AxisX.run();
      AxisY.run();
      Axis1.run();
    }
    if (AxisX.distanceToGo() == 0 && AxisY.distanceToGo() == 0) {
      Serial.println("at x inf conv");
    }
  
    Serial.println("Wrist= 0pwm0deg");
    Wrist.write(0);
    delay(15);
  
    Serial.println("Plunge to inf Conv");
    AxisZ.setMaxSpeed(100000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.moveTo(19700);//2400
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
      Axis1.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("at z inf cov");
    }
    
    digitalWrite(PumpMotor, LOW);
    Serial.println("Pump LOW");
    delay(500);
  
    digitalWrite(SunctionCupsRelease, HIGH);
    Serial.println("SunctionCupsRelease HIGH");
    delay(500);
    digitalWrite(SunctionCupsRelease, LOW);
    Serial.println("SunctionCupsRelease LOW");
  
    Serial.println("back to travel height");
    AxisZ.setMaxSpeed(100000000.0);
    AxisZ.setAcceleration(10000.0);
    AxisZ.moveTo(17800);//-2400
    while (AxisZ.distanceToGo() != 0) {
      AxisZ.run();
      Axis1.run();
    }
    if (AxisZ.distanceToGo() == 0) {
      Serial.println("at travel height");
    }
  
    Serial.println("Wrist= 64pwm90deg");
    Wrist.write(64);
    delay(15);
  
    Serial.println("go x stick storage");
    AxisX.setMaxSpeed(1000000.0);
    AxisX.setAcceleration(15000.0);
    AxisX.moveTo(-3600);//7250
    while (AxisX.distanceToGo() != 0) {
      AxisX.run();
    }
    if (AxisX.distanceToGo() == 0) {
      Serial.println("at x stick storage");
    }

    if (firstCycle == false) {
      StickPresentState = digitalRead(StickPresent);
      while (StickPresentState == 0){
        StickPresentState = digitalRead(StickPresent);
        Axis1.run();
        //delay(1);
      }
      StickPresentState = digitalRead(StickPresent);
      while (StickPresentState == 1){
        StickPresentState = digitalRead(StickPresent);
        Axis1.run();
        //delay(1);
      }
    }
    firstCycle = false;
    
    Serial.println("Run inf conv");
    Axis1.setMaxSpeed(100000000.0);
    Axis1.setAcceleration(7000.0);//10000
    Axis1.move(7000);//25000
  }

  Serial.println("Run inf conv");
  Axis1.setMaxSpeed(100000000.0);
  Axis1.setAcceleration(7000.0);//10000
  Axis1.move(7000);//25000
  while (Axis1.distanceToGo() != 0) {
    Axis1.run();
  }

  Serial.println("Back to start");
  AxisX.setMaxSpeed(1000000.0);
  AxisX.setAcceleration(15000.0);
  AxisY.setMaxSpeed(100000.0);
  AxisY.setAcceleration(1000.0);
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisX.moveTo(-6800);
  AxisY.moveTo(1500);
  AxisZ.moveTo(15000);
  while (AxisX.distanceToGo() != 0 || AxisY.distanceToGo() != 0 || AxisZ.distanceToGo() != 0) {
    AxisX.run();
    AxisY.run();
    AxisZ.run();
  }
  if (AxisX.distanceToGo() == 0 && AxisY.distanceToGo() == 0 && AxisZ.distanceToGo() == 0) {
    Serial.println("At Start");
  }

  //wait for mirobot to be done
  delay(33000);

  Serial.println("go x to frame");
  AxisX.setMaxSpeed(1000000.0);
  AxisX.setAcceleration(15000.0);
  AxisX.moveTo(-19800);
  while (AxisX.distanceToGo() != 0) {
    AxisX.run();
  }
  if (AxisX.distanceToGo() == 0) {
    Serial.println("at frame");
  }

  Serial.println("go y on top of frame");
  AxisY.setMaxSpeed(100000000.0);
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisY.moveTo(2180);
  AxisZ.moveTo(14700);
  while (AxisZ.distanceToGo() != 0 || AxisY.distanceToGo() != 0) {
    AxisY.run();
    AxisZ.run();
  }
  if (AxisY.distanceToGo() == 0 || AxisZ.distanceToGo() == 0) {
    Serial.println("at y top of frame");
  }

  delay(500);

  Serial.println("press prame");
  AxisZ.setMaxSpeed(100.0);
  AxisZ.setAcceleration(100.0);
  AxisZ.moveTo(15300);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("pressed prame");
  }

  Serial.println("Pull up");
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisZ.moveTo(14700);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("pulled up");
  }

  Serial.println("pull out");
  AxisY.setMaxSpeed(100000000.0);
  AxisY.moveTo(1800);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("pulled out");
  }

  Serial.println("move down to pick up frame");
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisZ.moveTo(19500);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("moved");
  }

  Serial.println("get under frame");
  AxisY.setMaxSpeed(100000000.0);
  AxisY.moveTo(2050);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("under frame");
  }

  Serial.println("z pick up frame");
  AxisZ.setMaxSpeed(1000.0);
  AxisZ.setAcceleration(200.0);
  AxisZ.moveTo(13500);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("z got frame");
  }

  Serial.println("y pick up frame");
  AxisY.setMaxSpeed(100000000.0);
  AxisY.moveTo(1800);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("y got frame");
  }

  Serial.println("go x to frame");
  AxisX.setMaxSpeed(5000.0);
  AxisX.setAcceleration(5000.0);
  AxisX.moveTo(-32300);
  while (AxisX.distanceToGo() != 0) {
    AxisX.run();
  }
  if (AxisX.distanceToGo() == 0) {
    Serial.println("at frame");
  }

  Serial.println("move y over outfeed conveyor");
  AxisY.setMaxSpeed(1000.0);
  AxisY.moveTo(1100);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("y over outfeed convey");
  }

  Serial.println("let frame down onto conv");
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisZ.moveTo(21300);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("frame on conv");
  }

  Serial.println("pull out of frame");
  AxisY.setMaxSpeed(1000.0);
  AxisY.moveTo(600);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("out of frame");
  }

  Serial.println("let frame down onto conv");
  AxisZ.setMaxSpeed(100000000.0);
  AxisZ.setAcceleration(10000.0);
  AxisZ.moveTo(15000);
  while (AxisZ.distanceToGo() != 0) {
    AxisZ.run();
  }
  if (AxisZ.distanceToGo() == 0) {
    Serial.println("frame on conv");
  }

  Serial.println("x go around frame");
  AxisX.setMaxSpeed(5000.0);
  AxisX.setAcceleration(5000.0);
  AxisX.moveTo(-27300);
  while (AxisX.distanceToGo() != 0) {
    AxisX.run();
  }
  if (AxisX.distanceToGo() == 0) {
    Serial.println("x clear frame");
  }

  Serial.println("y go around frame");
  AxisY.setMaxSpeed(1000.0);
  AxisY.moveTo(1800);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("y clear frame");
  }

  Serial.println("x back to start");
  AxisX.setMaxSpeed(5000.0);
  AxisX.setAcceleration(5000.0);
  AxisX.moveTo(-6800);
  while (AxisX.distanceToGo() != 0) {
    AxisX.run();
  }
  if (AxisX.distanceToGo() == 0) {
    Serial.println("x At Start");
  }

  Serial.println("y back to start");
  AxisY.setMaxSpeed(1000.0);
  AxisY.moveTo(1500);
  while (AxisY.distanceToGo() != 0) {
    AxisY.run();
  }
  if (AxisY.distanceToGo() == 0) {
    Serial.println("y At Start");
  }
*/
delay(5000);

  Serial.println("Run outfeed conv");
  Axis3.setMaxSpeed(100000000.0);
  Axis3.setAcceleration(7000.0);//10000
  Axis3.move(13000);
  while (Axis3.distanceToGo() != 0) {
    Axis3.run();
  }




  
  
}

void loop() {
  if(Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');

    //Outputs
    if (input.equals("h")) {
      robotHome();
    }
    if (input.equals("r")) {
      runProg();
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
    else if (input.equals("axx-")) {
      Serial.println("Jog Axis X= -4000");
      AxisX.move(-4000);
      while (AxisX.distanceToGo() != 0) {
        AxisX.run();
      }
      if (AxisX.distanceToGo() == 0) {
        Serial.println("Axis X Move Complete");
      }
    }
    else if (input.equals("axx")) {
      Serial.println("Jog Axis X= 4000");
      AxisX.move(4000);
      while (AxisX.distanceToGo() != 0) {
        AxisX.run();
      }
      if (AxisX.distanceToGo() == 0) {
        Serial.println("Axis X Move Complete");
      }
    }
    else if (input.equals("axxx-")) {
      Serial.println("Jog Axis X= -8000");
      AxisX.move(-8000);
      while (AxisX.distanceToGo() != 0) {
        AxisX.run();
      }
      if (AxisX.distanceToGo() == 0) {
        Serial.println("Axis X Move Complete");
      }
    }
    else if (input.equals("axxx")) {
      Serial.println("Jog Axis X= 8000");
      AxisX.move(8000);
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
    else if (input.equals("azz")) {
      Serial.println("Jog Axis Z= 5000");
      AxisZ.move(5000);
      while (AxisZ.distanceToGo() != 0) {
        AxisZ.run();
      }
      if (AxisZ.distanceToGo() == 0) {
        Serial.println("Axis Z Move Complete");
      }
    }
    else if (input.equals("azzz")) {
      Serial.println("Jog Axis Z= 10000");
      AxisZ.move(10000);
      while (AxisZ.distanceToGo() != 0) {
        AxisZ.run();
      }
      if (AxisZ.distanceToGo() == 0) {
        Serial.println("Axis Z Move Complete");
      }
    }
    else if (input.equals("a1-")) {
      Serial.println("Jog Axis 1= -7000");
      Axis1.move(-7000);
      while (Axis1.distanceToGo() != 0) {
        Axis1.run();
      }
      if (Axis1.distanceToGo() == 0) {
        Serial.println("Axis 1 Move Complete");
      }
    }
    else if (input.equals("a1")) {
      Serial.println("Jog Axis 1= 7000");
      Axis1.move(7000);
      while (Axis1.distanceToGo() != 0) {
        Axis1.run();
      }
      if (Axis1.distanceToGo() == 0) {
        Serial.println("Axis 1 Move Complete");
      }
    }
    else if (input.equals("a2-")) {
      Serial.println("Jog Axis 2= -6000");
      Axis2.move(-6000);
      while (Axis2.distanceToGo() != 0) {
        Axis2.run();
      }
      if (Axis2.distanceToGo() == 0) {
        Serial.println("Axis 2 Move Complete");
      }
    }
    else if (input.equals("a2")) {
      Serial.println("Jog Axis 2= 6000");
      Axis2.move(6000);
      while (Axis2.distanceToGo() != 0) {
        Axis2.run();
      }
      if (Axis2.distanceToGo() == 0) {
        Serial.println("Axis 2 Move Complete");
      }
    }
    else if (input.equals("a3-")) {
      Serial.println("Jog Axis 3= -6000");
      Axis3.move(-13000);
      while (Axis3.distanceToGo() != 0) {
        Axis3.run();
      }
      if (Axis3.distanceToGo() == 0) {
        Serial.println("Axis 3 Move Complete");
      }
    }
    else if (input.equals("a3")) {
      Serial.println("Jog Axis 3= 6000");
      Axis3.move(13000);
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
    else if (input.equals("w66")) {
      Serial.println("Wrist= 66deg");
      Wrist.write(66);
      delay(15);
    }
    else if (input.equals("w64")) {
      Serial.println("Wrist= 64deg");
      Wrist.write(64);
      delay(15);
    }else if (input.equals("w62")) {
      Serial.println("Wrist= 62deg");
      Wrist.write(62);
      delay(15);
    }
    else if (input.equals("w60")) {
      Serial.println("Wrist= 60deg");
      Wrist.write(60);
      delay(15);
    }
    else if (input.equals("w58")) {
      Serial.println("Wrist= 58deg");
      Wrist.write(58);
      delay(15);
    }
    else if (input.equals("w56")) {
      Serial.println("Wrist= 56deg");
      Wrist.write(56);
      delay(15);
    }
    else if (input.equals("w54")) {
      Serial.println("Wrist= 54deg");
      Wrist.write(54);
      delay(15);
    }else if (input.equals("w52")) {
      Serial.println("Wrist= 52deg");
      Wrist.write(52);
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
