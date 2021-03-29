from gpiozero import MotionSensor

pir = MotionSensor(18)
pir.wait_for_motion()
print("Motion detected!")