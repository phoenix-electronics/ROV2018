import RPi.GPIO as GPIO


class Motor:
    PWM_FREQUENCY = 50

    def __init__(self, channel: int) -> None:
        GPIO.setup(channel, GPIO.OUT)
        self.PWM = GPIO.PWM(channel, Motor.PWM_FREQUENCY)
        self.start_pwm()

    @staticmethod
    def get_duty_cycle(speed: float) -> float:
        return Motor.PWM_FREQUENCY * (0.15 + 0.05 * max(-1.0, min(1.0, speed)))

    def start_pwm(self) -> None:
        self.PWM.start(self.get_duty_cycle(0))

    def stop_pwm(self) -> None:
        self.PWM.stop()

    def set_speed(self, speed: float) -> None:
        self.PWM.ChangeDutyCycle(self.get_duty_cycle(speed))
