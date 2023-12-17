// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);

  Serial.println("");
  delay(100);
}

struct acc {
  float x;
  float y;
  float z;
};

unsigned long previousMillis = 0;
const int base_size = 10;
acc base_acc[base_size];
acc base_gyro[base_size];
int base_values = 0;

acc avg_a, avg_g;

void calculateAverage(struct acc &avg_a, struct acc &avg_g) {
  for(int i = 0; i < base_size; i++) {
    avg_a.x += base_acc[i].x/base_size;
    avg_a.y += base_acc[i].y/base_size;
    avg_a.z += base_acc[i].z/base_size;
    avg_g.x += base_gyro[i].x/base_size;
    avg_g.y += base_gyro[i].y/base_size;
    avg_g.z += base_gyro[i].z/base_size;
  }
}

void loop() {

  unsigned long currentMillis = millis();

  if(currentMillis - previousMillis >= 500) { // milliseconds
    previousMillis = currentMillis;

    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    float ax = a.acceleration.x;
    float ay = a.acceleration.y;
    float az = a.acceleration.z;
    float mag = sqrt(pow(ax,2)+pow(ay,2)+pow(az,2));
    float gx = g.gyro.x;
    float gy = g.gyro.y;
    float gz = g.gyro.z;

    if(base_values < base_size) {
      acc a1; a1.x = ax; a1.y = ay; a1.z = az;
      acc a2; a2.x = gx; a2.y = gy; a2.z = gz;
      base_acc[base_values] = a1;
      base_gyro[base_values] = a2;
      base_values++;
      if(base_values == base_size) {
        calculateAverage(avg_a, avg_g);
        Serial.print(avg_a.x); Serial.print(" "); Serial.print(avg_a.y); Serial.print(" "); Serial.println(avg_a.z);
        Serial.print(avg_g.x); Serial.print(" "); Serial.print(avg_g.y); Serial.print(" "); Serial.println(avg_g.z);
        digitalWrite(13, HIGH);
      }
    } else {
      Serial.print("Acc: "); Serial.print(ax-avg_a.x); Serial.print(", "); Serial.print(ay-avg_a.y); Serial.print(", "); Serial.println(az-avg_a.z);
      Serial.print("Gyro: "); Serial.print(gx-avg_g.x); Serial.print(", "); Serial.print(gy-avg_g.y); Serial.print(", "); Serial.println(gz-avg_g.z);
      Serial.println(" ");
    }
    

  }
  
}