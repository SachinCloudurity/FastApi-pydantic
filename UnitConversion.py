from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Conversion(BaseModel):
    value: float
    unit: str
    convert_to: str

conversions={
    'length':{'kms','miles'},
    'weight':{'pounds','kgs'},
    'time':{'hours','mins'},
    'temperature':{'far','cel'}
}

#retrives the available conversions for length,weight,time and temperature as a get method.
@app.get('/get_convertion/{conversions_type}')
def convert_length(conversions_type: str=None):
    return conversions[conversions_type]

#static multiplication factors. 
conversion_factors = {
    "miles_to_kms": 1.60934,
    "kms_to_miles": 0.621371,
    "pounds_to_kgs": 0.453592,
    "kgs_to_pounds": 2.20462,
    "hrs_to_mins": 60,
    "mins_to_hrs": 1/60,
}


#functions for variable multiplication factors.
def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9/5) + 32

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5/9
conversion_functions = {
    "cel_to_far": celsius_to_fahrenheit,
    "far_to_cel": fahrenheit_to_celsius,
}

# function that takes user input to perform unit conversions based on static or variable multiplication factors.
def convert(value: float, from_unit: str, to_unit: str) -> float:
    i = f"{from_unit}_to_{to_unit}"
    if i in conversion_factors and value>0 :
        return value * conversion_factors[i]
    elif i in conversion_functions:
        return conversion_functions[i](value)
    else:
        raise HTTPException(status_code=400, detail=f"Please enter correct conversion unit{conversions}")
    
#takes the input to update the results.
@app.post("/convert")
def convert_units(request: Conversion):
    result_value = convert(request.value, request.unit, request.convert_to)
    return {"value": result_value, "unit": request.convert_to}
