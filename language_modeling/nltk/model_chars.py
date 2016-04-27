from nltk.model.ngram import NgramModel
from nltk.probability import LidstoneProbDist
import sys

train_prefix = sys.argv[1]
test_prefix = sys.argv[2]
grams = int(sys.argv[3])

suffixes = { "a", "v", "n" }

models = { }

for suffix in suffixes:
  # Get the model for whichever suffix you're looking at.
  words = [ ] 

  with open(train_prefix + suffix) as infile:
    for line in infile:
      line = line.rstrip()

      word_vec = [ ]
      for char in line:
        word_vec.append(char)

      words.append(word_vec)

  est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2) 

  models[suffix] = [ ]
  for i in range(2, grams):
    models[suffix].append(NgramModel(i, words, estimator = est))

total = 0
errors = 0

for suffix in suffixes:
  print("****** testing " + suffix + "******")
  with open(test_prefix + suffix) as infile:
    for line in infile:
      total += 1
      word = line.rstrip()
      word_vec = [ ]
      for char in word:
        word_vec.append(char)

      argmax_suffix = ""
      min_prob = 10000000
      for test_suffix in suffixes:
        prob = 0
        for model in models[test_suffix]:
          prob += model.entropy(word_vec)

        if prob < min_prob:
          min_prob = prob
          argmax_suffix = test_suffix

      if suffix != argmax_suffix:
        errors += 1
        print(suffix + "\t" + argmax_suffix + "\t" + word)

print("Made " + str(errors) + " errors of " + str(total))
