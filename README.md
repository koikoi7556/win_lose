# Janken Simulation
Djangoの基本を勉強したのでそのアウトプット。Herokuにデプロイ済み。[こちら](https://win-lose.herokuapp.com/janken/)  
<small>※Heroku無料プランを使用しているためスリープ後の起動に20秒かかる。</small>

## アプリの内容
少し凝った、じゃんけんゲームを作った。ラジオボタンで自身の手を選択し、勝負する仕組みなっている。  
<img src="https://user-images.githubusercontent.com/38366932/69770963-5712b380-11ce-11ea-8366-7932a176eb2e.png" width="300px">

このアプリの一番の魅力は **誰でもじゃんけんの結果画面を作れる** ことだ。  
これにより、誰かが作成した結果画面をユーザー間で共有して、**ランダム**に表示される。  
また、その作品を「Like」することで評価を得ることもできる。  
面白おかしい結果画面をみんなで作ってもらうことが目的だ。  

<img src="https://user-images.githubusercontent.com/38366932/69770929-3ba7a880-11ce-11ea-8d77-2419744f80e7.png" width="300px">

ユーザー登録を行うことでメニューから「対戦履歴・作った結果画面・Likeリスト」を閲覧することができる。  
index番号をクリックするとその結果画面に遷移する。  

<img src="https://user-images.githubusercontent.com/38366932/69771010-92ad7d80-11ce-11ea-914f-c04c555e5eef.PNG" width="300px">
