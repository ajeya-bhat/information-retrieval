config_params={
  'preprocess_type': "stemming",
  "stopword_removal" : True,
  "index" : "tfidf",
  "tf_scheme" : "1"
}
#tf scheme : 1 is directly taking tf, 2 is 1+log(tf), 3 is log(1+tf)