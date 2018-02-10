## 알랴죠-GUI
> 궁극의 CTF Flag  탐색기

여준호님께서 만드신 [알랴죠](https://github.com/JunhoYeo/Allyajyo) 프로젝트에서 GUI 기능을 추가한 알랴죠-GUI

## 기능

### 1. Binary Hex Viewer

라고는 하는데 굉장히 허접해 보이는 Hex Viewer다. 

##### 1) Hex 1바이트에 대응하는 Character를 오른쪽에 보여준다.

이걸 기능이라고 해야하나.. 싶지만 그냥 넣어보았다.

readable하지 않는 글자는 간단히 '.'으로 넣었다.

##### 2) 파일 헤더만 보고 File Type 알아내기

뭐 간단히 할수 있겠지만.. 뭔가 DIE같은거를 만들고 싶었는데.. 딱히 생각나는게 없어서 파일 헤더로만 유추했다.

##### 3) String 값에서 Flag로 의심되는 String을 표시해주기

설정에서 바꿀수 있게 만들긴 했는데 Flag로 보이는 String을 그냥 MessageBox로 뿌리는 기능을 만들었다. (사실 여준호님꺼 소스를 복붙했지만..)

##### 4) PNG나 JPG같은 이미지 파일 헤더 복구하기 (예정)

앞에 헤더가 손상되어 있을 경우 Chunk layout 등을 분석해서 파일 헤더를 복구해주는 기능을 만들 **예정**이다.

### 2. Cryptography (예정)

내가 가장 취약한 Cryptography 분야에 base64니 md5*~~애X 뒤진 5~~* 니 다 사이트 들어가기는 귀찮아서 all-in-one으로 항상 되어있는것을 원했는데, 이참에 다른 암호기법도 알아보는겸 만들어볼 **예정**이다.

### 3. Web Crawler

##### 1. BeautifulSoup로 크롤링한 HTML 표시해주기

다른게 없이 그냥 BeautifulSoup로 HTML 긁어오는거다.

##### 2. HTML중에 Flag로 유추되는거 알려주기 (예정)

그럴리는 없겠지만, 마이크 테스트 겸으로 HTML에 주석으로 표시해주는 경우가 있으면 그런걸 알려준다.
