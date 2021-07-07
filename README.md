# Tacotron 2 with linguistic disfluences

In this thesis we assess how Tacotron 2 can address Linguistical disfluences.
Disfluences come up with different flavors, in our work we only focus on prolongations.
To do so, we used ELAN to annotate the audio files and two different python packages have been created:

- "research_preprocessing" used to open files both from xml and txt (outputted by ELAN)
- "conciliator" which is used in order to match dstr table and ORT table to then create a single table unified with disfluences.

Among the approaches followed, we try to give Tacotron 2 a generic <PRL> token for the prolongations and the specific one.

Tacotron 2 has been kept unchanged from its reported implementation.# tacotron2_thesis
