import json  # кодировать и декодировать данные
import queue  # коллекция объектов, которая поддерживает быструю семантику

import sounddevice as sd
from vosk import KaldiRecognizer, Model
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from skills import *
import words

q = queue.Queue()
model = Model("model_small")
samplerate = 16000


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def recognize(data, vectorized, clf):
    trg = words.Triggers.intersection(data.split())
    if not trg:
        voice.play("Не распознала команду, Сенпай")
        return
    data.replace(list(trg)[0], '')
    text_vector = vectorized.transform([data]).toarray()[0]
    total = clf.predict([text_vector])[0]

    func_name = total.split()[0]
    exec(func_name + '()')


def main():
    vectorized = CountVectorizer()
    vectors = vectorized.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=1, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorized, clf)


def additional_main():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=1, dtype='int16',
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                return data


if __name__ == '__main__':
    main()
