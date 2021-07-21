import argparse
import io
from typing import Callable, AnyStr, Any, Union, Dict
from google.cloud import speech



def speech_to_text(
    speechFile: str = "",
    speechLang: str = "",
    cb: Callable[ [Dict[AnyStr, Union[AnyStr, float]]], None] = None) -> None:

    client = speech.SpeechClient()

    # [START speech_python_migration_async_request]
    with io.open(speechFile, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        # encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code=speechLang,
    )

    # [START speech_python_migration_async_response]

    operation = client.long_running_recognize(config=config, audio=audio)
    # [END speech_python_migration_async_request]

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    # print(operation.status_code)
    for result in response.results:
        # just return the first one
        cb({"text": result.alternatives[0].transcript, "confidence": result.alternatives[0].confidence})
        return
        # print(u"Transcript: {}".format(result.alternatives[0].transcript))
        # print("Confidence: {}".format(result.alternatives[0].confidence))

    cb({"text": u"😞", "confidence": 0.0})