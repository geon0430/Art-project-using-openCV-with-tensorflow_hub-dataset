# Art-project-using-openCV-with-tensorflow_hub-dataset


Dataset: https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2

코드에서 보면 아래와 같이 url을 통해 학습이 끝난 모델을 불러오기에 datasets을 다운받을 필요는 없음
```
hub_handle_2 = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle_2)
```
-----
# 실행

### requirements.txt 설치
```
pip install -r requirements.txt
```
### web 실행
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```


## Result

<img width="400" alt="input" src="https://github.com/geon0430/Art-project-using-openCV-with-tensorflow_hub-dataset/assets/114966864/4737dd61-d9b1-484e-b79f-1ee145a20ad7">   <img width="400" alt="result" src="https://github.com/geon0430/Art-project-using-openCV-with-tensorflow_hub-dataset/assets/114966864/64bbd20a-eef9-4632-a0a9-c083818541d1">



