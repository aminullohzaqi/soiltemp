from django.core.exceptions import ValidationError

def validate_temp(value):
    temp_input = value
    if temp_input < 20 or temp_input > 40:
        message = "Maaf, data suhu tidak valid"
        raise ValidationError(message)

def validate_humidity(value):
    humidity_input = value
    if humidity_input < 0 or humidity_input > 100:
        message = "Maaf, data kelembaban tidak valid"
        raise ValidationError(message)

def validate_press(value):
    press_input = value
    if press_input < 1000 or press_input > 1015:
        message = "Maaf, data tekanan tidak valid"
        raise ValidationError(message)

def validate_SR(value):
    SR_input = value
    if SR_input < 0 or SR_input > 1300:
        message = "Maaf, data radiasi matahari tidak valid"
        raise ValidationError(message)

def validate_WS(value):
    WS_input = value
    if WS_input < 0 or WS_input > 20:
        message = "Maaf, data kecepatan angin tidak valid"
        raise ValidationError(message)

def validate_rainfall(value):
    rainfall_input = value
    if rainfall_input < 0 or rainfall_input > 120:
        message = "Maaf, data curah hujan tidak valid"
        raise ValidationError(message)
