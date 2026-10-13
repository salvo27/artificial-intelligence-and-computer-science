# Deep Learning

| | |
|---|---|
| **Code** | 27009511 |
| **ECTS** | 9 |
| **Period** | Year 1, semester 1 |
| **Curriculum** | Computer Security, Data Science |
| **Lecturers** | Carlo Adornetto, Gianluigi Greco |
| **Exam format** | Project: design and implement an application that uses neural networks for machine learning tasks; graded in thirtieths (see below) |
| **Official page** | [Course page on corsi.unical.it](https://corsi.unical.it/lm/artificial-intelligence-and-computer-science/cds/studiare/activities/293075/) |

## Contents

- [Summary](summary.md)
- [Part 2: lab notes](labs.md): the eight labs (NumPy and Pandas, Keras, a network from scratch, CNNs, RNNs and NLP, autoencoders, attention and Transformers, optimization and hyperparameter tuning) and TensorBoard, with code, a parameters recap for every exercise and the problems found in the notebooks
- [Exercises and past exams](exercises/): [evaluation metrics](exercises/metrics.md)

## Exam

From the official course page:

- **Method:** an educational **project**. Students must show they can **design a computer application that uses neural networks** in machine learning tasks.
- **Criteria:** the ability to design and implement systems based on neural networks.
- **Grade:** the outcome of the project is a mark in thirtieths.

## Syllabus

_TBD: list the topics of the official syllabus._ Covered so far in the [summary](summary.md), following the lessons:

- Introduction: machine learning, regression, bias-variance, metrics, k-NN, trees, k-means
- Lesson 1: neural network basics (perceptron, loss, optimizers, backpropagation, initialization)
- Lesson 2: classification with Keras (IMDb, Reuters)
- Lesson 3: regression (Boston housing), overfitting and regularization
- Lesson 4: convolutional networks
- Lesson 5: pre-trained convnets, functional API, subclassing
- Lesson 6: autoencoders and VAEs
- Lesson 7: batch normalization, transposed convolution, leaky ReLU
- Lesson 8: U-Net and segmentation
- Lesson 9: GANs, pix2pix, CycleGAN
- Lesson 10: recurrent networks, LSTM, GRU
- Lesson 11: word embeddings
- Lesson 12: language modeling
- Lesson 13: seq2seq, attention, Transformer
- Lesson 14: machine learning with graphs, GNNs
- Lesson 15: diffusion models, generative inverse design (GIDnets)

Laboratory (Carlo Adornetto), in the [lab notes](labs.md):

- Lab 1: NumPy, Pandas, Matplotlib; linear regression and gradient descent by hand
- Lab 2: TensorFlow and Keras; binary and multi-class classification; K-fold cross-validation
- Lab 3: a neural network from scratch with NumPy (forward pass, backpropagation)
- Lab 4: CNNs, data augmentation, feature maps, transfer learning (flowers, cats vs dogs, UTKFace)
- Lab 5: RNNs, LSTM, TextVectorization and embeddings (IMDb, next word prediction)
- Lab 6: autoencoders (simple, convolutional, sparse, denoising) and outlier detection
- Lab 7: attention from scratch, multi-head attention, a Transformer for translation
- Lab 8: optimizers, hyperparameter tuning (HParams, Keras Tuner), quantization, tf.data pipelines
- TensorBoard

## Resources

- **Lecture slides** and the notebook `ML_metrics.ipynb`, shared by the lecturers during the course (not included in this repository).
- **Lab material:** the notebooks of Lab 1 to Lab 8 and the lab slides (building networks from scratch, optimizers, network optimization, input pipelines, Transformer implementation), shared during the course (not included in this repository).
- **François Chollet, *Deep Learning with Python*** (Manning): many Keras examples of the lessons come from it.
- Readings used in the lessons: Lena Voita's *NLP Course For You* (word embeddings, language modeling, seq2seq), Stanford CS224W by Jure Leskovec (graphs), MIT 6.S191 (VAEs, GANs), Pascal Poupart's CS480/680 (diffusion).
