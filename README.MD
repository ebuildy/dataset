Will generate 2 files:
- access.log: HTTP access log (format is "HASH_IP URL TIMESTAMP")
    ex: "2075817ad0540682ddbe52563b58ad0c /api/search?query=Bowman-Watson&group=b&locale=fr 1641162891"
- end_users.csv: a CSV file with users details
    ex: "2075817ad0540682ddbe52563b58ad0c";"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3 like Mac OS X; ko-KR) AppleWebKit/535.38.3 (KHTML, like Gecko) Version/3.0.5 Mobile/8B112 Safari/6535.38.3";"South Georgia and the South Sandwich Islands";""

## usage

```
python data_gen.py --count=100 --output=./build
```

## deps

- https://github.com/google/python-fire
- https://pypi.org/project/Faker/