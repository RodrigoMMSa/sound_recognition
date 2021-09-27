# Sound_recognition Project

Based on the article
[Fingerprinting and audio recognition](https://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)
from Will Drevo Website.

## Audio Fingerprinting

As the Journal of VLSI signal processing systems for signal, image and video technology states on its Abstract:
>An audio fingerprint is a compact content-based signature that summarizes an audio recording.
Audio Fingerprinting technologies have attracted attention since they allow the identification of audio independently of
its format and without the need of meta-data or watermark embedding.
Other uses of fingerprinting include: integrity verification, watermark support and content-based audio retrieval.
The different approaches to fingerprinting have been described with different rationales and terminology:
Pattern matching, Multimedia (Music) Information Retrieval or Cryptography (Robust Hashing).
In this paper, we review different techniques describing its functional blocks as parts of a common, unified framework.  
[More...](https://link.springer.com/article/10.1007/s11265-005-4151-3)

On this project we use the Cryptography method, since we are using Robust Hashing to identify sound patterns.

## Hashing
As Richard P. Salgado states in his book "Fourth Amendment Search and the Power of the Hash":
>Hashing is a powerful and pervasive technique used in nearly 
every examination of seized digital media. The concept behind hashing
is quite elegant: take a large amount of data, such as a file or all 
the bits on a hard drive, and use a complex mathematical algorithm to 
generate a relatively compact numerical identifier (the hash value) 
unique to that data. Examiners use hash values throughout the forensics process,
from acquiring the data, through analysis, and even into 
legal proceedings. Hash algorithms are used to confirm that when a 
copy of data is made, the original is unaltered and the copy is identical, bit-for-bit.  
[More...](https://heinonline.org/HOL/LandingPage?handle=hein.journals/forharoc119&div=7&id=&page=)

Throughout the Project we only used the **SHA-1** hash, that stands for Secure Hashing Algorithm 1, 
which has a 160-bit length

## How to Use
