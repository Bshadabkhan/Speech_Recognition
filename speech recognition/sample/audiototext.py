

#transcribe an audio file

import assemblyai as aai
from api_secrets import API_KEY_ASSEMBLYAI

aai.settings.api_key = API_KEY_ASSEMBLYAI

# You can use a local filepath:
# audio_file = "./example.mp3"

# Or use a publicly-accessible URL:
audio_file = (
    "https://assembly.ai/wildfires.mp3"
)

transcriber = aai.Transcriber()

transcript = transcriber.transcribe(audio_file)

if transcript.status == aai.TranscriptStatus.error:
    print(f"Transcription failed: {transcript.error}")
    exit(1)

print(transcript.text)


config = aai.TranscriptionConfig(
  summarization=True,
  summary_model=aai.SummarizationModel.informative,
  summary_type=aai.SummarizationType.bullets
)

transcript = aai.Transcriber().transcribe(audio_file, config)

print(transcript.summary)
