# knowing_better_than_the_ai

- [knowing_better_than_the_ai](#knowing_better_than_the_ai)
- [Basic Information](#basic-information)
- [Introduction](#introduction)
- [Research Summary](#research-summary)
- [Keywords](#keywords)
- [Data](#data)
- [Dependencies](#dependencies)
- [Installation & Usage](#installation--usage)
- [License](#license)

# Basic Information

- Name of student: Lucie Kuiper
- Names of supervisors: dr. U.K. Gadiraju, G. He, prof.dr.ir. G.J.P.M. Houben
- Academic year: 22/23


# Introduction
This project aims to discover more about how the Dunning-Kruger effect affects human-AI decision making, more specifically on how the reliance of the human on the AI system changes due to the Dunning-Kruger effect in human-AI decision making when working on logical reasoning questions.

# Research Summary
Artificial Intelligence (AI) is increasingly helping people with all kinds of tasks, due to its promising capabilities. In some tasks, an AI system by itself will take over tasks, but in other tasks, an AI system making decisions on its own would be undesired due to ethical and legal reasons. In those cases, AI can still be of help by forming human-AI teams, in which humans get advice from the AI system helping them with making their final decisions. Human-AI teams are for instance used in the medical and legal fields. One problem arises, in which instances should one trust an AI system and in which not? Trusting the AI system when it is correct and trusting yourself when you are correct, results in a high appropriate reliance. If users appropriately rely on AI systems, it is possible to achieve complementary team performance, which is better than any single teammate. However, as known from previous literature, people struggle with assessing their performance and knowing how well they perform compared to peers. When one overestimates their performance this can be because of a dual burden, due to the lack of skill they also lack the skill to accurately estimate their performance. This phenomenon is called the Dunning-Kruger Effect (DKE). This raises questions about whether the inability to estimate their own capabilities would also reflect on their assessment of the AI system its performance.

In this thesis we look at how the DKE affects (appropriate) reliance on AI systems and if so, how such effects due to the DKE can be mitigated. The effects of the DKE and possible mitigation are being tested through an empirical study (N = 249). The attempt at mitigation is done by including a tutorial intervention, which has been proved in previous research to be useful in decreasing the DKE. The tutorial intervention is aimed at revealing the weaknesses of the participant and making them aware of their miscalibrated self-estimation. Furthermore, in this thesis, the effects of revealing how the AI system makes its decisions through explainable AI (XAI) are explored. The XAI consisted of highlights from logic unit-based explanations, it should allow participants to gain more understanding of the AI advice. This thesis shows how this will affect user self-assessment and reliance on the AI system.

We found that participants who overestimate themselves tend to rely less on the AI system, compared to participants that had an accurate or underestimation of their performance. After the tutorial participants have a better calibration of their self-assessment. While the designed tutorial intervention can help participants calibrate their self-assessment, it fails to promote (appropriate) reliance. Furthermore, the logic units-based explanations did not improve accurate self-assessing or increase user (appropriate) reliance on AI systems.  
This thesis shows the importance of considering cognitive biases when dealing with human-AI teams and invites more research on how to handle and mitigate the DKE in human-AI decision making.

# Keywords
Human-AI decision making, Dunning-Kruger effect, self-assessment, appropriate reliance

# Data
The data of this study can be found on:
https://osf.io/mhsr5/?view_only=4335f01fc3c248f6959895505aaae2b3

# Dependencies
The requirements can also be found in the requirements.txt

Flask==2.1.3  
Flask_Login==0.6.1  
Flask_SQLAlchemy==2.5.1  
Flask_WTF==0.15.1  
pandas==1.2.4  
psycopg2==2.9.3  
psycopg2_binary==2.9.3  
WTForms==2.3.3


# Installation & Usage
To run the program, run the run.py file as a python file, this should take care of the rest.
When accessing the website make sure to use the right prefixes (for instances "/ai/version1/?PROLIFIC_PID=")

# License
*We encourage you to use an open license and by default the repository contains an Apache License 2.0.*
