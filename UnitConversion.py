from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Conversion(BaseModel):
    value: float
    unit: str
    convert_to: str

conversions = {
    'length': {'kms', 'miles', 'meters'},
    'weight': {'pounds', 'kgs'},
    'time': {'hrs', 'mins', 'secs'},
    'temperature': {'far', 'cel'}
}

#retrives the available conversions for length,weight,time and temperature as a get method.
@app.get('/get_conversion/{conversions_type}')
def get_conversions(conversions_type: str = None):
    if conversions_type not in conversions:
        raise HTTPException(status_code=400, detail="Invalid conversion type")
    return list(conversions[conversions_type])

#static multiplication factors, i have taken meters,kgs and seconds as the base units
conversion_factors = {
    'length': {'kms': 1000,'miles': 1609.34,'meters': 1 },
    'weight': {'pounds': 0.453592, 'kgs': 1},
    'time': {'hrs': 3600,'mins': 60,'secs': 1}
}


#functions for variable multiplication factors.
def celsius_to_fahrenheit(c: float) -> float:
    if c < -273.15:
        raise HTTPException(status_code=400, detail="Temperature below absolute zero is not possible")
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f: float) -> float:
    if f < -459.67:
        raise HTTPException(status_code=400, detail="Temperature below absolute zero is not possible")
    return (f - 32) * 5/9

#first function converts every given unit to a bse unit(meter,kgs,secs).
def tobase_convert(value: float, from_unit: str, unit_type: str) -> float:
    if unit_type == 'temperature':
        if from_unit == 'far':
            return fahrenheit_to_celsius(value)
        return value
    elif value>0:
        return value * conversion_factors[unit_type][from_unit]
    else: raise HTTPException(status_code=400, detail="Please give positive value for length, weight and time")
        
#second function converts every base unit to required unit.
def frombase_convert(value: float, to_unit: str, unit_type: str) -> float:
    if unit_type == 'temperature':
        if to_unit == 'far':
            return celsius_to_fahrenheit(value)
        return value
    else:
        return value / conversion_factors[unit_type][to_unit]


# function that takes user input to perform unit conversions based on static or variable multiplication factors.
def convert(value: float, from_unit: str, to_unit: str) -> float:
    unit_types = {utype: units for utype, units in conversions.items() if from_unit in units and to_unit in units}
    if not unit_types:
        raise HTTPException(status_code=400, detail=f"Invalid conversion units. Available conversions: {conversions}")
    
    unit_type = list(unit_types.keys())[0]
    base_value = tobase_convert(value, from_unit, unit_type)
    result_value = frombase_convert(base_value, to_unit, unit_type)
    return result_value
    
#takes the input to update the results.
@app.post("/convert")
def convert_units(request: Conversion):
    result_value = convert(request.value, request.unit, request.convert_to)
    return {"value": result_value, "unit": request.convert_to}
