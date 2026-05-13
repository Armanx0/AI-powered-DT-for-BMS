"""Data validation utilities"""

from app.utils.constants import (
    VOLTAGE_MIN, VOLTAGE_MAX,
    TEMPERATURE_MIN, TEMPERATURE_MAX,
    CURRENT_MAX
)
from app.utils.exceptions import InvalidBatteryDataError


def validate_voltage(voltage: float) -> bool:
    """Validate battery voltage"""
    return VOLTAGE_MIN <= voltage <= VOLTAGE_MAX


def validate_current(current: float) -> bool:
    """Validate battery current"""
    return -CURRENT_MAX <= current <= CURRENT_MAX


def validate_temperature(temperature: float) -> bool:
    """Validate battery temperature"""
    return TEMPERATURE_MIN <= temperature <= TEMPERATURE_MAX


def validate_battery_cycle(voltage: float, current: float, temperature: float) -> None:
    """Validate complete battery cycle data"""
    errors = []

    if not validate_voltage(voltage):
        errors.append(f"Voltage {voltage}V out of range [{VOLTAGE_MIN}, {VOLTAGE_MAX}]")

    if not validate_current(current):
        errors.append(f"Current {current}A out of range [-{CURRENT_MAX}, {CURRENT_MAX}]")

    if not validate_temperature(temperature):
        errors.append(f"Temperature {temperature}°C out of range [{TEMPERATURE_MIN}, {TEMPERATURE_MAX}]")

    if errors:
        raise InvalidBatteryDataError("; ".join(errors))
