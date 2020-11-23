import pickle
import logging
import numpy as np
import tensorflow as tf 
from model import TFNer
from keras.preprocessing.sequence import pad_sequences
from preprocess import split_text_label, padding, createMatrices


def idx_to_label(predictions, correct, idx2Label): 
    
    label_pred = []    
    for sentence in predictions:
        for i in sentence:
            label_pred.append([idx2Label[elem] for elem in i ]) 

    label_correct = []  
    if correct != None:
        for sentence in correct:
            for i in sentence:
                label_correct.append([idx2Label[elem] for elem in i ]) 
        
    return label_correct, label_pred

def predict_single_sentence(sentence, word2Idx, max_seq_len):
        sentence = list(sentence.split(" "))
        sentences = []
        wordIndices = []
        masks = []
        length = len(sentence)

        for word in sentence:
            if word in word2Idx:
                wordIdx = word2Idx[word]
            elif word.lower() in word2Idx:
                wordIdx = word2Idx[word.lower()]                 
            else:                
                wordIdx = word2Idx['UNKNOWN_TOKEN']
            wordIndices.append(wordIdx)
        maskindices = [1]*len(wordIndices)
        sentences.append(wordIndices)
        masks.append(maskindices)
        padded_inputs = tf.keras.preprocessing.sequence.pad_sequences(sentences, maxlen=max_seq_len, padding="post")
        masks = tf.keras.preprocessing.sequence.pad_sequences(masks, maxlen=max_seq_len, padding="post")
        return length, masks, padded_inputs

def predict(sentence):

    logging.basicConfig(format='%(asctime)s - %(levelname)s -  %(message)s', datefmt='%m/%d/%Y ', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # padding sentences and labels to max_length of 128
    max_seq_len = 128
    EMBEDDING_DIM = 100
    
    #test_sentence = "Steve went to Paris"
    sentence = sentence
    idx2Label = pickle.load(open("model_output/idx2Label.pkl", 'rb'))
    label2Idx = {v:k for k,v in idx2Label.items()}
    num_labels = len(label2Idx)
    word2Idx = pickle.load(open("model_output/word2Idx.pkl",'rb'))
    embedding_matrix = pickle.load(open("model_output/embedding.pkl", 'rb'))
    logger.info("Loaded idx2Label, word2Idx and Embedding matrix pickle files")

    #Loading the model
    testmodel =  TFNer(max_seq_len=max_seq_len, embed_input_dim=len(word2Idx), embed_output_dim=EMBEDDING_DIM, weights=[embedding_matrix], num_labels=num_labels)
    testmodel.load_weights("model_output/model_weights")
    logger.info("Model weights restored")

    length, masks, padded_inputs = predict_single_sentence(sentence, word2Idx, max_seq_len)
    padded_inputs = tf.expand_dims(padded_inputs, 0)
    
    true_labels = None
    pred_labels = []
    pred_logits = []

    for sentence in padded_inputs:
        logits = testmodel(sentence)
        temp1 = tf.nn.softmax(logits) 
        max_values = tf.reduce_max(temp1, axis=-1)

        masked_max_values = max_values * masks 
        preds = tf.argmax(temp1, axis=2)
        pred_labels.append(np.asarray(preds))
        pred_logits.extend(np.asarray(masked_max_values))
    _,label_pred  = idx_to_label(pred_labels, true_labels, idx2Label)
    
    label_pred = label_pred[0][:length] 
    pred_logits = pred_logits[0][:length]
    # logger.info(f"Labels predicted are {label_pred}")
    # logger.info(f"with a confidence of {pred_logits}")
    return label_pred
# if __name__ == "__main__":


#     logging.basicConfig(format='%(asctime)s - %(levelname)s -  %(message)s', datefmt='%m/%d/%Y ', level=logging.INFO)
#     logger = logging.getLogger(__name__)
#     test_sentence="PETER went to London"
#     label_pred = predict(test_sentence)
#     logger.info(f"Results for - \"{test_sentence}\"")
#     logger.info(f"Labels predicted are {label_pred}")
