#define SERIAL_RATE 57600

#define MOTOR_PINS 6, 7, 2, 3, 4, 5
#define MOTOR_FLIP 1, 1, 1, 1, 0, 1

#define CMD_TIMEOUT 250
#define CMD_MAX_LEN 128

#define MOTORS_OFF 1500
#define MOTORS_MIN 1100
#define MOTORS_MAX 1900

#include <Servo.h>

Servo motors[6];

int *read_speeds(void);

const int motor_pins[6] = {MOTOR_PINS};
const int motor_flip[6] = {MOTOR_FLIP};

void setup() {
	Serial.begin(SERIAL_RATE);
	Serial.setTimeout(CMD_TIMEOUT);

	pinMode(LED_BUILTIN, OUTPUT);

	for (int i = 0; i < 6; i++) {
		motors[i].attach(motor_pins[i], MOTORS_MIN, MOTORS_MAX);
		motors[i].writeMicroseconds(MOTORS_OFF);
	}
}

void loop() {
	int *motor_speeds = read_speeds();

	digitalWrite(LED_BUILTIN, motor_speeds != NULL);

	for (int i = 0; i < 6; i++) {
		int speed = MOTORS_OFF;
		if (motor_speeds != NULL) {
		    speed = motor_speeds[i];
            if (motor_flip[i])
                speed = 2 * MOTORS_OFF - speed;
        }
		motors[i].writeMicroseconds(speed);
	}
}

int *read_speeds() {
	char cmd_buffer[CMD_MAX_LEN];
	if (!Serial.readBytesUntil('\n', cmd_buffer, CMD_MAX_LEN))
		return NULL;

	int motor_speeds[6];
	size_t fields_filled = sscanf(cmd_buffer, "!%d:%d:%d:%d:%d:%d;",
		&motor_speeds[0], &motor_speeds[1], &motor_speeds[2], &motor_speeds[3], &motor_speeds[4], &motor_speeds[5]);

	if (fields_filled == 6)
		return motor_speeds;
	else
		return NULL;
}
