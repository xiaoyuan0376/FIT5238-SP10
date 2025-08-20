# Links

**Trello**: https://trello.com/invite/b/6878b5b9557913d8aebc154c/ATTId72e6b39b892ee5082eb0b3baf7d1ba28B60B1DF/fit5238-25t3-team-sp10

**Shared folder**: https://drive.google.com/drive/folders/1L5g6MnRxbFoso5pV_VTbMOAB_EgQEIQa?usp=drive_link

**Git**: https://github.com/xiaoyuan0376/FIT5238-SP10.git

# Run Instructions

## Step1:Warehouse installation

In the project folder, run:

```
pip install -r requirements.txt
```

## Step2:data generator

In the project folder, run:

```
python generateData.py
```

You will see a generate.csv in the real folder, which adds a line of data every second. The last line of the CSV is the output of the LSTM model used in this experiment.
careful:

> [!WARNING]
>
> 1. It is necessary to open the CSV file in read-only mode for observation, otherwise the program will report an error due to the file being occupied when opening the CSV file.
> 2. This file needs to be kept running in real-time in the background as a data source to generate real-time data

## Step3:run program

In the project folder, run:

```
python app.py
```

then enter on the website: http://127.0.0.1:5000/.

> [!WARNING]
>
> If there is no response when you click the login/registration button, please ensure that your network environment can access Google
> 
> You can use test.py to detect it :
> 
> ``` python test_network.py ```
> 
> If appear "data write success" message, it means your network is ok.
