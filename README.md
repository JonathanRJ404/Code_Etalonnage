# SPN1 Calibration

## Requirements 

* install [Python 3.9.2](adr)
* install all module 

```sh
pip install -r requirements.txt 
``` 

## Input
Prepare 2 .csv files

data_test.csv with columns:
- TIMESTAMP: "%Y-%m-%d %H:%M:%S"
- GHI_test: float
- DHI_test: float

data_ref.csv with columns:
- TIMESTAMP: "%Y-%m-%d %H:%M:%S"
- GHI_ref: float
- DHI_ref: float
- Temp: float

move them into "data" folder
## Run
Run calibration.py in terminal

## Exemple
```sh
python calibration_spn1.py
```
## Output
Find the plots and the calibration certificate in output folder
