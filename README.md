# Art-project-using-openCV-with-tensorflow_hub-dataset


Dataset: https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2

there is no need to download datasets because the trained model is loaded through the url as shown below.
```
hub_handle_2 = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle_2)
```
-----
# Execution

### requirements.txt install
```
pip install -r requirements.txt
```
### web execution
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```


## Result

<img width="400" alt="input" src="https://github.com/geon0430/Art-project-using-openCV-with-tensorflow_hub-dataset/assets/114966864/4737dd61-d9b1-484e-b79f-1ee145a20ad7">   <img width="400" alt="result" src="https://github.com/geon0430/Art-project-using-openCV-with-tensorflow_hub-dataset/assets/114966864/64bbd20a-eef9-4632-a0a9-c083818541d1">



