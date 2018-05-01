#define SERIAL_BAUDRATE 57600

#define MOTOR_PINS 6, 7, 2, 3, 4, 5
#define MOTOR_FLIP 1, 1, 1, 1, 0, 1

#define STEPPER_PINS 8, 9, 10, 11

#define COMMAND_TIMEOUT 250
#define COMMAND_BUFSIZE 128

#define STEPPER_RPM 22

#define MOTORS_OFF 1500
#define MOTORS_MIN 1100
#define MOTORS_MAX 1900

#include <Servo.h>
#include <CheapStepper.h>

Servo motors[6];
CheapStepper stepper;

const int motor_pins[6] = {MOTOR_PINS};
const int motor_flip[6] = {MOTOR_FLIP};
const int stepper_pins[4] = {STEPPER_PINS};

int stepper_direction;

void run_stepper(void);
bool read_command(char *buffer);

void setup() {
    // Initialize the serial connection and built-in LED
    Serial.begin(SERIAL_BAUDRATE);
    pinMode(LED_BUILTIN, OUTPUT);

    // Initialize each of the motor ESCs
    for (int i = 0; i < 6; i++) {
        motors[i].attach(motor_pins[i], MOTORS_MIN, MOTORS_MAX);
        motors[i].writeMicroseconds(MOTORS_OFF);
    }

    // Initialize the stepper motor
    stepper = CheapStepper(STEPPER_PINS);
    stepper.setRpm(STEPPER_RPM);
}

void loop() {
    char command_buffer[COMMAND_BUFSIZE];
    int motor_speeds[6], stepper_speed;
    bool valid_command_received = false;

    // Try and read a command from serial
    if (read_command(command_buffer)) {
        // If a command was received, try and parse it
        auto fields_filled = sscanf(command_buffer, "!%d,%d,%d,%d,%d,%d,%d",
            &motor_speeds[0],
            &motor_speeds[1],
            &motor_speeds[2],
            &motor_speeds[3],
            &motor_speeds[4],
            &motor_speeds[5],
            &stepper_speed);

        // Check whether all of the fields were filled
        valid_command_received = fields_filled == 7;
    }

    // Update the built-in LED to show whether a valid command was received
    digitalWrite(LED_BUILTIN, valid_command_received);

    // Update stepper_direction, scaling the speed down to at most 1 step
    if (valid_command_received)
        stepper_direction = (stepper_speed > 0) - (stepper_speed < 0);
    else
        stepper_direction = 0;

    // Write the motor speeds to the ESCs
    for (auto i = 0; i < 6; i++) {
        int speed = valid_command_received
            ? motor_speeds[i]
            : MOTORS_OFF;
        if (motor_flip[i])
            speed = 2 * MOTORS_OFF - speed;
        motors[i].writeMicroseconds(speed);
    }
}

// Moves the stepper motor one step in stepper_direction
// If stepper direction is 0 (stopped), this does nothing
void run_stepper() {
    if (stepper_direction > 0)
        stepper.stepCW();
    else if (stepper_direction < 0)
        stepper.stepCCW();
}

// Reads a command from serial (ending with '\n') into the provided buffer
// Returns whether the read completed successfully within the timeout
// run_stepper() is called while waiting for data
bool read_command(char *buffer) {
    auto index = 0;
    auto start_millis = millis();

    while (millis() - start_millis < COMMAND_TIMEOUT) {
        if (Serial.available()) {
            // Read a character into the buffer, and check if it is a newline
            if ((buffer[index++] = Serial.read()) == '\n') {
                // If it is a newline, append NUL and return true (success)
                buffer[index] = '\0';
                return true;
            }
            // If at the end of the buffer, return false (failure)
            if (index == COMMAND_BUFSIZE - 1)
                return false;
        } else {
            // Run the stepper while waiting for data
            run_stepper();
        }
    }
    // Timed out, return false (failure)
    return false;
}
